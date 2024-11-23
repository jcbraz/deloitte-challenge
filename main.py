from dotenv import load_dotenv
load_dotenv(override=True)

import faiss
from openai import AzureOpenAI
from src.services.models.embeddings import Embeddings
from src.services.vectorial_db.faiss_index import FAISSIndex
from src.ingestion.ingest_files import ingest_files_data_folder
from src.services.models.llm import LLM
import os
from dotenv import load_dotenv
import time

def rag_chatbot(llm: LLM, input_text:str, history: list, index: FAISSIndex):
    """Retrieves relevant information from the FAISS index, generates a response using the LLM, and manages the conversation history.

    Args:
        llm (LLM): An instance of the LLM class for generating responses.
        input_text (str): The user's input text.
        history (list): A list of previous messages in the conversation history.
        index (FAISSIndex): An instance of the FAISSIndex class for retrieving relevant information.

    Returns:
        tuple: A tuple containing the AI's response and the updated conversation history.
    """

    context = index.retrieve_chunks(query=input_text, num_chunks=5)
    
    stream_response = llm.get_response(history=history, context=context, user_input=input_text)

    history.append({"role": "user", "content": input_text})
    history.append({"role":"assistant", "content": stream_response})


    return "ECO-GUIDE:", history 


def main():
    """Main function to run the chatbot."""

    embeddings = Embeddings()
    
    index = FAISSIndex(embeddings=embeddings.get_embeddings)

    try:
        index.load_index()
    except FileNotFoundError:
        raise ValueError("Index not found. You must ingest documents first.")

    llm = LLM()
    history = []
    print("\n# INTIALIZED CHATBOT #")

    while True:
        user_input = str(input("You:  "))
        if user_input.lower() == "exit":
            break
        response, history = rag_chatbot(llm, user_input, history, index)
        
        print("AI: ", response)


if __name__ == "__main__":
    main()