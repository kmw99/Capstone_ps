from pynput.keyboard import Key


def get_label_mapping():
    mapping = {
        "Space": " ", "Enter": Key.enter, "Tab": Key.tab, "Backspace": Key.backspace,
        "Caps Lock": Key.caps_lock, "left Shift": Key.shift, "right Shift": Key.shift_r,
        "left Ctrl": Key.ctrl, "right Ctrl": Key.ctrl_r, "left Alt": Key.alt, "right Alt": Key.alt_r,
        "left Win": Key.cmd, "right Win": Key.cmd_r, "Menu": Key.menu, "Tlide": "`",
        "Subtract": "-", "Add": "=", "Bracket1": "[", "Bracket2": "]",
        "Backslash": "\\", "Semi colon": ";", "Apostrophe": "'",
        "Comma": ",", "Period": ".", "Slash": "/"
    }
    for char in list("1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        mapping[char] = char
    return mapping