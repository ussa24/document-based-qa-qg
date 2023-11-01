import re

from googletrans import Translator
from langchain.embeddings import HuggingFaceEmbeddings  # Embeddings generator
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Text splitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)

# embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cuda"}
embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)


# Function to translate text

def translate(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text


def split_and_store(text):
    # Split the text into sentences based on the numbered format
    sentences = re.split(r'\d+\.', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # Split each sentence by the "Answer" delimiter and organize into question-answer pairs
    qa_pairs = []
    for sentence in sentences:
        parts = re.split(r'\bAnswer\b', sentence)
        if len(parts) == 2:
            translated_question = translate(parts[0].strip(), "fr")
            translated_answer = translate(parts[1].strip(), "fr")
        else:
            # If "Answer" delimiter is missing, use "?" as delimiter
            parts = sentence.split("?")
            if len(parts) == 2:
                translated_question = translate(parts[0].strip(), "fr")
                translated_answer = translate(parts[1].strip(), "fr")
            else:
                continue  # Skip this sentence if neither "Answer" nor "?" found

        qa_pairs.append({"question": translated_question, "answer": translated_answer})

    # Create a dictionary to store question-answer pairs indexed by numbers
    qa_dict = {str(index): pair for index, pair in enumerate(qa_pairs, start=1)}

    return qa_dict
