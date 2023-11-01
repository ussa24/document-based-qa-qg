from generators import *

import re


def extract_score(text):
    # find the score out of 10 in both "X out of 10" and "X/10" formats
    score_matches = re.findall(r'(\d{1,2})(?: out of 10|/10)', text)

    if score_matches:
        scores = [int(match) for match in score_matches]
        return max(scores)  # Return the highest score if multiple are found
    else:
        return 5  # Default score if no match is found


def meaning_similarity_score(student_answer, original_answer, chain):
    chat_history = []

    scoring_prompt = f"""Compare the meaning of the following two sentences and provide a score/10,
                         if although the words used are similar, the ideas expressed in the two sentences
                         are different, give it a very low score:
                      **First Sentence:**
                      "{student_answer}"

                      **Second Sentence:**
                      "{original_answer}"
                      """
    scoring_result = chain({"question": scoring_prompt, "chat_history": chat_history})
    scoring_answer = scoring_result['answer']
    score = extract_score(scoring_answer)

    return score


# Answer comparison scoring
def answer_comparison_scoring(question, student_answer, original_answer, chain):
    chat_history = []

    scoring_prompt = f"""
                    You are an expert exam corrector. You must provide a numerical score out of 10 for the student's answer in relation to the given question and the correct answer.
                    Question: {question} <end of question>
                    Student Answer: {student_answer} <end of student answer>
                    Correct Answer: {original_answer} <end of original answer>
                    """

    scoring_result = chain({"question": scoring_prompt, "chat_history": chat_history})
    scoring_answer = scoring_result['answer']
    score = extract_score(scoring_answer)

    return score


# Model based scoring
def model_based_scoring(question, student_answer, chain):
    chat_history = []

    scoring_prompt = f"You are an expert exam corrector, you will give a score out of 10 to the answer: {student_answer} of the question: {question}, please be strict and give bad scoring if the answer is wrong or doesn't exist in the document provided, and a good one if the answer is correct"

    scoring_result = chain({"question": scoring_prompt, "chat_history": chat_history})
    scoring_answer = scoring_result['answer']
    score = extract_score(scoring_answer)

    return score


# def calculate_score(question, student_answer, original_answer, chain):
#     total_score = 0
#
#     for _ in range(3):
#         meaning_similarity = float(meaning_similarity_score(student_answer, original_answer, chain))
#         answer_comparison = float(answer_comparison_scoring(question, student_answer, original_answer, chain))
#         model_scoring = float(model_based_scoring(question, student_answer, chain))
#
#         # Calculate the total score for this trial
#         trial_score = 0.2 * meaning_similarity + 0.2 * answer_comparison + 0.6 * model_scoring
#         # Accumulate the trial score
#         total_score += trial_score
#
#     # Calculate the average score over the trials
#     average_score = total_score / 3
#     return average_score


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_score(question, student_answer, original_answer, chain):
    total_score = 0

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the text data
    tfidf_matrix = vectorizer.fit_transform([student_answer, original_answer])

    # Calculate cosine similarity between the two TF-IDF representations
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    # If the similarity is below the threshold, assign a score of 0
    similarity_threshold = 0.25
    if similarity_score < similarity_threshold:
        return 0

    for _ in range(3):
        meaning_similarity = float(meaning_similarity_score(student_answer, original_answer, chain))
        answer_comparison = float(answer_comparison_scoring(question, student_answer, original_answer, chain))
        model_scoring = float(model_based_scoring(question, student_answer, chain))

        # Calculate the total score for this trial
        trial_score = 0.2 * meaning_similarity + 0.2 * answer_comparison + 0.6 * model_scoring
        # Accumulate the trial score
        total_score += trial_score

    # Calculate the average score over the trials
    average_score = total_score / 3

    return round(average_score)

# To improve the accuracy of the scoring, we calculate the score 3 times combining 3 different ways (functions) then
# (9 scores per answer) returning the average, this might lead to increasing the execution time, if you want to
# decrease it, you can just run the function below:

# def calculate_score(question, student_answer, original_answer, chain):
#     total_score = 0
#
#     meaning_similarity = float(meaning_similarity_score(student_answer, original_answer, chain))
#     answer_comparison = float(answer_comparison_scoring(question, student_answer, original_answer, chain))
#     model_scoring = float(model_based_scoring(question, student_answer, chain))
#
#     # Calculate the total score for this trial
#     trial_score = 0.2 * meaning_similarity + 0.2 * answer_comparison + 0.6 * model_scoring
#     # Accumulate the trial score
#     total_score += trial_score
#
#     return total_score
