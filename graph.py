from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from retrieval import load_vector_store
from pydantic import BaseModel, Field


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
hf_token = os.getenv("HF_TOKEN")


llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    temperature=0
    )

class Grade(BaseModel):
    binary_score: str = Field(description="Answer 'yes' or 'no' if the document is relevant to the question")


class State(TypedDict):
    question : str
    document : list
    generation : str


def retrieve_node(state: State):
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    your_retrieved_docs = retriever.invoke(state['question'])
    print(f"I received the question: {state['question']}")
    return {"document": your_retrieved_docs}



def grade_documents(state: State):
    print("this is the grade node")
    grader_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a strict grader assessing relevance of a retrieved document to a user question. "
                   "If the document contains keywords or semantic meaning related to the question, grade it as 'yes'. "
                   "Otherwise, grade it as 'no'. Return ONLY the structured output."),
        ("human", "Question: {question}\n\nDocument: {document}")
    ])
    grader_chain = grader_prompt | llm.with_structured_output(Grade)
    
    filtered_docs = []
    for doc in state['document']:
        result = grader_chain.invoke({"question": state['question'], "document": doc.page_content})
        if result.binary_score == 'no':
            print("document is not relevant")
            continue
        else:
            print("document is relevant")
            filtered_docs.append(doc)
    return {"document": filtered_docs}


def decide_to_generate(state: State):
    if not state['document']:
        print("no relevant documents found")
        return END
    else:
        print("relevant documents found")
        return "generate_answer"
    

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



def generate_answer(state: State):
    print("this is the generate answer node /n")
    context = format_docs(state['document'])
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert coder. Answer the question using ONLY the following context:\n\n{context}"),
            ("human", "{input}")
        ]
    )
    chain = prompt|llm
    response = chain.invoke({"context": context, "input": state['question']})
    return {"generation": response.content}


builder = StateGraph(State)
builder.add_node("retrieve_node", retrieve_node)
builder.add_node("grade_documents", grade_documents)
builder.add_node("generate_answer", generate_answer)
builder.add_edge(START, "retrieve_node")
builder.add_edge("retrieve_node", "grade_documents")
builder.add_conditional_edges("grade_documents", decide_to_generate)
builder.add_edge("generate_answer", END)
workflow = builder.compile()


if __name__ == "__main__":
    final_state = workflow.invoke({"question": "What does the chat_with_agent function do?"})
    print(final_state)
    print(workflow.get_graph().draw_ascii())
