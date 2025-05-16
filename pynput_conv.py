import pygame
from pynput import keyboard

def key_handler(key):
    
    if hasattr(key, "char") and key.char != None:
        return {key.vk:key.char}
    if hasattr(key, "char") and key.char == None:
        if 96 <= key.vk and key.vk <= 105:
            return {key.vk:f"Num{key.vk-96}"}
        return {key.vk:key.__dict__}
    if hasattr(key, "_name_"):
        return {key._sort_order_:key._name_}
    
    
def on_press(key):
    global key_dict
    key_dict = key_dict | result if (result := key_handler(key)) != None else key_dict 
    
    print(key_dict)
    
    
    
def sort_dict(dic):
    return {i[0]:i[1] for i in sorted(dic.items(), key = lambda x: x[0])}
        
def num(key):
    print("-", key)
    if key == None:
        return 0
    if hasattr(key, "vk"):
        return key.vk
    if hasattr(key, "_sort_order_"):
        return key._sort_order_
    
key_dict = {}
kb = keyboard.Listener(on_press = on_press)
kb.start()

while True:
    pass