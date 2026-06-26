import streamlit as st
import tempfile
import os

from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Environment variables (including LangSmith keys) are loaded here
load_dotenv()

# ----------------------------------------------------
# PAGE SETUP (Light Theme Baseline)
# ----------------------------------------------------
st.set_page_config(
    page_title="PDF AI: Ask Your PDF",
    page_icon="📄",
    layout="wide"
)

# ----------------------------------------------------
# CLEAN LIGHT THEME CUSTOM CSS 
# ----------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        color: #212529 !important;
    }
    .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3 {
        color: #212529 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e9ecef;
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #495057 !important;
        font-size: 16px !important;
        font-weight: 500;
    }
    div[data-testid="stFileUploader"] {
        background-color: #e9ecef !important;
        border: 2px dashed #0d6efd !important;
        border-radius: 12px;
        padding: 25px !important;
        text-align: center;
    }
    div[data-testid="stFileUploader"] label, div[data-testid="stFileUploader"] p {
        color: #0d6efd !important;
        font-weight: bold !important;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 8px;
        margin-bottom: 10px;
        padding: 15px !important;
    }
    .custom-card {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .btn-action {
        color: white !important;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Dashboard Header Layout
col_title, col_user = st.columns([4, 1])
with col_title:
    st.markdown("<h1 style='color: #212529; margin-bottom: 0;'>📄 PDF AI: Ask Your PDF</h1>", unsafe_allow_html=True)
    st.write("Upload a PDF and ask questions about its content using RAG with LangSmith tracing.")
with col_user:
    st.markdown("<div style='text-align: right; padding-top: 15px; color: #495057;'>Welcome,<br><b>User</b> 👤</div>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("<h2 style='color: #0d6efd; margin-top: 0;'>🏠 Home</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='margin-bottom: 15px;'>📂 Files</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='margin-bottom: 15px;'>💬 Chat</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='margin-bottom: 15px;'>📊 Analytics</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='margin-bottom: 15px;'>⚙️ Settings</p>", unsafe_allow_html=True)

# Cached PDF Document Processor
@st.cache_resource(show_spinner=False)
def process_pdf(file_bytes, file_name):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_bytes)
        temp_pdf_path = temp_file.name

    loader = PyPDFLoader(temp_pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, 
        chunk_overlap=500
    )
    chunks = text_splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
    
    try:
        os.unlink(temp_pdf_path)
    except:
        pass
        
    return vectorstore, len(documents), len(chunks)

# Main Workspace File Uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

if uploaded_file is None:
    st.write("### Recent Documents")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='custom-card'>📄<br><b>Q4 Sales.pdf</b><br><small style='color:#6c757d;'>2026-06-25</small></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='custom-card'>📄<br><b>Product Specs.pdf</b><br><small style='color:#6c757d;'>2026-06-24</small></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='custom-card'>📄<br><b>Team Manual.pdf</b><br><small style='color:#6c757d;'>2026-06-20</small></div>", unsafe_allow_html=True)

    st.write("### Quick Actions")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        st.markdown("<div class='btn-action' style='background-color: #0d6efd;'>📝 Summarize</div>", unsafe_allow_html=True)
    with qa2:
        st.markdown("<div class='btn-action' style='background-color: #6f42c1;'>📊 Extract Data</div>", unsafe_allow_html=True)
    with qa3:
        st.markdown("<div class='btn-action' style='background-color: #fd7e14;'>🌐 Translate</div>", unsafe_allow_html=True)

else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.sidebar.success("✅ Document Attached!")
    st.sidebar.write(f"**Name:** {uploaded_file.name}")

    with st.spinner("🧠 Initializing contextual document arrays..."):
        try:
            file_bytes = uploaded_file.read()
            vectorstore, total_pages, total_chunks = process_pdf(file_bytes, uploaded_file.name)
            
            retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # Input area
            if question := st.chat_input("💬 Ask a question about your uploaded PDF..."):
                with st.chat_message("user"):
                    st.write(question)
                st.session_state.messages.append({"role": "user", "content": question})

                with st.chat_message("assistant"):
                    with st.spinner("🤖 Extracting intelligence..."):
                        # LangChain will automatically trace retriever invoke and LLM run to LangSmith
                        results = retriever.invoke(question)
                        context = "\n\n".join([doc.page_content for doc in results])

                        # UPDATED PROMPT: Fixed acronym definition issue so accurate answers hit UI
                        prompt = f"""
                        You are an intelligent AI assistant.

                        Answer the user's question. Use the provided context to give the most accurate answer related to the document.
                        If the question is about defining or expanding an acronym found in the document (like MSME), you can use your general knowledge to explain what it stands for, and then use the context to explain its relevance or schemes mentioned in the context.

                        Context:
                        {context}

                        Question:
                        {question}

                        Answer:
                        """
                        response = llm.invoke(prompt)
                        ai_answer = response.content
                        
                        st.write(ai_answer)
                        st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                        
                        with st.expander("📌 View Reference Source Text"):
                            for idx, doc in enumerate(results, start=1):
                                st.markdown(f"<div style='background-color: #f1f3f5; padding: 12px; border-radius: 6px; border-left: 4px solid #0d6efd; margin-bottom: 10px; color: #212529;'><b>Source Chunk {idx}:</b><br>{doc.page_content}</div>", unsafe_allow_html=True)
                                
        except Exception as e:
            st.error(f"Error: {e}")