import tkinter
from tkinter import filedialog, simpledialog, messagebox
import openai
import threading


# Initialize the main window
root = tkinter.Tk()
root.title("AguNotes")


openai.api_key = 'Secret Key' 



# Create a text widget for note-taking
text = tkinter.Text(root)
text.pack()

# Function to save the note
def save_note():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        note = text.get("1.0", "end-1c")
        with open(file, "w") as f:
            f.write(note)

# Function to delete the note
def delete_note(): 
    text.delete("1.0", "end")

# Function to upload a note
def upload_note():
    file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file:
        with open(file, "r") as f:
            note = f.read()
            text.delete("1.0", "end")
            text.insert("1.0", note)

def get_gpt_suggestions(user_notes):
    print("API Call Started")  # Debug print
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_notes}]
        )
        suggestion = response.choices[0].message.content.strip()
        print("API Call Finished")  # Debug print


        # Create a new window to display the response
        response_window = tkinter.Toplevel(root)
        response_window.title("GPT-3 Response")

        # Create a Text widget in the new window
        response_text = tkinter.Text(response_window, wrap="word", height=100, width=100)
        response_text.insert("1.0", suggestion)
        response_text.config(state="disabled")  # Make the text read-only
        response_text.pack()

        # Optionally, you can add a scrollbar to the Text widget

    except Exception as e:
        messagebox.showerror("Error", str(e))
        print("Error:", e)  # Debug print
        

def chat_with_gpt():
    print("Chat with GPT function called")  # Debug print
    user_notes = text.get("1.0", "end-1c")
    if user_notes.strip():
        threading.Thread(target=get_gpt_suggestions, args=(user_notes,)).start()
    else:
        messagebox.showinfo("No Input", "Please enter some notes before asking for suggestions.")

        
# Create buttons for saving, deleting, uploading notes, and chatting with GPT
save_button = tkinter.Button(root, text="Save Note", command=save_note)
delete_button = tkinter.Button(root, text="Delete Note", command=delete_note)
upload_button = tkinter.Button(root, text="Upload Note", command=upload_note)
chat_button = tkinter.Button(root, text="AI Suggestions", command=chat_with_gpt)

save_button.pack()
delete_button.pack()
upload_button.pack()
chat_button.pack()

# Run the application
root.mainloop()