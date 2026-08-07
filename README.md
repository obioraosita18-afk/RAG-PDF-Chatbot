# RAG PDF Chatbot

An intelligent chatbot that reads any PDF document and answers questions from it — powered by LLaMA 3.3 on Groq, LangChain, FAISS, and Flask.

##  What It Does

Upload any PDF file and ask it questions. The chatbot will:
- Read and understand your PDF
- Find the most relevant information
- Answer your questions accurately
- Tell you honestly when it doesn't know something

##  Built With

- **Python** — core programming language
- **Flask** — web framework
- **LangChain** — AI pipeline management
- **FAISS** — vector database for fast search
- **Groq + LLaMA 3.3** — language model for answering questions
- **PyMuPDF** — PDF text extraction

##  How It Works

1. User uploads a PDF
2. PDF is read and split into chunks
3. Chunks are converted into vectors and stored in FAISS
4. User asks a question
5. Most relevant chunks are retrieved
6. LLaMA reads the chunks and answers the question

##  How To Run Locally

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Add your Groq API key to .env
5. Run the app

##  Built By

Obiora Osita Nwankwo — AI/ML Engineer | Prompt Engineer | Data Scientist

Connect with me on LinkedIn: linkedin.com/in/obiora-osita-3068513b2