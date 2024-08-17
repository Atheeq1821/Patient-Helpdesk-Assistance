import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=40,
            length_function=len,
            is_separator_regex=False,
        )

def calculate_chunk_ids(chunks):

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        print(current_page_id)
        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        print(chunk_id)
        last_page_id = current_page_id
        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def denial_embeddings(path):
    document_loader = PyPDFDirectoryLoader(path)
    docs=document_loader.load()

    #splittting data

    splitted=text_splitter.split_documents(docs)
    CHROMA_PATH='chroma\denial'

    db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=embeddings,
            collection_name="denial"
        )

    chunks_with_ids = calculate_chunk_ids(splitted)
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        # db.persist() neede onl y in jpter
    else:
        print("✅ No new documents to add")


def embeddings_creation(path,policy_name):


    #loading data
    document_loader = PyPDFDirectoryLoader(path)
    docs=document_loader.load()

    #splittting data

    splitted=text_splitter.split_documents(docs)
    CHROMA_PATH='chroma\policies'

    db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=embeddings,
            collection_name=policy_name
        )

    chunks_with_ids = calculate_chunk_ids(splitted)
    existing_items = db.get(include=[]) #retriving existing documents from the database
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")