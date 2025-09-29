from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"] = "AIzaSyAY2SoL3vsHRJihyBfMFc1JKolqYyJ4Lj4"
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: ChatState):
    messages = state.get("messages", [])
    if not messages:
        return {"messages": []}
    try:
        response = gemini_llm.invoke(messages, timeout=40)
    except Exception as e:
        response = type('obj', (object,), {'content': f"❗ Error: {e}"})()
    return {"messages": [response]}

graph_builder = StateGraph(ChatState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
memory = MemorySaver()
app_graph = graph_builder.compile(checkpointer=memory)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    messages: list
@app.get("/")
def root():
    return {"message": "Welcome to LangGraph Gemini Chatbot Backend"}

@app.post("/chat")
async def chat(req: MessageRequest):
    result = app_graph.invoke(ChatState(messages=req.messages),
                             config={"configurable": {"thread_id": "1"}})
    bot_reply = result["messages"][-1].content
    return {"reply": bot_reply}
#https://github.com/Jananii2611/chat_bot_vac.git