# 📄 AI PDF Chat RAG Application

An AI-powered PDF Question Answering application built using **Python**, **Streamlit**, **LangChain**, **Google Gemini**, **FAISS**, and **Retrieval-Augmented Generation (RAG)**.

The application allows users to upload any PDF document, ask questions in natural language, retrieve the most relevant information using a vector database, and generate accurate answers using Google's Gemini Large Language Model.

---

# 🚀 Features

* 📂 Upload PDF documents
* 📖 Automatic PDF text extraction
* ✂️ Intelligent text chunking
* 🧠 Google Gemini Embeddings
* 🗄️ FAISS Vector Database
* 🔍 Similarity Search Retriever
* 🤖 Google Gemini 2.5 Flash LLM
* 💬 Context-aware Question Answering
* ⚡ Cached PDF Processing
* 🎨 Streamlit User Interface

---

# 🏗️ System Architecture

```
                 User
                   │
                   ▼
            Upload PDF
                   │
                   ▼
          PyPDFLoader
                   │
                   ▼
   RecursiveCharacterTextSplitter
                   │
                   ▼
  Google Gemini Embeddings
                   │
                   ▼
        FAISS Vector Store
                   │
                   ▼
            Retriever
                   │
                   ▼
      Relevant PDF Chunks
                   │
                   ▼
     Google Gemini 2.5 Flash
                   │
                   ▼
           Final AI Answer
```

---

# 🛠️ Tech Stack

| Component             | Technology              |
| --------------------- | ----------------------- |
| Programming Language  | Python                  |
| Frontend              | Streamlit               |
| AI Framework          | LangChain               |
| Large Language Model  | Google Gemini 2.5 Flash |
| Embeddings            | Gemini Embedding Model  |
| Vector Database       | FAISS                   |
| PDF Loader            | PyPDFLoader             |
| Environment Variables | python-dotenv           |

---

# 📂 Project Structure

```
rag-pdf-chat-gemini/

│── app.py
│── requirements.txt
│── README.md
│── SETUP.md
│── VERSION_FIX.md
│── .env.example
│── .gitignore
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-pdf-chat-gemini.git
```

Move into the project folder

```bash
cd rag-pdf-chat-gemini
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate Virtual Environment (Windows)

```bash
.venv\Scripts\activate
```

Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a file named

```
.env
```

Add your Google Gemini API Key

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

> **Note:** Never upload your `.env` file to GitHub.

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will start on

```
http://localhost:8501
```

---

# 📸 Application Workflow

```
Upload PDF
      │
      ▼
Read PDF
      │
      ▼
Split into Chunks
      │
      ▼
Generate Embeddings
      │
      ▼
Store in FAISS
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Generate AI Answer
      │
      ▼
Display Answer in Streamlit
```

---

# 📷 Screenshots

## Home Screen

(Add Screenshot Here)

```
screenshots/home.png
```

---

## Upload PDF

(Add Screenshot Here)

```
screenshots/upload.png
```

---

## AI Generated Answer

(Add Screenshot Here)

```
screenshots/answer.png
```

---

# 📖 How Retrieval-Augmented Generation (RAG) Works

1. User uploads a PDF.
2. The PDF is loaded using **PyPDFLoader**.
3. The extracted text is split into smaller chunks.
4. Each chunk is converted into vector embeddings using **Google Gemini Embeddings**.
5. The embeddings are stored inside a **FAISS Vector Database**.
6. When the user asks a question, the Retriever finds the most relevant chunks.
7. Those chunks are passed as context to **Google Gemini 2.5 Flash**.
8. Gemini generates an accurate answer based on the retrieved context.
9. The answer is displayed in the Streamlit application.

---

# 🌟 Future Enhancements

* ✅ Multiple PDF Support
* ✅ Chat History
* ✅ Conversation Memory
* ✅ Source Page References
* ✅ Save FAISS Index Locally
* ✅ Authentication
* ✅ Dark Mode UI
* ✅ Streamlit Cloud Deployment

---

# 📚 Learning Outcomes

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation (RAG)
* LangChain Framework
* Google Gemini API
* Vector Embeddings
* FAISS Vector Database
* Streamlit Web Applications
* Prompt Engineering
* Semantic Search
* PDF Processing
* AI-powered Question Answering

---

# 👨‍💻 Author

**N. Gopalakrishnan**

Generative AI Learner

GitHub: https://github.com/YOUR_USERNAME

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you found this project helpful, please consider giving it a Star on GitHub!
