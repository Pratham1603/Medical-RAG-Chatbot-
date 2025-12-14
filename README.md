# Medical-RAG-Chatbot
### Build a Complete Medical Chatbot with LLMs (TinyLlama), LangChain, Pinecone, Flask & AWS

![Medical Chatbot Screenshot](static/images/chatbot_preview.png.png)

## 📝 Project Overview

This project is an advanced **Medical Chatbot** designed to provide accurate, context-aware answers to medical queries. Unlike standard chatbots that can "hallucinate" or make up facts, this bot uses a technique called **Retrieval-Augmented Generation (RAG)**.

It retrieves real information from a trusted medical knowledge base (PDF documents) before generating an answer. This ensures the responses are grounded in factual data rather than just the model's training memory.

### 🌟 Key Features
* **Source-Grounded Answers:** Uses a custom knowledge base (e.g., medical textbooks/PDFs) to answer questions.
* **Open-Source & Efficient:** Powered by **TinyLlama-1.1B**, a compact but powerful LLM that runs efficiently without high costs.
* **Fast Retrieval:** Utilizes **Pinecone**, a vector database, to instantly find the most relevant medical context for every user question.
* **Interactive UI:** Built with **Flask** to provide a clean, user-friendly chat interface.
* **Deployment Ready:** Configured for seamless deployment on **AWS (EC2 & ECR)** using Docker and GitHub Actions.

---

## ⚙️ How It Works

1.  **Ingestion:** Medical PDF documents are loaded and split into small chunks.
2.  **Embedding:** These chunks are converted into numerical vectors (embeddings) using **Hugging Face** models.
3.  **Storage:** The vectors are stored in **Pinecone**, a specialized vector database.
4.  **Retrieval:** When a user asks a question, the system searches Pinecone for the most similar text chunks.
5.  **Generation:** The retrieved text is sent along with the user's question to the **TinyLlama** model, which generates a natural language answer based *only* on that context.

---

## 🛠️ Tech Stack

- **Python:** Core programming language.
- **LangChain:** Framework for orchestrating the RAG pipeline.
- **Flask:** Web framework for the chatbot UI.
- **HuggingFace:** Source for the LLM (TinyLlama-1.1B) and Embeddings (`all-MiniLM-L6-v2`).
- **Pinecone:** Vector database for semantic search.
- **AWS:** Cloud platform for deployment (EC2, ECR).
- **Docker:** Containerization for consistent deployment.

---

## 🚀 How to run?

### STEPS:

### 1\. Clone the repository

```bash
git clone [https://github.com/Pratham1603/Medical-RAG-Chatbot.git](https://github.com/Pratham1603/Medical-RAG-Chatbot.git)
```

### 2\. Create a conda environment

```bash
conda create -n medibot python=3.10 -y
```

```bash
conda activate medibot
```

### 3\. Install the requirements

```bash
pip install -r requirements.txt
```

### 4\. Configure Environment Variables

Create a `.env` file in the root directory and add your Pinecone and HuggingFace credentials:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
HUGGINGFACEHUB_ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 5\. Ingest Data (Create Vector Store)

Run the following command to process your PDFs and store embeddings in Pinecone:

```bash
python store_index.py
```

### 6\. Run the Application

Finally, run the Flask app:

```bash
python app.py
```

Now, open your browser and go to:

```bash
http://localhost:8080
```

-----

## AWS CI/CD Deployment with Github Actions

### 1\. Login to AWS console.

### 2\. Create IAM user for deployment

**Grant the following permissions (Policies):**

1.  `AmazonEC2ContainerRegistryFullAccess`
2.  `AmazonEC2FullAccess`

**Description:**

1.  **EC2 access:** Virtual machine to run the app.
2.  **ECR:** Elastic Container Registry to save your docker image.

### 3\. Create ECR repo to store the docker image

  - Create a repository named `medicalbot` (or similar).
  - **Save the URI:** `your-account-id.dkr.ecr.your-region.amazonaws.com/medicalbot`

### 4\. Create EC2 machine (Ubuntu)

### 5\. Install Docker in EC2 Machine:

**Optional (Update system):**

```bash
sudo apt-get update -y
sudo apt-get upgrade
```

**Required (Install Docker):**

```bash
curl -fsSL [https://get.docker.com](https://get.docker.com) -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

### 6\. Configure EC2 as self-hosted runner:

Go to your GitHub Repo -\> **Settings** \> **Actions** \> **Runners** \> **New self-hosted runner** \> Choose Linux \> Run the provided commands one by one in your EC2 terminal.

### 7\. Setup GitHub Secrets:

Go to your GitHub Repo -\> **Settings** \> **Secrets and variables** \> **Actions** \> **New repository secret**. Add the following:

  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION` (e.g., us-east-1)
  - `ECR_REPO` (The URI you saved in Step 3)
  - `PINECONE_API_KEY`
  - `HUGGINGFACEHUB_ACCESS_TOKEN`

<!-- end list -->

````