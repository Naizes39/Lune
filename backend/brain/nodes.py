from backend.brain.orchestrator import AgentState
import asyncio
from backend.memory.rag_query import query_knowledge
import ollama

async def rag_node(state: AgentState):
    rag = query_knowledge(state.user_input)
    MAX_L2_DISTANCE = 1.15
    filtered_context = []
    
    for doc, distance in zip(rag['documents'][0], rag['distances'][0]):
        if distance <= MAX_L2_DISTANCE:
            filtered_context.append(doc)
            
    if filtered_context:
        rag_context = "\n".join(filtered_context)
        state.context = rag_context
    state.next_node = "LLM"


async def llm_node(state: AgentState):
    final_prompt = f"""<context>
    {state.context}
    </context>

    <user_query>
    {state.user_input}
    </user_query>

    <critic_feedback>
    {state.feedback}
    </critic_feedback>

    Answer the user's query. If there is critic feedback,
    you must correct your previous mistakes."""
    response = await ollama.AsyncClient().generate(
        model='phi4-mini', 
        prompt=final_prompt
    )
    
    state.final_response = response.response
    state.next_node = "CRITIC"


async def router_node(state: AgentState):
    router_prompt = f"""You are an elite routing agent.
    Analyze the user's input. If the input requires searching an external database for
    specific, private, or technical context, output exactly the word: SEARCH.
    If the input is a greeting, casual conversation, or a general question you can
    answer without external data, output exactly the word: SKIP.
    Do not output anything else. No explanations.

    User input: {state.user_input}"""
    response = await ollama.AsyncClient().generate(
        model='phi4-mini', 
        prompt=router_prompt,
        options={
        'temperature': 0,    
        'stop': [' ', '\n', '.']
    }
    ) 
    decision = response.response.strip().upper()
    if "SEARCH" in decision:
        state.next_node = "RAG"
    else:
        state.next_node = "LLM"


async def critic_node(state: AgentState):
    critic_prompt = f"""You are an elite QA Engineer.
    Evaluate the following AI response to the user's query.
    If the response is perfectly accurate and highly
    professional, output exactly: PASS.
    If the response is flawed, rambling, or hallucinated,
    output a 1-sentence harsh critique of what must be
    fixed. Do not output anything else.

    <user_query>{state.user_input}</user_query>
    <ai_response>{state.final_response}</ai_response>"""
    response = await ollama.AsyncClient().generate(
        model='phi4-mini', 
        prompt=critic_prompt,
        options={
        'temperature': 0,    
    }
    ) 
    evaluation = response.response.strip()
    if evaluation == "PASS":
        state.next_node = "END"
    else:
        state.feedback = evaluation
        state.next_node = "LLM"
