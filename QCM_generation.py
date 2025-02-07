import random
import os
from groq import Groq, BadRequestError
from dotenv import load_dotenv
from prompts import *
import re


# Constants
MODEL = "llama3-8b-8192"

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_chat_completion(system_prompt: str, user_prompt: str, model: str = MODEL):
    """Generate text using Groq API."""
    client = Groq(api_key=GROQ_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model=model,
        temperature=0.5,
    )
    return chat_completion.choices[0].message.content

def create_1_QCM(category):
    #load file 
    path = os.path.join("Cours", str(category) + ".md")
    with open(path, "r", encoding="utf-8") as file:
        file_content = file.read()
        
    #count number of line in the file
    number_of_line = len(file_content.split("\n"))
    batch_size = 20
    num_paragraphe = random.randint(1, number_of_line//batch_size)
    extract = file_content.split("\n")[num_paragraphe*batch_size: (num_paragraphe+1)*batch_size]
    # extract each element of the list 'extract' and put it in a string with a new line between each element
    extract = "\n".join(extract)
    
    

    
    user_prompt = create_user_prompt(extract)
    system_prompt = create_system_prompt()
    generate_QCM = generate_chat_completion(system_prompt, user_prompt)
    user_explanation_prompt = explanation_prompt(file_content, generate_QCM)
    system_prompt_explanation = create_system_prompt_explanation()
    #explanation = generate_chat_completion(system_prompt_explanation, user_explanation_prompt)
    explanation = extract
    
    match_question = re.search(r'"question":\s*"(.*?)"', generate_QCM)
    if match_question:
        question = match_question.group(1)
    else:
        question = "Question not found."
        
    match_answer_A = re.search(r'"A":\s*"(.*?)"', generate_QCM)
    if match_answer_A:
        answer_A = match_answer_A.group(1)
    else:
        answer_A = "A not found."
        
    match_answer_B = re.search(r'"B":\s*"(.*?)"', generate_QCM)
    if match_answer_B:
        answer_B = match_answer_B.group(1)
    else:
        answer_B = "B not found."
        
    match_answer_C = re.search(r'"C":\s*"(.*?)"', generate_QCM)
    if match_answer_C:
        answer_C = match_answer_C.group(1)
    else:
        answer_C = "C not found."
        
    match_answer_D = re.search(r'"D":\s*"(.*?)"', generate_QCM)
    if match_answer_D:
        answer_D = match_answer_D.group(1)
    else:
        answer_D = "D not found."
        
    match_correct_answer = re.search(r'"correct_answer":\s*"(.*?)"', generate_QCM)
    if match_correct_answer:
        correct_answer = match_correct_answer.group(1)
    else:
        correct_answer = "Correct answer not found." 
        
    # Create a list of tuples containing (answer_letter, answer_text)
    answer_pairs = [
        ('A', answer_A),
        ('B', answer_B),
        ('C', answer_C),
        ('D', answer_D)
    ]

    # Find the original letter of the correct answer
    original_correct_letter = correct_answer  # e.g., 'A', 'B', 'C', or 'D'

    # Shuffle the pairs
    random.shuffle(answer_pairs)

    # Reassign the shuffled answers
    answer_A = answer_pairs[0][1]
    answer_B = answer_pairs[1][1]
    answer_C = answer_pairs[2][1]
    answer_D = answer_pairs[3][1]

    # Update correct_answer to match the new position
    for new_letter, (original_letter, answer_text) in zip(['A', 'B', 'C', 'D'], answer_pairs):
        if original_letter == original_correct_letter:
            correct_answer = new_letter
            break
            
    return question, answer_A, answer_B, answer_C, answer_D, correct_answer, explanation

  

