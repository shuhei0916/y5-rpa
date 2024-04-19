# 操作リストに基づいてマウスを動かす。
# 操作リスト　-> op_listにする??
# tkinterのmainloopとシーケンサのフラグ（文字列が入力されたことをしらせるM100フラグ）を両立させるにはどうすればよいんだろう。


import tkinter as tk
from tkinter import messagebox
import pyautogui

# マウス座標の更新を行う関数
def update_position():
    x, y = pyautogui.position()
    coord_text = 'マウス座標: x: ' + str(x) + ', y: ' + str(y)
    pos_label.config(text=coord_text)
    root.after(100, update_position)

# 操作リストの出力を行う関数
def save_operations():
    s = text.get('1.0', tk.END) # WARNING: textはグローバル変数なので注意
    with open('./operation_sample.txt', mode='w') as f:
        f.write(s)
    # TODO: 書き出しに成功したことを伝えるポップアップ画面を作る。
    messagebox.showinfo('save_operations success', '保存に成功しました！')

    
def reset_text():
    text.delete('0.0', tk.END)

def execute_operations():
    try:
        with open('./operation_sample.txt', 'r') as f:
            commands = f.readline()
            for command in commands:
                exec(command.strip()) # WARNING: exec関数の使用には注意が必要
    except Exception as e:
        # print("Error exectution operations: ", e)
        messagebox.showinfo("Error exectution operations: ", e, commands)

root = tk.Tk()
root.title("Y5-OCR-RPA")
# root.geometry("400x300")

# マウス座標表示用Label
pos_label = tk.Label(root)
pos_label.pack()

# 操作リスト表示用Text 
text = tk.Text()
text.pack()

# 操作リストを書き出す用のボタン
regis_button = tk.Button(text='書き出し', command=save_operations)
regis_button.pack()

# reset_button
reset_button = tk.Button(text='リセット', command=reset_text)
reset_button.pack()

root.bind('<e>', lambda event: execute_operations())

update_position()  # 座標更新関数を初めて呼び出します

root.mainloop()