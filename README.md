# Offline BNS Legal Assistant (Capstone Project)

A privacy-first, offline-capable Legal AI Assistant that replaces the old Indian Penal Code (IPC) with the new **Bharatiya Nyaya Sanhita (BNS) 2023**. 

Built as a **Final Year B.Tech Capstone Project**, this system demonstrates how to implement **Retrieval-Augmented Generation (RAG)** in highly sensitive environments (Courtrooms, Police Stations) where data sovereignty and zero-internet connectivity are mandatory.

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Tech Stack](https://img.shields.io/badge/Stack-Llama3_|_LangChain_|_Streamlit-blue)
![Privacy](https://img.shields.io/badge/Privacy-100%25_Offline-green)

## Key Features

* **100% Offline Architecture:** Runs entirely on localhost. No data leaves the machine. No OpenAI API keys required.
* **BNS-First Intelligence:** Strictly trained on the *Bharatiya Nyaya Sanhita 2023*, avoiding confusion with outdated IPC sections.
* **Evidence-Based Answers:** Every AI response cites the specific Section Number and Offense Name from the official Gazette.
* **Cognizable Offense Classifier:** Automatically identifies if an offense is Cognizable (arrest without warrant) or Non-Cognizable.

## Tech Stack

* **LLM Engine:** Llama-3 (via Ollama) / Mistral
* **Vector Database:** ChromaDB (Local Persist)
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
* **Orchestration:** LangChain (Manual RAG Pipeline)
* **Frontend:** Streamlit

## Installation & Setup

### Prerequisites
1.  Install [Ollama](https://ollama.com/) and pull the model:
    ```bash
    ollama run llama3
    ```
2.  Python 3.9+ installed.

### Steps
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/bns-offline-legal-assistant.git](https://github.com/your-username/bns-offline-legal-assistant.git)
    cd bns-offline-legal-assistant
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ingest the Data** (Build the Vector Database)
    * *Note: This reads the `bns_sections.csv` and creates a local `bns_vector_db` folder.*
    ```bash
    python ingest.py
    ```

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

## How It Works (The RAG Pipeline)

1.  **Ingestion:** The official BNS CSV is loaded.
2.  **Embedding:** Text is converted into vector embeddings using `all-MiniLM-L6-v2`.
3.  **Retrieval:** When a user queries (e.g., *"What is the punishment for mob lynching?"*), the system searches the local ChromaDB for the top 3 most relevant BNS sections.
4.  **Generation:** The retrieved sections are "stuffed" into a strict system prompt. Llama-3 generates the answer based *only* on that context.

## Why Offline? (The Problem Statement)
Legal data is sensitive. Uploading client case files or FIR details to cloud-based LLMs (like GPT-4) violates data privacy norms and the **DPDP Act 2023**. This project proves that high-quality legal intelligence can be achieved **locally**, ensuring data sovereignty for Indian Legal Institutions.