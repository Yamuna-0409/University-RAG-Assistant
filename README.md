# 🎓 University RAG Assistant

### AI-Powered University Document Search & Question Answering System

University RAG Assistant is an AI-powered web application that allows students to ask questions about university academic documents and receive relevant answers using **Retrieval-Augmented Generation (RAG)**.

The system processes university documents, cleans and chunks the extracted text, generates semantic embeddings, retrieves the most relevant information, and provides it as context to a local **Llama 3.2** language model running through **Ollama**.

---

## 🚀 Features

* 📄 University document ingestion and text extraction
* 🧹 Document cleaning and preprocessing
* ✂️ Intelligent document chunking
* 🧠 Semantic embeddings using Sentence Transformers
* 🔎 Vector-based semantic search
* 🔑 Hybrid vector + keyword retrieval
* 🤖 Retrieval-Augmented Generation (RAG)
* 🦙 Local Llama 3.2 LLM using Ollama
* 💬 Interactive React chat interface
* 📋 University document summarization
* 📚 Source chunk identification for generated answers
* ⚡ FastAPI REST API backend

---

## 🏗️ System Architecture

University Documents
        ↓
   Text Extraction
        ↓
   Data Cleaning
        ↓
   Document Chunking
        ↓
 Semantic Embeddings
        ↓
 Vector + Keyword Search
        ↓
 Relevant Context Retrieval
        ↓
        RAG
        ↓
   Llama 3.2 + Ollama
        ↓
    FastAPI Backend
        ↓
    React Frontend
        ↓
   Student's Answer


## 🔄 How It Works

### 1. Document Ingestion

University PDF documents are stored in the raw data directory.

### 2. Text Extraction

Python and PyPDF are used to extract text from the university PDF.

### 3. Data Cleaning

Extracted text is cleaned by removing unnecessary blank lines and formatting issues.

### 4. Document Chunking

The cleaned document is divided into smaller chunks so that relevant sections can be retrieved efficiently.

### 5. Embedding Generation

Each document chunk is converted into a numerical vector using:

---text
all-MiniLM-L6-v2


These embeddings capture the semantic meaning of the document content.

### 6. Information Retrieval

When a user asks a question, the question is converted into an embedding and compared with document embeddings.

The system also uses keyword matching to improve retrieval for important terms such as years and semesters.

### 7. RAG

The most relevant document chunks are provided as context to the language model.

The model generates an answer using the retrieved university information rather than relying on external knowledge.

### 8. Local LLM

Llama 3.2 runs locally through Ollama, allowing the project to work without paid cloud LLM APIs.

### 9. Web Application

FastAPI exposes the RAG functionality through REST APIs, while React provides the interactive user interface.

---

## 🧩 Project Modules

### Backend


backend/
│
├── extract_text.py
├── clean_text.py
├── chunk_text.py
├── create_embeddings.py
├── vector_search.py
├── spark_process.py
├── rag.py
└── main.py


### Frontend


frontend/
│
├── src/
│   ├── App.jsx
│   ├── App.css
│   └── index.css
│
├── package.json
└── vite.config.js



## 🛠️ Tech Stack

| Category            | Technologies                             |
| ------------------- | ---------------------------------------- |
| Programming         | Python, JavaScript                       |
| Frontend            | React.js, Vite, CSS                      |
| Backend             | FastAPI, Uvicorn                         |
| Document Processing | PyPDF                                    |
| Embeddings          | Sentence Transformers                    |
| Embedding Model     | all-MiniLM-L6-v2                         |
| AI Architecture     | Retrieval-Augmented Generation (RAG)     |
| LLM                 | Llama 3.2                                |
| LLM Runtime         | Ollama                                   |
| Search              | Vector Similarity + Keyword Search       |
| Data Engineering    | PySpark, Bronze/Silver/Gold Architecture |
| Tools               | VS Code, Git, GitHub                     |

---

## 📁 Data Pipeline

The project follows a structured data processing approach:


Raw PDF
   ↓
Bronze
   ↓
Extracted Text
   ↓
Silver
   ↓
Cleaned Text
   ↓
Gold
   ↓
Document Chunks
   ↓
Embeddings


The project also includes a PySpark processing pipeline designed for structured data processing.


## 💻 Installation & Setup

### 1. Clone the Repository

---bash
git clone 


### 2. Create Virtual Environment

---bash
python -m venv .venv


Activate it on Windows:

---powershell
.\.venv\Scripts\Activate.ps1


### 3. Install Python Dependencies

---bash
pip install -r requirements.txt


### 4. Install Frontend Dependencies

---bash
cd frontend
npm install


### 5. Start Ollama

Make sure Ollama is installed and run:

---bash
ollama run llama3.2:3b


### 6. Start Backend

From the project root:

---bash
uvicorn backend.main:app --reload


Backend:

---text
http://127.0.0.1:8000


### 7. Start Frontend

Open another terminal:

---powershell
cd D:\University_Knowledge_AI\frontend
npm run dev


Frontend:

---text
http://localhost:5173


---

## 💬 Example Questions

The assistant can answer questions such as:

What are the courses in the first year?

<img width="1796" height="901" alt="image" src="https://github.com/user-attachments/assets/5a8a7292-4165-4abf-aaa2-b7c49625967b" />

Retrieved Information:
I Year - I Semester
I Year - II Semester

Generated Answer:
The first year includes subjects such as Engineering
Mathematics, Green Chemistry, English, Computer
Programming using C, IT Essentials, Data Structures
Using C, Computer Organization, and other subjects
listed in the university syllabus.

What is Data Structures using C?

## 📊 Example RAG Output

<img width="1828" height="892" alt="Screenshot 2026-09-15 142652" src="https://github.com/user-attachments/assets/ce2a5a17-f76d-43af-9100-1c5c5e97d529" />


What subjects are included in the CSE syllabus?

It retrieves relevant sections from the university document and generates an answer using the retrieved context.


## 🔐 Privacy & Cost

The project uses **Ollama with Llama 3.2 locally** for answer generation.

Therefore:

* No paid OpenAI API is required
* No external LLM API is required
* University document content can remain on the local system during inference

---

## 🎯 Project Objectives

* Build an AI assistant for university document retrieval
* Apply Retrieval-Augmented Generation
* Implement semantic document search
* Process and structure document data
* Integrate a local Large Language Model
* Build a complete full-stack AI application
* Demonstrate practical use of GenAI and Data Engineering concepts

---

## 🔮 Future Enhancements

* Support multiple university documents
* Add a dedicated vector database
* Improve document chunking strategies
* Add metadata-based filtering
* Integrate cloud-based Databricks processing
* Add multilingual question answering
* Add chat history
* Add user authentication
* Deploy the application to the cloud


---

## ⭐ Project Highlights
```
---text
✔ Retrieval-Augmented Generation
✔ Semantic Search
✔ Local LLM with Ollama
✔ Llama 3.2
✔ Sentence Transformers
✔ FastAPI
✔ React.js
✔ Document Processing
✔ PySpark
✔ Data Engineering Pipeline
```

