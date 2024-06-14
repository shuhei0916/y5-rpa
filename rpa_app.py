# TODO: pyarmor。stimerの設置。


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyautogui
import datetime
import keyboard


# マウス座標の更新を行う関数
def update_position():
    x, y = pyautogui.position()
    coord_text = f'(x: {x:>4}, y: {y:>4})'
    st_bar.config(text=coord_text)
    root.after(100, update_position)


# シーケンサーの入力の更新を行う関数
def update_plcinput():
    plc_st = datetime.datetime.now() # # TODO: シーケンサーの入力に置き換え
    plc_st_label.config(text=f'シーケンサ状態: {plc_st}')
    root.after(100, update_plcinput)
    
    
# 操作リストの出力を行う関数
def save_command_list():
    output_path = './command_list.txt'
    try: 
        with open(output_path, mode='w') as f:
            for command in command_list:
                    f.write(command + '\n')
        messagebox.showinfo('save_command_list success', f'保存に成功しました！\n保存先: {output_path}') # TODO: output_pathを絶対パスで表示する
    except Exception as e:
        messagebox.showerror('Error', f'コマンドリストの保存に失敗しました。\n{str(e)}')

# def execute_commands(execution_window):
#     try:
#         with open('./command_list.txt', 'r') as f:
#             commands = f.readlines()
#             for command in commands:
#                 command = command.strip()
#                 if "マウス移動" in command:
#                     args = command[5:].strip("()").split(", ")
#                     x, y = int(args[0]), int(args[1])
#                     pyautogui.moveTo(x, y)
#                 elif "マウスクリック" in command:
#                     pyautogui.click()
#                 elif "文字列入力" in command:
#                     pyautogui.typewrite('Hello\nWorld!\n', 0.25)
#                 if keyboard.is_pressed('esc'):
#                     raise KeyboardInterrupt
#         root.after(100, lambda: execute_commands(execution_window))  # 繰り返し実行するために再帰的に呼び出す
#     except KeyboardInterrupt:
#         execution_window.destroy()
#         root.deiconify()

# def exe_command():
#     root.withdraw()  # メイン画面を一時的に閉じる
#     execution_window = tk.Toplevel(root)
#     execution_window.title("実行中")
#     tk.Label(execution_window, text="コマンド実行中... ESCキー長押しで停止します。").pack(padx=20, pady=20)
#     execution_window.geometry("300x100+20+900")# 画面左下に配置
    
#     root.after(100, lambda: execute_commands(execution_window))
    
    
# TODO: 実行中であることをしめすmessageboxを作る（メイン画面はその間とじる）
def exe_command():
    # messagebox.showinfo("command executed!!")
    with open('./command_list.txt', 'r') as f:
        commands = f.readlines()
        for command in commands:
            command = command.strip() # NOTE: 不要かも？
            if "マウス移動" in command:
                # "マウス移動(x, y)" から引数を抽出
                args = command[5:].strip("()").split(", ")
                x, y = int(args[0]), int(args[1])
                pyautogui.moveTo(x, y)
            elif "マウスクリック" in command:
                pyautogui.click()
            elif "文字列入力" in command:
                pyautogui.typewrite('Hello\nWorld!\n', 0.25) # TODO: シーケンサーからの入力をここに含める

# drop_down_listからcommand_listboxにコマンドを追加
def add_command():
    command = drop_down_list.get()
    if command:
        # マウス移動の場合は、目的地の座標も含める。
        if command == 'マウス移動':
            item = command + '(' + x_spinbox.get() + ', ' + y_spinbox.get() + ')'
            command_list.append(item)
            command_listbox.insert(tk.END, item) 
        else:
            command_list.append(command)            
            command_listbox.insert(tk.END, command)

# command_listboxから選択したコマンドを削除
def remove_command():
    selection = command_listbox.curselection() # selectionはタプルなので注意（複数選択している場合、タプルの要素数は複数になる。）
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

# シーケンサーの入力監視用ラベル
plc_st_label = tk.Label(main_frame)
plc_st_label.pack()
update_plcinput()

# st_bar（オプション引数についてはあんまりわかってないです）
st_bar = tk.Label(root, bd=1, relief=tk.SUNKEN, anchor=tk.E)
st_bar.pack(side=tk.BOTTOM, fill=tk.X)
update_position()  # 座標更新関数を初めて呼び出す


root.mainloop()

