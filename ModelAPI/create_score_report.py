import os

import pymongo
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db"]
collection = db["validateAnswers"]
data = collection.find()

# Ensure the 'score_reports' folder exists
if not os.path.exists("score_reports"):
    os.mkdir("score_reports")

smaller_font_style = ParagraphStyle('SmallerFont')
smaller_font_style.fontName = 'Helvetica'
smaller_font_style.fontSize = 5


def create_pdf(score_data):
    for item in score_data:
        pdf_filename = f"score_reports/{item['userName']}_report_{item['category']}.pdf"  # Use _id as the filename
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        # Add user information
        c.setFont("Helvetica", 8)
        c.drawString(100, 750, f"User Name: {item['userName']}")
        c.drawString(100, 735, f"Category: {item['category']}")

        # Set font size and color for the title "Vanguard Center"
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.darkblue)  # Dark blue color

        # Calculate the width of the title
        title = "Vanguard Center-UM6P"
        title_width = c.stringWidth(title, "Helvetica-Bold", 12)

        # Calculate the X position to center the title
        x_centered = (letter[0] - title_width) / 2

        # Add centered "Vanguard Center" title in red at the top
        c.drawString(x_centered, 770, title)
        # Add questions and answers
        y = 700  # Initial Y position
        for question in item['textAndQuestion']:
            # Use smaller font size for all text
            question_text = f"Question: {question['currentQuestions']}"
            user_answer_text = f"User Answer: {question['userAnswers']}"
            correct_answer_text = f"Correct Answer: {question['correct_answer']}"
            score_text = f"Score: {question['score']}"

            question_paragraph = Paragraph(question_text, style=smaller_font_style)
            user_answer_paragraph = Paragraph(user_answer_text, style=smaller_font_style)
            correct_answer_paragraph = Paragraph(correct_answer_text, style=smaller_font_style)
            score_paragraph = Paragraph(score_text, style=smaller_font_style)
            # Check if there is enough space on the current page
            if y - 80 < 50:  # 50 is a margin for the footer and next page
                c.showPage()  # Start a new page
                y = 700  # Reset Y position
            question_paragraph.wrapOn(c, 400, 60)
            user_answer_paragraph.wrapOn(c, 400, 60)
            correct_answer_paragraph.wrapOn(c, 400, 60)
            score_paragraph.wrapOn(c, 400, 60)

            question_paragraph.drawOn(c, 100, y)
            user_answer_paragraph.drawOn(c, 100, y - 20)
            correct_answer_paragraph.drawOn(c, 100, y - 40)
            score_paragraph.drawOn(c, 100, y - 60)

            y -= 80  # Adjust the Y position for the next question
        # Add total score
        c.drawString(100, y - 80, f"Total Score: {item['total_score']}")

        c.save()
        print(f"PDF saved as {pdf_filename}")
