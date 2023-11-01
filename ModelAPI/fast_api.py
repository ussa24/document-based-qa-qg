import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017")
db = client["db"]
collection = db["answer"]
inpcs_collection = db["inpcs"]
categories_collection = db["categories"]
que_ans_collection = db["queAns"]
answers_collection = db["answer"]
validateAnswers_collection = db["validateAnswers"]


##############################################################################################################
class StoreTextRequest(BaseModel):
    userName: str
    category: str
    text: str
    currentQuestions: str
    correctAnswer: str


# Endpoint for storing text in MongoDB
@app.post('/api/storetext')
async def store_text(request_data: StoreTextRequest):
    try:
        userName = request_data.userName
        category = request_data.category
        text = request_data.text
        current_question = request_data.currentQuestion
        correctAnswer = request_data.correctAnswer

        if text:
            # Check if the user and category combination already exists in the database
            user_entry = collection.find_one({"userName": userName, "category": category})

            if user_entry:
                # If the user and category combination exists, update the entry
                collection.update_one(
                    {"userName": userName, "category": category},
                    {"$push": {"textAndQuestion": {"currentQuestions": current_question, "userAnswer": text,
                                                   "correctAnswer": correctAnswer}}}
                )
            else:
                # If the user and category combination does not exist, create a new entry
                collection.insert_one({
                    "userName": userName,
                    "category": category,
                    "textAndQuestion": [
                        {"currentQuestions": current_question, "userAnswer": text, "correctAnswer": correctAnswer}]
                })

            return {"message": "Text and current question stored successfully"}
        else:
            raise HTTPException(status_code=400, detail="Text field is required")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


###############################################################################################################
# Pydantic model for a single question and answer
class QuestionResponse(BaseModel):
    question: str
    answer: str


# Endpoint for retrieving questions (with answers) by category
@app.get('/api/getquestions/{category}')
async def get_questions_with_answers_by_category(category: str):
    try:
        # Retrieve all questions (with answers) for the specified category
        questions_cursor = que_ans_collection.find({category: {"$exists": True}}, {category: 1, "_id": 0})

        # Extract the "question" and "answer" fields from the cursor
        questions_with_answers = [
            {"question": entry[category][i]['question'], "answer": entry[category][i]['answer']}
            for entry in questions_cursor
            for i in range(len(entry[category]))
        ]

        return {"questions": questions_with_answers}
    except Exception as e:
        return {"error": str(e)}


###############################################################################################################
@app.get("/pdfs/{category}")
async def get_pdfs(category: str):
    # Query the MongoDB collection to find filePdf names with the specified category
    pdfs = inpcs_collection.find({"category": category}, {"filePdf": 1})
    keywords = inpcs_collection.find({"category": category}, {"description": 1})

    # Extract the filePdf names from the query results
    pdf_names = [pdf["filePdf"] for pdf in pdfs]
    keywords = [key["description"] for key in keywords]

    return pdf_names, keywords


###############################################################################################################

@app.get("/categories")
async def get_categories():
    categories = categories_collection.find({}, {"name": 1})
    return {"categories": [category["name"] for category in categories]}


###############################################################################################################


@app.get("/generate_questions_all_pdfs/{category}")
async def generate_questions_all_pdfs(category: str):
    from generators import generate_json_from_pdf_files

    # Check if data for this category already exists in the que_ans_collection
    existing_data = que_ans_collection.find_one({category: {"$exists": True}})

    if existing_data:
        # If data exists, delete it
        que_ans_collection.delete_one({category: {"$exists": True}})

    result = await get_pdfs(category)

    pdfs_in_category = result[0]
    keywords_in_category = result[1]
    print(pdfs_in_category)
    print(keywords_in_category)

    questionsAnswers = generate_json_from_pdf_files(pdfs_in_category, category, keywords_in_category)
    all_pdf_data = json.loads(questionsAnswers)

    # Store the generated questions and answers in the queAns collection
    que_ans_collection.insert_one({category: all_pdf_data})

    return {"message": f"Questions and answers for all PDFs in {category} stored in queAns collection"}


###############################################################################################################

