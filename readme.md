# Interactive Quiz Application

## Description
This project is an interactive quiz application built with Python and Tkinter. It generates multiple-choice questions (MCQ) based on predefined markdown course files. The application selects random questions, tracks the user's score, and provides detailed feedback for each question, including explanations.

## Features
- Graphical user interface (GUI) using Tkinter.
- Randomized question selection from markdown files.
- Answer submission with validation and immediate feedback.
- Score tracking and final score display.
- Explanation display for correct and incorrect answers.
- Responsive UI with modern styling.

## Project Structure
```
Interactive-Quiz/
│-- main.py               # Main application file
│-- prompts.py            # Functions for generating prompts
│-- QCM_generation.py     # Functions for generating multiple-choice questions
│-- Cours/                # Folder containing markdown course files
│   │-- 1.md
│   │-- 2.md
│   │-- ...
│   │-- 15.md
│-- .env                  # Environment file for API keys
│-- requirements.txt       # List of dependencies
│-- README.md             # Documentation file
```

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and add the necessary API keys:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Usage
Run the application with:
```bash
python main.py
```
