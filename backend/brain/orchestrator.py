from dataclasses import dataclass
import asyncio


@dataclass  
class AgentState:
    user_input: str
    context: str = ""
    final_response: str = ""
    feedback: str = ""
    next_node: str = "START"


class Orchestrator:
    def __init__(self):
        self.nodes: dict = {}

    
    def add_node(self, name: str, func: callable):
        self.nodes[name] = func
    

    async def run(self, state: AgentState) -> AgentState:
        while state.next_node != "END":
            name = state.next_node
            func = self.nodes.get(name)
            if not func:
                raise ValueError(f"Node '{name}' does not exist.")
            await func(state)
        return state