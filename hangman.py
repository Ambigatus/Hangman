import random
import tkinter as tk
from tkinter import messagebox

with open("words.txt") as f:
	words = [word.strip() for word in f]

# Define the hangman visualization
hangman_visuals = [
"""
|------|
|      |
|      
|      
|      
|      
""",
"""
|------|
|      |
|      O
|      
|      
|      
""",
"""
|------|
|      |
|      O
|      |
|      
|      
""",
"""
|------|
|      |
|      O
|     /|
|      
|      
""",
"""
|------|
|      |
|      O
|     /|\\
|      
|      
""",
"""
|------|
|      |
|      O
|     /|\\
|     / 
|      
""",
"""
|------|
|      |
|      O
|     /|\\
|     / \\
|      
"""
]

word = random.choice(words).lower()
max_guesses = 6
guessed_letters = []

#define the GUI from tkinter
root = tk.Tk()
root.title("Hangman")

word_label = tk.Label(root, text="Word: " + " ".join(["_" for _ in range(len(word))]))
word_label.pack()

hangman_label = tk.Label(root, text=hangman_visuals[0])
hangman_label.pack()

guesses_left_label = tk.Label(root, text="Guesses left: " + str(max_guesses))
guesses_left_label.pack()

guess_label = tk.Label(root, text="Guess a letter: ")
guess_label.pack()

guess_entry = tk.Entry(root)
guess_entry.pack()

result_label = tk.Label(root, text="")
result_label.pack()

#Function for GUI update
def update_gui():
	displayed_word = ""
	for letter in word:
		if letter in guessed_letters:
			displayed_word += letter + " "
		else:
			displayed_word += "_ "
	word_label.config(text="Word: " + displayed_word)
	guesses_left_label.config(text="Guesses left: " + str(max_guesses - len(set(guessed_letters) - set(word))))
	guess_entry.delete(0, tk.END)

#Function for handle a guess
def handle_guess():
    global max_guesses
    guess = guess_entry.get().lower()
    if guess in guessed_letters:
        result_label.config(text="You already guessed that letter!")
    elif guess in word:
        guessed_letters.append(guess)
        if all(letter.lower() in guessed_letters for letter in word):
            result_label.config(text="Congratulations, you won!")
            guess_entry.config(state=tk.DISABLED)
        else:
            result_label.config(text="Correct!")
            update_gui()
    else:
        guessed_letters.append(guess)
        max_guesses -= 1
        if max_guesses == 0:
            result_label.config(text="Sorry, but you lose. The word was " + word)
            guess_entry.config(state=tk.DISABLED)
        else:
            result_label.config(text="Incorrect! Try harder!")
            hangman_label.config(text=hangman_visuals[7 - max_guesses])
            update_gui()

guess_entry.bind("<Return>", lambda event: handle_guess())

# Define the reset function
def reset_game():
	global word, guessed_letters
	word = random.choice(words).lower()
	guessed_letters = []
	max_guesses = 6
	result_label.config(text="")
	hangman_label.config(text=hangman_visuals[0])
	guess_entry.config(state=tk.NORMAL)
	update_gui()

#Add a retry button
retry_button = tk.Button(root, text="Retry?", command=reset_game)
retry_button.pack()

#Start the game
root.mainloop()