@app.get("/validate_all")
async def validate_all_users():
    from scoring import calculate_score, get_chain
    from create_score_report import create_pdf

    try:
        # Use aggregation to group by userName and category and get unique combinations
        pipeline = [
            {"$group": {"_id": {"userName": "$userName", "category": "$category"}}}
        ]

        unique_combinations = list(answers_collection.aggregate(pipeline))

        if not unique_combinations:
            return {"message": "No data found in answers_collection."}

        for combo in unique_combinations:
            userName = combo["_id"]["userName"]
            category = combo["_id"]["category"]

            # Find answers for the specified user and category
            user_answers = answers_collection.find_one({"userName": userName, "category": category},
                                                       {"textAndQuestion": 1})

            if not user_answers:
                continue  # Skip if no answers found for this user and category.

            text_and_question = user_answers.get("textAndQuestion", [])

            result = []
            total_score = 0

            for item in text_and_question:
                current_question = item["currentQuestions"]
                user_answer = item.get("userAnswer")
                correct_answer = item.get("correctAnswer")
                pdfs_list = await get_pdfs(category)

                pdfs_in_category = pdfs_list[0]

                chain = get_chain(pdfs_in_category)

                score = calculate_score(current_question, user_answer, correct_answer, chain)
                total_score = total_score + score

                result.append({
                    "currentQuestions": current_question,
                    "userAnswers": user_answer,
                    "correct_answer": correct_answer,
                    "score": score
                })

            final_score = (total_score / len(text_and_question)) * 10
            final_score_str = f"{final_score}%"

            # Check if there are existing documents with the same userName and category in validateAnswers_collection
            existing_data = validateAnswers_collection.find_one({"userName": userName, "category": category})

            if existing_data:
                # If data exists, delete it
                validateAnswers_collection.delete_one({"userName": userName, "category": category})

            # Insert the result into the validateAnswers_collection
            validateAnswers_collection.insert_one({
                "userName": userName,
                "category": category,
                "textAndQuestion": result,
                "total_score": final_score_str
            })

            valideted = validateAnswers_collection.find()
            create_pdf(valideted)

            delete_liste_attente = answers_collection.find_one({"userName": userName, "category": category})

            if delete_liste_attente:
                # If data exists in answers_collection, delete it
                answers_collection.delete_one({"userName": userName, "category": category})
        return {"message": "Validation completed for all users and categories."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""
import random

# This endpoint validates for a specific user, we kept it for potential future use

@app.get("/validate/{userName}/{category}")
async def get_user_answers(userName: str, category: str):
    from scoring import get_chain
    from scoring import calculate_score

    # Find answers for the specified user and category
    user_answers = answers_collection.find_one({"userName": userName, "category": category}, {"textAndQuestion": 1})

    if not user_answers:
        return {"message": "No answers found for this user and category."}

    text_and_question = user_answers.get("textAndQuestion", [])

    result = []
    total_score = 0



    for item in text_and_question:
        question = item["currentQuestions"]
        student_answer = item.get("userAnswer")
        original_answer = item.get("correctAnswer")
        pdfs_in_category = await get_pdfs(category)

        chain = get_chain(pdfs_in_category)

        score = calculate_score(question, student_answer, original_answer, chain)
        total_score = total_score+score

        result.append({
            "currentQuestions": question,
            "userAnswers": student_answer,
            "correct_answer": original_answer,
            "score": score
        })

    final_score = (total_score / len(text_and_question)) * 10
    final_score = round(final_score)
    final_score_str = f"{final_score}%"

    # Check if there are existing documents with the same userName and category
    existing_data = validateAnswers_collection.find_one({"userName": userName, "category": category})

    if existing_data:
        # If data exists, delete it
        validateAnswers_collection.delete_one({"userName": userName, "category": category})

    # Insert the result into the answers_collection
    validateAnswers_collection.insert_one({
        "userName": userName,
        "category": category,
        "textAndQuestion": result,
        "total_score": final_score_str
    })

    delete_liste_attente = answers_collection.find_one({"userName": userName, "category": category})

    if delete_liste_attente:
        # If data exists, delete it
        answers_collection.delete_one({"userName": userName, "category": category})

    return result 
"""

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000)
