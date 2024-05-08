import pyautogui
import keyboard

def main():
    keyboard.wait('s')  # 's' キーが押されるのを待つ
    pyautogui.moveRel(100, 0, duration=0.25)
    pyautogui.moveRel(0, 100, duration=0.25)
    pyautogui.moveRel(-100, 0, duration=0.25)
    pyautogui.moveRel(0, -100, duration=0.25)

if __name__ == '__main__':
    main()
