import tkinter
import pyautogui

def update_position():
    x, y = pyautogui.position()
    coord_text = 'x: ' + str(x) + ', y: ' + str(y)
    label.config(text=coord_text)
    root.after(100, update_position)  # 100ミリ秒ごとにupdate_position関数を再帰的に呼び出します

root = tkinter.Tk()
root.title("Dynamic Mouse Position Tracker")
root.geometry("400x300")

label = tkinter.Label(root)
label.pack()

update_position()  # 座標更新関数を初めて呼び出します

root.mainloop()