import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from groq import Groq, BadRequestError
from dotenv import load_dotenv
from prompts import *
import re
from QCM_generation import *

# Constants
NUMBER_OF_QUESTIONS = 24
PADDING = 20
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
SUCCESS_COLOR = "#27ae60"
ERROR_COLOR = "#e74c3c"

class ModernQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quiz")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Main.TFrame', background=BG_COLOR)
        self.style.configure('Header.TLabel', 
                           background=BG_COLOR,
                           font=('Helvetica', 12),
                           foreground=PRIMARY_COLOR)
        self.style.configure('Score.TLabel',
                           background=BG_COLOR,
                           font=('Helvetica', 12, 'bold'),
                           foreground=SECONDARY_COLOR)
        self.style.configure('Custom.TRadiobutton',
                           background=BG_COLOR,
                           font=('Helvetica', 11))
        self.style.configure('Action.TButton',
                           font=('Helvetica', 11, 'bold'),
                           padding=10)
        
        # Score tracking
        self.correct_answers = 0
        self.total_questions = 0
        
        # Create main container with custom padding
        self.main_frame = ttk.Frame(root, style='Main.TFrame', padding=PADDING)
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Header frame
        self.header_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.header_frame.grid(row=0, column=0, columnspan=2, pady=(0, PADDING))
        
        # Question counter with improved styling
        self.counter_label = ttk.Label(self.header_frame,
                                     text="Question 1/24",
                                     style='Header.TLabel')
        self.counter_label.grid(row=0, column=0, padx=(0, PADDING))
        
        # Score display with improved styling
        self.score_label = ttk.Label(self.header_frame,
                                   text="Score: 0/0",
                                   style='Score.TLabel')
        self.score_label.grid(row=0, column=1)
        
        # Question display with custom styling
        self.question_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.question_frame.grid(row=1, column=0, columnspan=2, pady=(0, PADDING))
        
        self.question_text = tk.Text(self.question_frame,
                                   height=4,
                                   wrap=tk.WORD,
                                   width=70,
                                   font=('Helvetica', 12),
                                   bd=2,
                                   relief=tk.GROOVE,
                                   padx=10,
                                   pady=10)
        self.question_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.question_text.config(state='disabled')
        
        # Answer section with improved layout
        self.answer_var = tk.StringVar()
        self.answers_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.answers_frame.grid(row=2, column=0, columnspan=2, pady=(0, PADDING))
        
        self.answer_buttons = []
        for i in range(4):
            btn = ttk.Radiobutton(self.answers_frame,
                                text="",
                                variable=self.answer_var,
                                value=chr(65 + i),
                                style='Custom.TRadiobutton')
            btn.grid(row=i, column=0, pady=8, sticky=tk.W)
            self.answer_buttons.append(btn)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=PADDING)
        
        # Submit button with improved styling
        self.submit_btn = ttk.Button(self.button_frame,
                                   text="Submit Answer",
                                   style='Action.TButton',
                                   command=self.check_answer)
        self.submit_btn.grid(row=0, column=0, padx=5)
        
        # Next question button with improved styling
        self.next_btn = ttk.Button(self.button_frame,
                                 text="Next Question",
                                 style='Action.TButton',
                                 command=self.load_next_question)
        self.next_btn.grid(row=0, column=1, padx=5)
        self.next_btn.state(['disabled'])
        
        # Initialize question data
        self.current_question = None
        self.correct_answer = None
        self.current_explanation = None  # New attribute to store explanation
        self.question_number = 0
        
        # Load first question
        self.load_next_question()
    
    def load_next_question(self):
        if self.question_number >= NUMBER_OF_QUESTIONS:
            self.show_final_score()
            return
        
        # Generate new question
        random_number = random.randint(1, 15)
        question, answer_A, answer_B, answer_C, answer_D, correct_answer, explanation = create_1_QCM(random_number)
        
        # Store the explanation for later use
        self.current_explanation = explanation
        
        # Update question counter
        self.question_number += 1
        self.counter_label.config(text=f"Question {self.question_number}/{NUMBER_OF_QUESTIONS}")
        
        # Update question text
        self.question_text.config(state='normal')
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, question)
        self.question_text.config(state='disabled')
        
        # Update answer buttons
        answers = [answer_A, answer_B, answer_C, answer_D]
        for i, (btn, answer) in enumerate(zip(self.answer_buttons, answers)):
            btn.config(text=f"{chr(65 + i)}. {answer}")
        
        # Reset answer selection
        self.answer_var.set('')
        
        # Store correct answer
        self.correct_answer = correct_answer
        
        # Reset button states
        self.submit_btn.state(['!disabled'])
        self.next_btn.state(['disabled'])
    
    def check_answer(self):
        if not self.answer_var.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        self.total_questions += 1
        selected_answer = self.answer_var.get()
        
        # Create custom dialog for feedback
        feedback_dialog = tk.Toplevel(self.root)
        feedback_dialog.title("Question Feedback")
        feedback_dialog.geometry("1000x600")
        feedback_dialog.configure(bg=BG_COLOR)
        
        # Make dialog modal
        feedback_dialog.transient(self.root)
        feedback_dialog.grab_set()
        
        # Create frame for content
        content_frame = ttk.Frame(feedback_dialog, style='Main.TFrame', padding=PADDING)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Result label
        if selected_answer == self.correct_answer:
            self.correct_answers += 1
            result_label = ttk.Label(content_frame,
                                   text="Correct!",
                                   style='Header.TLabel',
                                   foreground=SUCCESS_COLOR)
        else:
            result_label = ttk.Label(content_frame,
                                   text=f"Incorrect. The correct answer was {self.correct_answer}.",
                                   style='Header.TLabel',
                                   foreground=ERROR_COLOR)
        result_label.pack(pady=(0, 10))
        
        # Explanation label
        explanation_title = ttk.Label(content_frame,
                                    text="Explanation:",
                                    style='Header.TLabel')
        explanation_title.pack(pady=(0, 5))
        
        # Explanation text
        explanation_text = tk.Text(content_frame,
                                 wrap=tk.WORD,
                                 height=50,
                                 width=150,
                                 font=('Helvetica', 11),
                                 bg=BG_COLOR,
                                 relief=tk.FLAT)
        explanation_text.insert(1.0, self.current_explanation)
        explanation_text.config(state='disabled')
        explanation_text.pack(pady=(0, 10))
        
        # OK button
        ok_button = ttk.Button(content_frame,
                             text="OK",
                             style='Action.TButton',
                             command=feedback_dialog.destroy)
        ok_button.pack()
        
        # Update score
        self.score_label.config(text=f"Score: {self.correct_answers}/{self.total_questions}")
        
        # Enable/disable buttons
        self.submit_btn.state(['disabled'])
        self.next_btn.state(['!disabled'])
        
        # Wait for dialog to be closed
        self.root.wait_window(feedback_dialog)
    
    def show_final_score(self):
        percentage = (self.correct_answers / self.total_questions) * 100
        messagebox.showinfo("Quiz Complete", 
                          f"Quiz finished!\nFinal Score: {self.correct_answers}/{self.total_questions}"
                          f"\nPercentage: {percentage:.1f}%")
        self.root.quit()

def main():
    root = tk.Tk()
    app = ModernQuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()