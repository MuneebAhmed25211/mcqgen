import os
import re
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("Error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format. Only PDF and text files supported.")


def get_table_data(quiz_str):
    try:
        # Clean the quiz string by extracting just the JSON part
        json_match = re.search(r'\{.*\}', quiz_str, re.DOTALL)
        if not json_match:
            raise Exception("No valid JSON found in quiz output")
        
        # Convert the quiz from str to dict
        quiz_dict = json.loads(json_match.group())
        quiz_table_data = []
        
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}-> {option_value}" 
                    for option, option_value in value["options"].items()
                ]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False