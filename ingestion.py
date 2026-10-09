from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import GitLoader, PyPDFLoader, ToMarkdownLoader



def load_github_repo(url):
    loader = GitLoader(
        clone_url=url,
        repo_path="./temp_repo",
        branch="main"
    )
    docs = loader.load()
    return docs


def load_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()


def load_md_file(path):
    loader = ToMarkdownLoader(path)
    return loader.load()


def load_codebase(path):
    loader = GenericLoader.from_filesystem(
        path,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser()
    )

    docs = loader.load()
    return docs


def load_router(input):
    if input.startswith("https://github.com"):
        return load_github_repo(input)
    elif input.endswith(".pdf"):
        return load_pdf(input)
    elif input.endswith(".md"):
        return load_md_file(input)
    else:
        return load_codebase(input)


def split_docs(docs):
    all_chunks = []
    for doc in docs:
        if doc.metadata['source'].endswith(".py"):
            splitter = RecursiveCharacterTextSplitter.from_language(
                language='python',
                chunk_size=1000,
                chunk_overlap=200,
                )
            splitted = splitter.split_documents([doc])
            all_chunks.extend(splitted)

        elif doc.metadata['source'].endswith(".js"):
            splitter = RecursiveCharacterTextSplitter.from_language(
                language='javascript',
                chunk_size=1000,
                chunk_overlap=200,
                )
            splitted = splitter.split_documents([doc])
            all_chunks.extend(splitted)

        elif doc.metadata['source'].endswith(".html"):
            splitter = RecursiveCharacterTextSplitter.from_language(
                language='html',
                chunk_size=1000,
                chunk_overlap=200,
                )
            splitted = splitter.split_documents([doc])
            all_chunks.extend(splitted)
        
        elif doc.metadata['source'].endswith(".css"):
            splitter = RecursiveCharacterTextSplitter.from_language(
                language='css',
                chunk_size=1000,
                chunk_overlap=200,
                )
            splitted = splitter.split_documents([doc])
            all_chunks.extend(splitted)
        
        elif doc.metadata['source'].endswith(".md"):
            splitter = RecursiveCharacterTextSplitter.from_language(
                language='markdown',
                chunk_size=1000,
                chunk_overlap=200,
                )
            splitted = splitter.split_documents([doc])
            all_chunks.extend(splitted)

        elif doc.metadata['source'].endswith(".pdf"):
            splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", ".", " "],
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            splitted = splitter.split_documents([doc])
            all_chunks.extend(splitted)
    
    return all_chunks

def embed_docs():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder="embeddings"
    )
    return embeddings

def vector_store(docs, embeddings):
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./.chroma_db"
    )
    return vectorstore



if __name__ == "__main__":
    docs = load_codebase(r"C:\Users\Dell\Downloads\reborn\Voice-AI-Development")
    print("Documents loaded successfully!")
    splitted_docs = split_docs(docs)
    print("Documents split successfully!")
    embeddings = embed_docs()
    print("Embeddings created successfully!")
    vector_store(splitted_docs, embeddings)
    print("Vector store created successfully!")
    
