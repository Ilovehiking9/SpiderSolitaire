import pyautogui

def get_cursor_position():
    # Get the current cursor position
    x, y = pyautogui.position()
    return x, y

if __name__ == "__main__":
    try:
        while True:
            x, y = get_cursor_position()
            print(f"Cursor Position: X={x}, Y={y}")
    except KeyboardInterrupt:
        print("\nExiting...")