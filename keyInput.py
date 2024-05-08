import pyautogui
import keyboard

keyboard.wait('s')
pyautogui.click(100, 100)
pyautogui.typewrite('Hello\nWorld!\n', 0.25)