# 操作リストに基づいてマウスを動かす。
# 操作リスト　-> op_listにする??
# tkinterのmainloopとシーケンサのフラグ（文字列が入力されたことをしらせるM100フラグ）を両立させるにはどうすればよいんだろう。


import tkinter as tk
import pyautogui

# マウス座標の更新を行う関数
def update_position():
    x, y = pyautogui.position()
    coord_text = 'x: ' + str(x) + ', y: ' + str(y)
    pos_label.config(text=coord_text)
    root.after(100, update_position)

# 操作リストの出力を行う関数
def output_op():
    s = text.get('1.0', tk.END) # textはグローバル変数なので、注意
    with open('./operation_sample.txt', mode='w') as f:
        f.write(s)
    print(s)
    # TODO: 書き出しに成功したことを伝えるポップアップ画面を作る。

    
def reset_text():
    text.delete('0.0', tk.END)

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
regis_button = tk.Button(text='書き出し', command=output_op)
regis_button.pack()

# reset_button
reset_button = tk.Button(text='リセット', command=reset_text)
reset_button.pack()

# # Entry
# EditBox = tk.Entry(width=40)
# # EditBox.insert(tk.END, "挿入する文字列")

# with open('./operation_sample.txt') as f:
#     for s_line in f:
#         # print(s_line)
#         EditBox.insert(tk.END, s_line)

# EditBox.pack()

update_position()  # 座標更新関数を初めて呼び出します

root.mainloop()