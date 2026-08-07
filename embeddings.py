from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from groq import Groq
import os
from dotenv import load_dotenv
import numpy as np

# Load our secret API key from .env file
load_dotenv()

# This is our custom embedding class using Groq
class GroqEmbeddings(Embeddings):
    """
    This class converts text into numbers (vectors) that the AI can understand.
    Think of it like translating English into a secret math language that 
    computers can search through super fast.
    """
    
    def __init__(self):
        # Connect to Groq using our API key
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
    
    def embed_documents(self, texts):
        """
        Convert a list of text chunks into vectors.
        This runs on all our PDF chunks at once.
        """
        embeddings = []
        for text in texts:
            embedding = self._get_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, text):
        """
        Convert a single question into a vector.
        This runs on the user's question when they ask something.
        """
        return self._get_embedding(text)
    
    def _get_embedding(self, text):
        """
        This is the actual function that talks to Groq and gets the embedding.
        We ask Groq to summarize the meaning of the text as numbers.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an embedding assistant. When given text, respond with exactly 10 comma-separated numbers between -1 and 1 that represent the semantic meaning of the text. Nothing else, just the numbers."
                },
                {
                    "role": "user", 
                    "content": f"Convert this to embedding numbers: {text[:500]}"
                }
            ],
            max_tokens=100
        )
        
        # Get the numbers from Groq's response
        numbers_text = response.choices[0].message.content.strip()
        
        # Convert the text numbers into actual Python numbers
        try:
            numbers = [float(x.strip()) for x in numbers_text.split(',')]
            # Make sure we always have exactly 10 numbers
            if len(numbers) != 10:
                numbers = [0.0] * 10
        except:
            numbers = [0.0] * 10
            
        return numbers


def split_text_into_chunks(text):
    """
    This function takes our big wall of text from the PDF and 
    cuts it into smaller pieces called chunks.
    
    Why? Because AI can't process one giant text — it works better 
    with smaller, focused pieces. Like reading a book chapter by chapter
    instead of all at once.
    """
    
    # This tool cuts our text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # each chunk is 500 characters long
        chunk_overlap=50,    # chunks overlap by 50 characters so we don't lose context
        length_function=len
    )
    
    # Cut the text into chunks
    chunks = text_splitter.split_text(text)
    
    print(f"Your PDF was split into {len(chunks)} chunks")
    
    return chunks


def create_vector_store(chunks):
    """
    This function takes our chunks and converts them into vectors,
    then stores them in FAISS — our searchable database.
    
    Think of FAISS like a super smart filing cabinet that can find 
    the most relevant information in milliseconds.
    """
    
    print("Creating embeddings... this may take a moment")
    
    # Create our embedding tool
    embeddings = GroqEmbeddings()
    
    # Create the vector store from our chunks
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    print("Vector store created successfully!")
    
    return vector_store