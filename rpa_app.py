# 操作リストに基づいてマウスを動かす。
# TODO: 自動操作開始後、escキーの入力でループを抜けるようにする
# TODO: シーケンサーの入力を表示し、更新し続ける関数を作る。
# TODO: エントリーボックスを編集し、より分かりやすいUIにする（ラジオボックス？を使うなど）
# TODO: リファクタリング：
#       名前をわかりやすく変更　操作リスト　-> op_listにする??or command_list?
# TODO: pyarmorによる難読化。stimerの設置。


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyautogui

# マウス座標の更新を行う関数
def update_position():
    x, y = pyautogui.position()
    coord_text = 'マウス座標: x: ' + str(x) + ', y: ' + str(y)
    pos_label.config(text=coord_text)
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


def exe_command():
    # messagebox.showinfo("command executed!!")
    try:
        with open('./command_list.txt', 'r') as f:
            commands = f.readlines()
            # messagebox.showinfo('hehe', commands)
            for command in commands:
                exec(command.strip()) # WARNING: exec関数の使用には注意が必要
                # print(command.strip())
    except Exception as e:
        messagebox.showinfo("Error exectution operations: ", e, commands)


def add_command():
    new_item = command_cbox.get()
    if new_item:
        command_list.append(new_item)
        # command_cbox.delete(0, tk.END)
        command_listbox.insert(tk.END, new_item)

def remove_command():
    selection = command_listbox.curselection() # selectionはタプルなので注意（複数選択している場合、タプルの要素数は複数になる。）
    if selection:
        selected_command = command_list[selection[0]]
        command_list.remove(selected_command) #WARNING: removeとdeleteの引数がそれぞれなんなのか、あんまり理解していないまま実装しているので注意
        command_listbox.delete(selection[0])

root = tk.Tk()
root.title("Y5-OCR-RPA")

# フレームの作成とレイアウトの設定
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# マウス座標表示用Label
pos_label = tk.Label(main_frame)
pos_label.pack()

# Commandを選択するためのComboBox
values = ['マウス移動', 'マウスクリック', '文字列入力']
command_cbox = ttk.Combobox(main_frame, state="readonly", values=values)
command_cbox.pack()


# マウス座標設定用SpinBox TODO: y座標のぶんのspinboxも同様に定義し、配置を変える。
s = tk.Spinbox(main_frame)
s.pack()

# ボタン用ウィジェット
buttons = tk.Frame(main_frame)


# 追加ボタン
add_button = tk.Button(buttons, text="▽追加▽", command=add_command)
add_button.pack(side=tk.LEFT)

# 削除ボタン
remove_button = tk.Button(buttons, text="×削除×", command=remove_command)
remove_button.pack(side=tk.LEFT)

# ボタン用ウィジェットをパック
buttons.pack()

# label
instruction_label = tk.Label(main_frame, text='Command List: ')
instruction_label.pack()

# command_list表示用Text TODO: リファクタリングの余地ありそう
command_list = [] 
command_listbox = tk.Listbox(main_frame, height=7, width=30)
for item in command_list:
    command_listbox.insert(tk.END, item)
command_listbox.pack()


# 操作リストを書き出す用のボタン
regis_button = tk.Button(main_frame, text='書き出し', command=save_command_list)
regis_button.pack()

# 自動操作開始ボタン(eキーだとうまくいかないので、ボタンで暫定的処理。最終的にはシーケンサの信号に置き換える予定)
start_auto_button = tk.Button (main_frame, text='自動操作開始', command=exe_command)
start_auto_button.pack()


# main_frame.bind('<e>', lambda event: execute_operations())

update_position()  # 座標更新関数を初めて呼び出す

root.mainloop()

