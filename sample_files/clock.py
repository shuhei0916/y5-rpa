import tkinter as tk
import time
# Tkinterのウィンドウを作成
root = tk.Tk()
root.title("Clock")
# 時計のラベルを作成
clock = tk.Label(root, font=("times", 50, "bold"))
clock.pack()
# 時計を更新する関数
def tick():
# 現在の日時を取得
    now = time.strftime("%H:%M:%S")
    # ラベルのテキストを更新
    clock.config(text=now)
    # 1000msごとに再度tick関数を呼び出す
    clock.after(1000, tick)
    
# 時計をスタート
tick()
root.mainloop()