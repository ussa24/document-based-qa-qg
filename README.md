# Document based Question Generation, Question Answering and Auto Answer Evaluation using RAG, LLaMA-2,LangChain, VectorDB, HuggingFace Embeddings

## Project Introduction

The main aim of this project is to create an API that generates
questions from documents in any language and provides accurate long form
answers in french, making it easier to understand and interact with
complex information, ultimately supporting virtual learning.

## RAG Architecture

Retrieval Augmented Generation (RAG) is an AI framework that enhances
the quality of responses generated by an LLM by supplementing its
internal representation of information with external sources of
knowledge.

In our case, the knowledge is the PDF documents provided, and the output
is our question/answer pairs.

![alt](https://github.com/ussa24/document-based-qa/blob/main/images/rag.jpg?raw=true)


## Project Workflow

![alt](https://github.com/ussa24/document-based-qa/blob/main/images/workflow-libs.png?raw=true)

# RAG Implementation

## Data Preprocessing

The PDFs undergo a set of preprocessing operations to make them usable.
Firstly, for each PDF file, we extract the text. Next, this text is
divided into smaller segments to facilitate processing. then, we
generate vector embeddings to represent the text as vectors
comprehensible to the model.

### Text Extracting

Here we iterate through the PDFs to extract text using the built in
**PyPDF2** function from **LangChain**.

### Split into Chunks

To facilitate text processing and to ensure that the LLM goes through
all text data, we split text into small chunks using the **LanChain Text
Splitter**.

### Vector Embeddings

We used the Embedding Model from HuggingFace
[`sentence-transformers/all-mpnet-base-v2`](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)
to represent text into vectors.

## Vector Store

The vector representations generated in the preprocessing stage are
stored in a **vector store** as contextual data. This allows efficient
access to these vectors by the language model. We used the open source
local VectorDB **FAISS** from Meta AI.

## Question Generation & Answering {#question-generation--answering}

The vectors and contextual data are provided to
[`meta-llama/Llama-2-7b-chat-hf`](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
that analyzes and processes this information to generate raw output.

## Post-Processing

The raw output then undergoes a post-processing stage. Firstly, the text
is filtered to remove unwanted elements using **Regex**. Then, it is
translated into the French language using **google-trans** open-source
translation library.

## Output:

Finally, the questions and answers are formatted in a JSON format that
is parseable, making it easy to parse and integrate into the API.

# Evaluation Algorithm:

After several attempts, we managed to develop an optimal algorithm that
takes into account the entire context rather than comparing each word
individually. This algorithm also relies on LLaMA-2, thus exploiting its
ability to capture the meaning of sentences. It integrates three
different approaches that use the same model but with different prompts.
It is somewhat like a voting system, where each of these approaches
assigns a score, and we then calculate the average of these scores to
obtain the final result.

![alt](https://github.com/ussa24/document-based-qa/blob/main/images/eval.png?raw=true)

The use of cosine similarity at the beginning of the algorithm is used
to filter out responses that lack any form of accuracy, for example,
when the user says \"I don't know\" or provides a response devoid of
meaning. This filter aims to reduce computations, as it would be
unnecessary to engage the scoring algorithm in such cases. The outputs
of each evaluation function are then subjected to a regex filter to
extract only the score, ignoring the model's comments.

# FastAPI Integration

We implemented a FastAPI API to interact with the RAG system, the API
has 3 main endpoints:

- **POST /api/storetext:**

This endpoint is used to store text and related data in the MongoDB
database.

- **GET /categories:**

This endpoint retrieves a list of available categories from the MongoDB
database.

- **GET /api/getquestions/{category}:**

This endpoint retrieves questions (with answers) for a specific category
from the MongoDB database. It queries the database for questions and
answers related to the specified category.

- **GET /pdfs/{category}:**

Retrieves PDF file names and keywords associated with a specific
category. It queries the database for PDF file names and keywords
related to the specified category and returns them as a JSON response.

- **GET /validate_all:**

This endpoint performs the evaluation of user answers for all users and
categories. After validation is complete, the data in the
answers_collection is deleted for each user and category.
