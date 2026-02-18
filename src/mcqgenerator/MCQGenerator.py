import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# Importing necessary packages from langchain
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
key = os.getenv("GROQ_API_KEY")

print("Value of GROQ_API_KEY:", key)

llm = ChatGroq(api_key=key, model="llama-3.1-8b-instant", temperature=0.3)

template = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
)

# Modern quiz chain
quiz_chain = quiz_generation_prompt | llm | StrOutputParser()

template2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz if the students
will be able to understand the questions and answer them. Only use at max 50 words for complexity analysis. 
if the quiz is not at par with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2
)

# Modern review chain
review_chain = quiz_evaluation_prompt | llm | StrOutputParser()


# Function to run both chains in sequence (replaces SequentialChain)
def generate_evaluate_chain(inputs):
    try:
        # Step 1: Generate quiz
        quiz = quiz_chain.invoke({
            "text": inputs["text"],
            "number": inputs["number"],
            "subject": inputs["subject"],
            "tone": inputs["tone"],
            "response_json": inputs["response_json"]
        })

        # Step 2: Review the generated quiz
        review = review_chain.invoke({
            "subject": inputs["subject"],
            "quiz": quiz
        })

        return {"quiz": quiz, "review": review}

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise e