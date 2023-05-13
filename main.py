import tkinter as tk
from tkinter import filedialog, scrolledtext

class Node:
    def __init__(self, text='', left=None, right=None):
        self.text = text
        self.left = left
        self.right = right
       # self.length = len(text) + (0 if not left else left.length) + (0 if not right else right.length)

class Rope:
    def __init__(self, text=''):
        self.root = self._build_rope(text.splitlines())

    """def _build_rope(self, text):
        if len(text) < 1024:
            return Node(text)
        else:
            mid = len(text) // 2
            left = self._build_rope(text[:mid])
            right = self._build_rope(text[mid:])
            return Node(text='', left=left, right=right)"""


    def _build_rope(self, lines):
        if len(lines) == 1:
            text = lines[0]
            if len(text) < 1024:
                return Node(text)
            else:
                mid = len(text) // 2    # Split strings in half
                left = self._build_rope([text[:mid]])
                right = self._build_rope([text[mid:]])

                return Node(text='', left=left, right=right)
        else:
            mid = len(lines) // 2
            left = self._build_rope(lines[:mid])
            right = self._build_rope(lines[mid:])
            return Node(text='', left=left, right=right)

    def get_text(self):
        return self._get_text(self.root)

    def _get_text(self, node):
        if not node.left and not node.right:
            return node.text
        else:
            return self._get_text(node.left) + self._get_text(node.right)
# -------------------------
def find_matches(text, search_string):
    matches = []
    for i in range(len(text) - len(search_string) + 1): # total - len(searched) + 1
        if text[i:i+len(search_string)] == search_string:   # Each index of i : is checked for the entire string
            matches.append(i)
    return matches  # Contains the index of all of the occurence of text

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as f:
            text = f.read()
        input_text.delete('1.0', tk.END)    # Clear
        input_text.insert('1.0', text)      # Insert New


def save_file():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        with open(file_path, 'w') as f:
            text = output_text.get('1.0', tk.END)
            f.write(text)

"""def highlight_matches():
    text = input_text.get('1.0', tk.END).strip()    
    text = text.replace('\n', ' ')
    search_string = search_entry.get().strip()
    if not search_string:
        return
    rope = Rope(text)   
 
    for match_index in matches:  
        output_text.tag_add('highlight', f'{start_line}.{start_index}',f'{end_line}.{end_index}')   
        output_text.tag_config('highlight', background='yellow')"""

def highlight_matches():
    text = input_text.get('1.0', tk.END).strip()    # Get the text in the widget also strip white spaces
    text = text.replace('\n', ' ')
    search_string = search_entry.get().strip()  # Get text from the search string widget
    if not search_string:
        return
    rope = Rope(text)   # Rope object from text variable
    matches = find_matches(rope.get_text(), search_string)  # find all matches
    output_text.delete('1.0', tk.END)
    output_text.insert('1.0', text)
    for match_index in matches: # loops over each matched index
        start_line, start_index = output_text.index(f'1.{match_index}').split('.')  # For each match gets start and end position and split it into line and column components(widget)
        end_line, end_index = output_text.index(f'1.{match_index + len(search_string)}').split('.')
        output_text.tag_add('highlight', f'{start_line}.{start_index}',f'{end_line}.{end_index}')   # Highlighter
        output_text.tag_config('highlight', background='yellow')

# Creating a GUI

root = tk.Tk()

root.title("Text Highlighter")

# Creating Input Text Box

input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

input_label = tk.Label(input_frame, text="Input Text")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD)
input_text.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

# Creating Output Text Box

output_frame = tk.Frame(root)
output_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

output_label = tk.Label(output_frame, text="Output Text")
output_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
output_text.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

search_frame = tk.Frame(root)
search_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

# Creating Search Box

search_label = tk.Label(search_frame, text="Search String:")
search_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

search_button = tk.Button(search_frame, text="Search", command=highlight_matches)
search_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

# Creating menu bar

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# configure row and column weights to make them adjustable

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=0)

# main event loop

root.mainloop()
