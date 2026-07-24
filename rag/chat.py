from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client=OpenAI()

embedding_model=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db= QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)
#user ask 
user_query=input("ASK SOMETHING....")

#relevent chunks of data
search_results=vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata['page_label']}\n"
    f"File Location: {result.metadata['source']}"
    for result in search_results
])

SYSTEM_PROMPT=f'''
You are a helpful AI assistant who answers queries based on the available context and data retrieved from a pdf file along with page_contents and page number.

you should only answer the user based on the following context and navigate  the user to open the right page number to know more.

Context:
{context}
'''

response=openai_client.chat.completions.create(
    model="gpt-5",
    messages=[{
        "role":"system","content":SYSTEM_PROMPT
    },
    {
        "role":"user","content":user_query
    }]
)

print(response.choices[0].message.content)