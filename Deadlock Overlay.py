import pygame
from os import environ

import win32api
import win32con
import win32gui

from pynput import mouse, keyboard

import ctypes

from message_gen import relevant_message
import functions as fn

class Overlay():
    def __init__(self):
        self.attempt_DPI_awareness()
        self.set_overlay_pos()
        self.load_settings()
        
        self.init_pygame()
        self.init_timer()
        self.init_pynput()
        
        self.def_flags()
        
        #Function-ify
        self.mouse_listener.start()
        self.keyboard_listener.start()
        #<end>
        
        self.loop_active = True
        self.main_loop()
    
    def attempt_DPI_awareness(self):
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
        print(awareness.value)
        print(errorCode)
        
        # Set DPI Awareness  (Windows 10 and 8)
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(True)
        print(errorCode)
               
    def set_overlay_pos(self):
        #os.environ
        environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        
    def load_settings(self):
        from config_parser import config as user_config
        self.wx, self.wy = user_config["Positions"]["screen_size_x"],user_config["Positions"]["screen_size_y"]
        
    def win32api_black_magic(self):
        #This code was mostly borrowed from some StackOverflow question. In short, it basically just makes the window invisible and somehow as a result allows passthrough.
        
        
        fuchsia = (255, 0, 128)  # Transparency color
        dark_red = (139, 0, 0)
        blue = (0, 0, 255)
        
        # Create layered window
        self.hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(self.hwnd, -1, 0,0,self.wx,self.wy, 2|1)
        
    def init_pygame(self):
        pygame.init()
        
        # Set display Size.
        self.screen = pygame.display.set_mode((self.wx,self.wy), pygame.NOFRAME) # For borderless, use pygame.NOFRAME
        
        # Init font object
        self.font = pygame.font.Font(None, 24)
        
    def init_timer(self):
        # Timer things
        self.clock = pygame.time.Clock()
        self.start = pygame.time.get_ticks()
        
        self.offset = 0
        self.unpaused = True
        
    def init_pynput(self):
        self.mouse_listener = mouse.Listener(on_scroll = self.on_mouse_scroll, on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press = self.key_pressed, on_release= self.key_released)
    
    def get_time(self):
        return (self.offset, pygame.time.get_ticks()-self.start)[self.unpaused]
        
    def key_pressed(self, key):
        #TODO
        pass
        
    def key_released(self, key):
        #TODO
        pass
    
    def on_mouse_scroll(self, mouse_position_x, mouse_position_y, scroll_x_change, scroll_y_change):
        self.mouse_pos = [mouse_position_x, mouse_position_y]
        
        #TODO
        global start, offset, modPressed
        start += scroll_y_change*-1000*modPressed
        offset += scroll_y_change*-1000*modPressed
    
    def on_click(self, mouse_position_x, mouse_position_y, button, was_pressed):
        self.mouse_pos = [mouse_position_x, mouse_position_y]
        
        if not self.interaction_modifier:
            return
        
        if button == pynput.Button.left and was_pressed:
            self.handle_click()
        
        
    def handle_click(self):
        pass
        #TODO
        
    
    def main_loop(self):
        while self.loop_active:
            pass


test = Overlay()

# Function Box
def isKeyPressed(key):
    #"if the high-order bit is 1, the key is down; otherwise, it is up."
    
    return (win32api.GetAsyncKeyState(key) & (1 << 15)) != 0



unpaused = True
Num1Pressed = False
Num3Pressed = False

showhud = True
active = False


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #Num0 96 for reset
    if isKeyPressed(user_config["Keys"]["timer_reset"]):
        start = pygame.time.get_ticks()
        
    #Num1 97 for pause/play
    if not isKeyPressed(user_config["Keys"]["timer_pause"]):
        Num1Pressed = False
    
    # Check that key has been unpressed, and state is currently unpaused
    if not Num1Pressed and unpaused and isKeyPressed(user_config["Keys"]["timer_pause"]):
        offset = current_time
        unpaused = False
        Num1Pressed = True
        
    if not Num1Pressed and not unpaused and isKeyPressed(user_config["Keys"]["timer_pause"]):
        start = pygame.time.get_ticks()-offset
        unpaused = True
        Num1Pressed = True
        
    #Num3 99 for toggle overlay
    if not isKeyPressed(user_config["Keys"]["overlay_hide"]):
        Num3Pressed = False
        
    if not Num3Pressed and isKeyPressed(user_config["Keys"]["overlay_hide"]):
        showhud = not showhud
        from config_parser import config as user_config
        
        Num3Pressed = True
        
    
    #Delete 46 for chording with scroll
    modPressed = isKeyPressed(user_config["Keys"]["scroll_activation"])
    
    #MMB 4 for something happened.
    

    screen.fill(fuchsia)  # Transparent background
    
    
    
    timer_obj = number_font.render(fn.formatms((offset, current_time)[unpaused]), False, (255,255,255))
    message_obj = number_font.render(relevant_message((offset, current_time)[unpaused]), False, (255,255,255))
    if showhud:
        pygame.draw.rect(screen, (dark_red, blue)[isKeyPressed(65)], pygame.Rect(wx-60, wy-60, 60, 60))
        screen.blit(timer_obj, (user_config["Positions"]["timer_x"], user_config["Positions"]["timer_y"]))
        screen.blit(message_obj, (user_config["Positions"]["message_x"], user_config["Positions"]["message_y"]))
    
    pygame.display.update()
    
    clock.tick(15)




