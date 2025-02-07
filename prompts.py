import random


def create_user_prompt(extract):
    
    prompt = f'''Generate a multiple-choice question (MCQ) in JSON format based on the following text.  
The JSON should include:
- "question": The generated question.
- "choices": A dictionary with keys "A", "B", "C", and "D" representing answer choices.
- "correct_answer": The key corresponding to the correct choice (e.g., "A", "B", "C", or "D").

Here is the text on which the question should be based:  
"{extract}"  

Return only the JSON object without additional text.'''
    
    return prompt

def create_system_prompt():
    prompt = '''You are a university professor. 
You are preparing a multiple-choice question (QCM) for your students. 
Here are some examples of questions you could ask:

{
  "question": "What does Electroencephalography (EEG) record?",
  "choices": {
    "A": "Action potentials",
    "B": "Passive conduction",
    "C": "Both action potentials and passive conduction",
    "D": "Neither action potentials nor passive conduction"
  },
  "correct_answer": "B"
}

{
  "question": "Neglect syndrome, often resulting from damage to the right parietal lobe, is a disorder of:",
  "choices": {
    "A": "Memory",
    "B": "Spatial awareness",
    "C": "Language comprehension",
    "D": "Motor skills"
  },
  "correct_answer": "B"
}

{
  "question": "Which of the following is an example of crystallized intelligence?",
  "choices": {
    "A": "Solving a brand-new logic puzzle without prior experience",
    "B": "Quickly adapting to a new problem-solving strategy",
    "C": "Recalling historical facts to answer a quiz",
    "D": "Discovering a new way to solve a math problem you've never encountered before"
  },
  "correct_answer": "C"
}
'''
    return prompt
  
  
def explanation_prompt(file_content, QCM):
    
    prompt = f'''I will give you a extract from a text and a multiple-choice question. 
You will have to explain the answer to the QCM based on the extract.

Here is the multiple-choice question (MCQ) :  
"{QCM}"  


Here is the text on which the question is based:
"{file_content}"
'''
    return prompt
  
def create_system_prompt_explanation():
    prompt = '''You are a university professor. 
You are providing feedback to a student who answered a multiple-choice question (QCM) incorrectly.
Explain why the correct answer is indeed correct and why the other choices are incorrect.'''
    
    return prompt