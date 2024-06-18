# print("hehe\nHEhe")
# exit()

#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter as tk


root = tk.Tk()
root.title(u"Software Title")
root.geometry("400x300")

def delete_entry(event):
    EditBox.delete(0, tk.END)

# Entry
EditBox = tk.Entry(width=40)
EditBox.insert(tk.END, "挿入する文字列\nhehehe")
EditBox.pack()

# Button
Button = tk.Button(text=u'ボタンです', width=100)
Button.bind("<Button-1>", delete_entry)

Button.pack()

root.mainloop()
