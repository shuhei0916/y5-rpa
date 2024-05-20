# 操作リストに基づいてマウスを動かす。
# TODO: 自動操作開始後、escキーの入力でループを抜けるようにする
# TODO: シーケンサーの入力を表示し、更新し続ける関数を作る。
# TODO: pyarmorによる難読化。stimerの設置。


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyautogui

# マウス座標の更新を行う関数
def update_position():
    x, y = pyautogui.position()
    coord_text = f'マウス座標(x, y): ({x}, {y})'
    st_bar.config(text=coord_text)
    root.after(100, update_position)

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

# TODO: 実行中であることをしめすmessageboxを作る（メイン画面はその間とじる）
# TODO: 無限ループにし、ESCで抜ける
# TODO: テキストコマンド -> pyautoguiの関数への変換
def exe_command():
    # messagebox.showinfo("command executed!!")
    try: # TODO: このtry-except文いる？（with openしてるから要らない気もする）
        with open('./command_list.txt', 'r') as f:
            commands = f.readlines()
            for command in commands:
                # command = command.strip() # 前後の空白除く
                if "マウス移動" in command:
                    pyautogui.moveTo(100, 200) # 暫定的処理。引数を含める
                elif "マウスクリック" in command:
                    pyautogui.click()
                elif "文字列入力" in command:pyautogui.typewrite('Hello\nWorld!\n', 0.25) # TODO: シーケンサーからの入力をここに含める
    except Exception as e:
        messagebox.showinfo("Error exectution commands: ", e)

# command_cboxからcommand_listboxにコマンドを追加
def add_command():
    new_item = command_cbox.get()
    if new_item:
        # マウス移動の場合は、目的地の座標も含める。
        if new_item == 'マウス移動': # TODO: item -> commandに命名を変更する
            item = new_item + '(' + x_spinbox.get() + ', ' + y_spinbox.get() + ')'
            command_list.append(item)
            command_listbox.insert(tk.END, item) 
        else:
            command_list.append(new_item)            
            command_listbox.insert(tk.END, new_item)

# command_listboxから選択したコマンドを削除
def remove_command():
    selection = command_listbox.curselection() # selectionはタプルなので注意（複数選択している場合、タプルの要素数は複数になる。）
    if selection:
        selected_command = command_list[selection[0]]
        command_list.remove(selected_command) #WARNING: removeとdeleteの引数がそれぞれなんなのか、あんまり理解していないまま実装しているので注意
        command_listbox.delete(selection[0])

# command_cboxの選択されたコマンドによって、spinboxのstateを変更
def on_command_change(event):
    selected_command = command_cbox.get()
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
command_cbox = ttk.Combobox(command_panel, state="readonly", values=values)
command_cbox.pack(side=tk.LEFT, padx=(0, 10))
command_cbox.bind("<<ComboboxSelected>>", on_command_change) # ????

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

# st_bar（オプション引数についてはあんまりわかってないです）
st_bar = tk.Label(root, bd=1, relief=tk.SUNKEN, anchor=tk.E)
st_bar.pack(side=tk.BOTTOM, fill=tk.X)

update_position()  # 座標更新関数を初めて呼び出す

root.mainloop()

