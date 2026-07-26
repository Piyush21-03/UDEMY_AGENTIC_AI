from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import  StateGraph,START,END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm= init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)

class State(TypedDict):
    messages:Annotated[list, add_messages]

def chatbot(state:State):
    response=llm.invoke(state.get("messages"))
    return {"messages":[response]}


graph_builder=StateGraph(State)
graph_builder.add_node("chatbot",END)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph=graph_builder.compile()

def compile_graph_with_checkpointer():
    DB_URl="mongodb://admin:admin@localhost:27017/lg" 
    with MongoDBSaver.from_conn_string(DB_URl) as checkpointer:
        graph=graph_builder.compile(checkpointer=checkpointer)
    return graph

graph_with_checkpointer=compile_graph_with_checkpointer()

updated_state=graph.checkpointer.invoke(State({"messages":["hi my name is Piyush Panigrahi"]}))
print("\n\nUpdated State",updated_state)