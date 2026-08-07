def retrieve_relevant_chunks(vector_store, question, k=3):
    """
    This function searches our smart filing cabinet (vector store)
    and finds the most relevant chunks that match the user's question.
    
    Think of it like a librarian who searches through all 25 pages
    and picks the 3 most relevant ones that answer your question.
    
    k=3 means we pick the top 3 most relevant chunks.
    You can change this number if you want more or fewer results.
    """
    
    # Search the vector store for the most similar chunks
    relevant_chunks = vector_store.similarity_search(question, k=k)
    
    # Extract just the text from the results
    context = ""
    for i, chunk in enumerate(relevant_chunks):
        context += f"Chunk {i+1}:\n{chunk.page_content}\n\n"
    
    return context