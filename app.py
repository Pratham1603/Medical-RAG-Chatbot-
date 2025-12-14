from flask import Flask, render_template, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HUGGINGFACEHUB_ACCESS_TOKEN = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["HUGGINGFACEHUB_ACCESS_TOKEN"] = HUGGINGFACEHUB_ACCESS_TOKEN

embeddings = download_embeddings()

index_name = "medical-rag-chatbot"

# Load the existing index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize the LLM
# Using TinyLlama because it is open (no gated error) and lightweight (fast on CPU)
llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    device=-1,  # -1 for CPU. Change to 0 if you have a GPU.
    pipeline_kwargs={
        "max_new_tokens": 256, 
        "temperature": 0.5,
        "repetition_penalty": 1.1,
        "return_full_text": False  # <--- ADD THIS LINE
    }
)

# Define the Prompt Template
# We wrap the prompts in <|system|>, <|user|>, and <|assistant|> tags
qa_prompt = PromptTemplate(
    template="<|system|>\n" + system_prompt + "\nContext:\n{context}</s>\n<|user|>\n{question}</s>\n<|assistant|>",
    input_variables=["context", "question"]
) 

# Initialize RetrievalQA Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": qa_prompt}
)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    user_input = msg
    print(f"User Input: {user_input}")
    
    # .invoke is required for LangChain 0.3.x
    response = qa.invoke({"query": user_input})
    
    print("Response : ", response["result"])
    return str(response["result"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)