import os
from groq import Groq
from dotenv import load_dotenv
from pdf_loader import load_pdf
from embeddings import split_text_into_chunks, create_vector_store
from retriever import retrieve_relevant_chunks

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def process_pdf(pdf_path):
    print("Reading your PDF...")
    text = load_pdf(pdf_path)
    print("Splitting into chunks...")
    chunks = split_text_into_chunks(text)
    print("Creating vector store...")
    vector_store = create_vector_store(chunks)
    print("PDF is ready! You can now ask questions.")
    return vector_store

def ask_question(vector_store, question):
    print("Searching for relevant information...")
    context = retrieve_relevant_chunks(vector_store, question)
    
    prompt = "You are a helpful assistant that answers questions based ONLY on the provided document content.\n\n"
    prompt += "Here is the relevant content from the document:\n"
    prompt += context + "\n"
    prompt += "User question: " + question + "\n\n"
    prompt += "Rules:\n"
    prompt += "- Only answer based on the document content above\n"
    prompt += "- If the answer is not in the document say: I could not find that information in the document\n"
    prompt += "- Be clear and helpful\n"
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful document assistant. You only answer questions based on the document content provided to you."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    return answer