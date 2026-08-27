from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from contextlib import asynccontextmanager
from backend.memory.database import init_db, safe_save_chat_turn
from backend.validation.schemas import Message
import asyncio
from backend.memory.cache import get_cache, set_cache
from pydantic import BaseModel, Field
from typing import Annotated
import uuid
from datetime import datetime
from backend.brain.orchestrator import Orchestrator, AgentState
from backend.brain.nodes import rag_node, llm_node, critic_node, router_node



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Lune", lifespan=lifespan)


class ChatRequest(BaseModel):
    user_id: Annotated[str, Field(min_length=1, max_length=4)]
    content: Annotated[str, Field(min_length=1, max_length=50000)]


@app.post('/agent/chat')
async def chat(user_req: ChatRequest):
    user = Message(
        message_id=str(uuid.uuid4()),
        role="user",
        content=user_req.content,
        time_sent=datetime.now(),
        session_id="1",
        user_id=user_req.user_id
    )
    response = await get_cache(user.content)
    if response:
        assistant = Message(
        message_id=str(uuid.uuid4()),
        role="assistant",
        content=response,
        time_sent=datetime.now(),
        session_id="1",
        user_id='2'
        )
    else: 
        state = AgentState(user_input=user.content)
        orchestrator = Orchestrator()
        orchestrator.add_node("START", router_node)
        orchestrator.add_node("RAG", rag_node)
        orchestrator.add_node("LLM", llm_node)
        orchestrator.add_node("CRITIC", critic_node)

        final_state = await orchestrator.run(state)
        response = final_state.final_response


        assistant = Message(
        message_id=str(uuid.uuid4()),
        role="assistant",
        content=response,
        time_sent=datetime.now(),
        session_id="1",
        user_id='2'
        )


        await set_cache(user.content, response)
    await safe_save_chat_turn(user=user, assistant=assistant)
    return response


@app.websocket("/ws/voice")
async def voice_websocket(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received via WebSocket {data}")
            await websocket.send_text(f"Echo from server: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected.")


if __name__ ==  "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
