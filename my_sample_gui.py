import tkinter as tk

# ウィンドウの作成
root = tk.Tk()
root.title("Harvest Overlay Ver.0.20")

# フレームの作成とレイアウトの設定
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# ラベルの作成とテキストの設定
name_label = tk.Label(main_frame, text="▽名前を入力してください▽")
name_label.pack()

# エントリーボックスの作成
name_entry = tk.Entry(main_frame)
name_entry.pack()

# リストボックスの作成と選択の管理
item_list = ["test1", "test2", "test3", "test4", "test5"]
selected_items = tk.Variable(value=["test4"])
list_box = tk.Listbox(main_frame, listvariable=selected_items)
list_box.pack()

# ボタンの作成と機能の実装
def add_item():
    new_item = name_entry.get()
    if new_item:
        item_list.append(new_item)
        name_entry.delete(0, tk.END)
        list_box.insert(tk.END, new_item)

def remove_item():
    selection = list_box.curselection()
    if selection:
        item = selected_items.get()[selection[0]]
        item_list.remove(item)
        list_box.delete(selection[0])

add_button = tk.Button(main_frame, text="▽追加▽", command=add_item)
add_button.pack(side=tk.LEFT)

remove_button = tk.Button(main_frame, text="×削除×", command=remove_item)
remove_button.pack(side=tk.LEFT)

# メインループの開始
root.mainloop()