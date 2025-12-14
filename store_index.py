from dotenv import load_dotenv
import os
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings   
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
 
load_dotenv() 

PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
HUGGINGFACEHUB_ACCESS_TOKEN=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["HUGGINGFACEHUB_ACCESS_TOKEN"]=HUGGINGFACEHUB_ACCESS_TOKEN

extracted_docs = load_pdf_files("Data/")
filter_data = filter_to_minimal_docs(extracted_docs)
text_chunk = text_split(filter_data)

embeddings = download_embeddings()  

pinecone_api_key = PINECONE_API_KEY
#Authenticate Pinecone
pc = Pinecone(api_key=pinecone_api_key)


index_name = "medical-rag-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 384, # Dimension of the embeddings
        metric = "cosine", # Cosine Similarity
        spec = ServerlessSpec( cloud = "aws" , region="us-east-1")
    )
index = pc.Index(index_name)


docsearch = PineconeVectorStore.from_documents(
    documents=text_chunk,
    embedding=embeddings,
    index_name=index_name
)