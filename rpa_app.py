import datetime
import logging
import tkinter as tk
from tkinter import messagebox, ttk

import pyautogui

# from MCTest import readData, writeData
from common import *

logging.basicConfig(filename='log_rpa_app.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s', filemode='w')
# logging.disable(logging.CRITICAL)

def check_consistency():
    try:
        check_expiration()
    except:
        messagebox.showerror("Error", error_message)
        exit(1)

def update_cursor_position():
    x, y = pyautogui.position()
    coord_text = f'(x: {x:>4}, y: {y:>4})'
    st_bar.config(text=coord_text)
    root.after(100, update_cursor_position)

def update_plc_input():
    # plc_st, frame_num = readDate()
    plc_st = datetime.datetime.now() # TODO: シーケンサーの入力に置き換え
    plc_st_label.config(text=f'シーケンサ状態: {plc_st}')
    root.after(100, update_plc_input)
    
def save_command_list():
    logging.debug('save_command_list started!')
    output_path = './command_list.txt'
    try: 
        with open(output_path, mode='w') as f:
            for command in command_list:
                f.write(command + '\n')
        messagebox.showinfo('save_command_list success', f'保存に成功しました！\n保存先: {output_path}') # TODO: output_pathを絶対パスで表示する
        logging.debug('save_command_list ended successfully!')
    except Exception as e:
        messagebox.showerror('Error', f'コマンドリストの保存に失敗しました。\n{str(e)}')
        logging.error('save_command_list failed.')
    
def exe_command():
    check_consistency()
    root.withdraw()
    with open('./command_list.txt', 'r') as f:
        commands = f.readlines()
        for command in commands:
            command = command.strip()
            if "マウス移動" in command:
                args = command[5:].strip("()").split(", ") # "マウス移動(x, y)" から引数を抽出
                x, y = int(args[0]), int(args[1])
                pyautogui.moveTo(x, y, 0.5)
            elif "マウスクリック" in command:
                pyautogui.click()
            elif "文字列入力" in command:
                # frame_num ==  # strip系の処理する必要あり。
                pyautogui.typewrite('Hello\nWorld!\n', 0.25) # TODO: シーケンサーからの入力をここに含める
    root.deiconify()

def add_command():
    command = drop_down_list.get()
    if command:
        if command == 'マウス移動':
            item = f"{command}({x_spinbox.get()}, {y_spinbox.get()})"
        else:
            item = command
        command_list.append(item)
        command_listbox.insert(tk.END, item)

def remove_command():
    selection = command_listbox.curselection() # NOTE: selectionはタプルなので注意（複数選択している場合、タプルの要素数は複数になる。）
    if selection:
        selected_command = command_list[selection[0]]
        command_list.remove(selected_command) #WARNING: removeとdeleteの引数がそれぞれなんなのか、あんまり理解していないまま実装しているので注意
        command_listbox.delete(selection[0])

# drop_down_listの選択されたコマンドによって、spinboxのstateを変更
def on_command_change(event):
    selected_command = drop_down_list.get()
    if selected_command == 'マウス移動':
        x_spinbox.config(state="normal")
        y_spinbox.config(state="normal")
    else:
        x_spinbox.config(state="disabled")
        y_spinbox.config(state="disabled")


# 解像度の取得
x_size, y_size = pyautogui.size()
# assert isinstance(x_size, int)

root = tk.Tk()
root.title("Y5-OCR-RPA")
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

command_panel = tk.Frame(main_frame)
command_panel.pack()

values = ['マウス移動', 'マウスクリック', '文字列入力']
drop_down_list = ttk.Combobox(command_panel, state="readonly", values=values)
drop_down_list.pack(side=tk.LEFT, padx=(0, 10))
drop_down_list.bind("<<ComboboxSelected>>", on_command_change) # ????

spinboxes = tk.Frame(command_panel)
spinboxes.pack(side=tk.RIGHT)
x_label = tk.Label(spinboxes, text="x:")
x_label.pack(side=tk.LEFT)
x_spinbox = tk.Spinbox(spinboxes, from_=0, to=x_size, width=5, state="disabled")
x_spinbox.pack(side=tk.LEFT, padx=5)
y_label = tk.Label(spinboxes, text="y:")
y_label.pack(side=tk.LEFT)
y_spinbox = tk.Spinbox(spinboxes, from_=0, to=y_size, width=5, state="disabled")
y_spinbox.pack(side=tk.LEFT)

# ボタン用ウィジェット
buttons = tk.Frame(main_frame)

# 追加ボタン
add_button = tk.Button(buttons, text="▽追加▽", command=add_command)
add_button.pack(side=tk.LEFT, padx=10)

# 削除ボタン
remove_button = tk.Button(buttons, text="×削除×", command=remove_command)
remove_button.pack(side=tk.LEFT, padx=10)

# ボタン用ウィジェットをパック
buttons.pack(padx=10, pady=10)

# command_list表示用Text TODO: リファクタリングの余地ありそう
command_list = [] 
command_listbox = tk.Listbox(main_frame, height=7, width=40)
for item in command_list:
    command_listbox.insert(tk.END, item)
command_listbox.pack()


# 操作リストを書き出す用のボタン
regis_button = tk.Button(main_frame, text='保存', command=save_command_list)
regis_button.pack(pady=5)

# 自動操作開始ボタン(eキーだとうまくいかないので、ボタンで暫定的処理。最終的にはシーケンサの信号に置き換える予定)
start_auto_button = tk.Button (main_frame, text='自動操作開始(削除予定)', command=exe_command)
start_auto_button.pack()
# if plc_st == 1:
#     exe_command()

# シーケンサーの入力監視用ラベル
plc_st_label = tk.Label(main_frame)
plc_st_label.pack()
update_plc_input()

# st_bar（オプション引数についてはあんまりわかってないです）
st_bar = tk.Label(root, bd=1, relief=tk.SUNKEN, anchor=tk.E)
st_bar.pack(side=tk.BOTTOM, fill=tk.X)
update_cursor_position()  # 座標更新関数を初めて呼び出す


logging.debug("mainloop 1")
root.mainloop()
logging.debug("mainloop 2")