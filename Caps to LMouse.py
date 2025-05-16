from pynput import mouse, keyboard
from time import sleep

pressed = True

def set_press(state):
    if state:
        m.press(mouse.Button.middle)
    else:
        m.release(mouse.Button.middle)
        

def on_press(key):
    global m, pressed
    if pressed and False:
        return
    if hasattr(key, "_name_"):
        if key._name_ == 'caps_lock' and not pressed:
            print("On")
            set_press(True)
            pressed = True
        elif key._name_ == 'esc':
            print("Off")            
            set_press(False)
            pressed = False
            
            
def on_release(key):
    global m, pressed
    if hasattr(key, "_name_"):
        if key._name_ == 'caps_lock':
            print("Off")
            set_press(False)
            pressed = False
        elif key._name_ == 'break':
            print("Off")
            set_press(False)
            pressed = False
            
def on_move(x,y):
    pass #print(f"{x}, {y}")
            
kb = keyboard.Listener(on_press=on_press, on_release=on_release)
m = mouse.Controller()
#m_l = mouse.Listener(on_move=on_move)




kb.start()
#m_l.start()

try:
    while True:
        sleep(0.001)
except:
    kb.join()