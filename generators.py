import json  # JSON parsing

from langchain.document_loaders import PyPDFLoader  # PDF Loader
from langchain.vectorstores import FAISS  # Vector store faiss-cpu (On a linux system, use faiss-gpu `pip install
# faiss-gpu`)
from langchain.chains import ConversationalRetrievalChain  # Document retrieval chain

from llm import *
from preprocessing import *


def generate_json_from_pdf_files(pdf_files, category, keywords):
    chat_history = []
    prompt2 = ("""Your are an expert exam author, based on the information from the document provided, write 10 relevant
               questions followed by their correct, long and detailed answers, numerated from 1, to 10 and never mention
               yourself or the document, never say 'as exam author', never say 'According to the document',
               the questions must be about the general concepts, don't dive too much into details.""")

    # Initialize an empty list to store all question-answer pairs
    all_qa_pairs = []

    for pdf_file in pdf_files:
        # Load and split each file separately
        pdf_path = "uploads/" + pdf_file

        print(pdf_path)
        loader = PyPDFLoader(pdf_path)
        documents = loader.load_and_split()
        all_splits = text_splitter.split_documents(documents)
        print(all_splits[0])

        # Generate embeddings and initialize vectorstore and chain for each file separately
        vectorstore = FAISS.from_documents(all_splits, embeddings)
        chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), return_source_documents=True)

        # Generate questions for each file separately and regenerate if JSON data is empty (up to 2 attempts)
        for attempt in range(2):
            result = chain({"question": prompt2, "chat_history": chat_history})
            answer = result['answer']
            print(answer)
            # Translate and format the questions and answers into JSON for each file separately
            qa_dict = split_and_store(answer)

            if qa_dict:
                all_qa_pairs.extend(qa_dict.values())  # Append the question-answer pairs to the list
                break  # If JSON data is not empty, break the loop
            else:
                reserve = []

                # categorie = "Data Analysis"
                # keywords = "Data warhousing, data visualization, Power BI"

                prompt = f"generate 10 questions and their correct, long and detailed answers about {category} and its description: {keywords}, numerated from '1.' to '10.'"

                all_pdfs_chain = get_chain(pdf_files)

                result = all_pdfs_chain({"question": prompt, "chat_history": chat_history})
                answer = result['answer']

                reserve = split_and_store(answer)
                reserve_json_string = json.dumps(reserve, indent=4, ensure_ascii=False)

                qa_dict = reserve_json_string  # Assign the reserve array when JSON data is empty


    # Convert the list of question-answer pairs into a JSON string
    all_json_string = json.dumps(all_qa_pairs, indent=4, ensure_ascii=False)
    print(type(all_json_string))
    return all_json_string


def get_chain(pdf_files):
    all_splits = []
    for pdf_file in pdf_files:
        # Load and split each file separately
        pdf_path = "uploads/" + pdf_file
        loader = PyPDFLoader(pdf_path)
        documents = loader.load_and_split()
        all_splits.extend(text_splitter.split_documents(documents))
    # Generate embeddings and initialize vectorstore and chain for all files together
    vectorstore = FAISS.from_documents(all_splits, embeddings)
    chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), return_source_documents=True)
    return chain
