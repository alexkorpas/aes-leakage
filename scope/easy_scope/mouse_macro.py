import pyautogui as pyautogui


def stop_macro():
    pyautogui.hotkey('ctrl', 'f6')


def start_macro():
    pyautogui.hotkey('ctrl', 'f11')
