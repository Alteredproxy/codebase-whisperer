from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    temperature=0
    )

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder="embeddings"
    )
    return Chroma(persist_directory="./.chroma_db", embedding_function=embeddings)
   

vectorstore = load_vector_store()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert coder. Answer the question using ONLY the following context:\n\n{context}"),
        ("human", "{input}")
    ]
)

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

if __name__ == "__main__":
    response = retrieval_chain.invoke({"input": "What does the chat_with_agent function do?"})
    print(response["answer"])
    
