import sys
import tkinter as tk

root = tk.Tk()
root.title('hehe')
root.geometry('400x300')

EditBox = tk.Entry(width=50)
EditBox.insert(tk.END,"挿入する文字列")
EditBox.pack()

# EditBox.delete(0, tk.END)
root.mainloop()
