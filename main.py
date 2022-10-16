from typing import List



import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import string
from pynput import keyboard
from pynput.keyboard import Listener, Key
import time
import glob
import functools

printable = string.ascii_letters + string.digits + string.punctuation + ' '
control_char_to_key = {
    "'\\x01'": 'a',
    "'\\x02'": 'b',
    "'\\x03'": 'c',
    "'\\x04'": 'd',
    "'\\x05'": 'e',
    "'\\x06'": 'f',
    "'\\x07'": 'g', 
    "'\\x08'": 'h',
    "'\\x09'": 'i',
    "'\\x0a'": 'j',
    "'\\x0b'": 'k',
    "'\\x0c'": 'l',
    "'\\x0d'": 'm',
    "'\\x0e'": 'n',
    "'\\x0f'": 'o',
    "'\\x10'": 'p',
    "'\\x11'": 'q',
    "'\\x12'": 'r',
    "'\\x13'": 's',
    "'\\x14'": 't',
    "'\\x15'": 'u',
    "'\\x16'": 'v',
    "'\\x17'": 'w',
    "'\\x18'": 'x',
    "'\\x19'": 'y',
    "'\\x1a'": 'z',
    49: '1',
    50: '2',
    51: '3',
    52: '4',
    53: '5',
    54: '6',
    55: '7',
    56: '8',
    57: '9',
    58: '0',
}

def get_current_time_ms():
    return round(time.time() * 1000)

class Main:
    def __init__(self):
        self.last_event_time_ms = get_current_time_ms()
        self.f = open("output.txt", "a")

    def appendlog(self, string):
        self.f.write(string + "\n")

    def key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = str(key)
        actual_key = None
        if type(key).__name__ == 'KeyCode':
            actual_key = control_char_to_key.get(repr(key.char), None)
            if not actual_key and key.vk:
                actual_key = control_char_to_key.get(key.vk, None)
        
        if not actual_key:
            actual_key = current_key
        
        current_time = get_current_time_ms()
        print(f"Press,{actual_key},{current_time - self.last_event_time_ms}")
        self.appendlog(f"Press,{actual_key},{current_time - self.last_event_time_ms}")
        self.last_event_time_ms = current_time
    
    def key_release(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = str(key)

        actual_key = None
        if type(key).__name__ == 'KeyCode':
            actual_key = control_char_to_key.get(repr(key.char), None)
        
        if not actual_key:
            actual_key = current_key
        
        if key == Key.pause:
            self.appendlog("======================================================")
            self.f.close()
            exit()
        
        current_time = get_current_time_ms()
        print(f"Release,{actual_key},{current_time - self.last_event_time_ms}")
        self.appendlog(f"Release,{actual_key},{current_time - self.last_event_time_ms}")
        self.last_event_time_ms = current_time


    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.key_press, on_release=self.key_release)
        with keyboard_listener:
            keyboard_listener.join()

main = Main()
main.run()