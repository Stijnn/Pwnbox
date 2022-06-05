from enum import Enum

USB_CHARACTER_TRANSLATION_KEYCODES = {
    'a': [False, 4], 
    'A': [True, 4], 
    'b': [False, 5], 
    'B': [True, 5], 
    'c': [False, 6], 
    'C': [True, 6], 
    'd': [False, 7], 
    'D': [True, 7], 
    'e': [False, 8], 
    'E': [True, 8], 
    'f': [False, 9], 
    'F': [True, 9], 
    'g': [False, 10], 
    'G': [True, 10], 
    'h': [False, 11], 
    'H': [True, 11], 
    'i': [False, 12], 
    'I': [True, 12], 
    'j': [False, 13], 
    'J': [True, 13], 
    'k': [False, 14], 
    'K': [True, 14], 
    'l': [False, 15], 
    'L': [True, 15], 
    'm': [False, 16], 
    'M': [True, 16], 
    'n': [False, 17], 
    'N': [True, 17], 
    'o': [False, 18], 
    'O': [True, 18], 
    'p': [False, 19], 
    'P': [True, 19], 
    'q': [False, 20], 
    'Q': [True, 20], 
    'r': [False, 21], 
    'R': [True, 21], 
    's': [False, 22], 
    'S': [True, 22], 
    't': [False, 23], 
    'T': [True, 23], 
    'u': [False, 24], 
    'U': [True, 24], 
    'v': [False, 25], 
    'V': [True, 25], 
    'w': [False, 26], 
    'W': [True, 26], 
    'x': [False, 27], 
    'X': [True, 27], 
    'y': [False, 28], 
    'Y': [True, 28], 
    'z': [False, 29], 
    'Z': [True, 29],
    '1': [False, 30], 
    '2': [False, 31], 
    '3': [False, 32], 
    '4': [False, 33], 
    '5': [False, 34], 
    '6': [False, 35], 
    '7': [False, 36], 
    '8': [False, 37], 
    '9': [False, 38],
    '0': [False, 39],
    '!': [True, 30], 
    '@': [True, 31], 
    '#': [True, 32], 
    '$': [True, 33], 
    '%': [True, 34], 
    '^': [True, 35], 
    '&': [True, 36], 
    '*': [True, 37], 
    '(': [True, 38], 
    ')': [True, 39], 

    '-': [False, 45], 
    '_': [True, 45],
    '=': [False, 46], 
    '+': [True, 46],
    '[': [False, 47], 
    '{': [True, 47],
    ']': [False, 48], 
    '}': [True, 48],
    '\\': [False, 49], 
    '|': [True, 49],

    ';': [False, 51], 
    ':': [True, 51],
    '\'': [False, 52], 
    '"': [True, 52],
    '`': [False, 53], 
    '~': [True, 53],
    ',': [False, 54], 
    '<': [True, 54],
    '.': [False, 55], 
    '>': [True, 55],
    '/': [False, 56], 
    '?': [True, 56],
     
    ' ': [False, 0x2c],
}


KEY_MOD_LCTRL  =  chr(0x01)
KEY_MOD_LSHIFT =  chr(0x02)
KEY_MOD_LALT   =  chr(0x04)
KEY_MOD_LMETA  =  chr(0x08)
KEY_MOD_RCTRL  =  chr(0x10)
KEY_MOD_RSHIFT =  chr(0x20)
KEY_MOD_RALT   =  chr(0x40)
KEY_MOD_RMETA  =  chr(0x80)

KEY_NONE =  chr(0x00)
KEY_ERR_OVF =  chr(0x01)
KEY_A =  chr(0x04) #  Keyboard a and A
KEY_B =  chr(0x05) #  Keyboard b and B
KEY_C =  chr(0x06) #  Keyboard c and C
KEY_D =  chr(0x07) #  Keyboard d and D
KEY_E =  chr(0x08) #  Keyboard e and E
KEY_F =  chr(0x09) #  Keyboard f and F
KEY_G =  chr(0x0a) #  Keyboard g and G
KEY_H =  chr(0x0b) #  Keyboard h and H
KEY_I =  chr(0x0c) #  Keyboard i and I
KEY_J =  chr(0x0d) #  Keyboard j and J
KEY_K =  chr(0x0e) #  Keyboard k and K
KEY_L =  chr(0x0f) #  Keyboard l and L
KEY_M =  chr(0x10) #  Keyboard m and M
KEY_N =  chr(0x11) #  Keyboard n and N
KEY_O =  chr(0x12) #  Keyboard o and O
KEY_P =  chr(0x13) #  Keyboard p and P
KEY_Q =  chr(0x14) #  Keyboard q and Q
KEY_R =  chr(0x15) #  Keyboard r and R
KEY_S =  chr(0x16) #  Keyboard s and S
KEY_T =  chr(0x17) #  Keyboard t and T
KEY_U =  chr(0x18) #  Keyboard u and U
KEY_V =  chr(0x19) #  Keyboard v and V
KEY_W =  chr(0x1a) #  Keyboard w and W
KEY_X =  chr(0x1b) #  Keyboard x and X
KEY_Y =  chr(0x1c) #  Keyboard y and Y
KEY_Z =  chr(0x1d) #  Keyboard z and Z
KEY_1 =  chr(0x1e) #  Keyboard 1 and !
KEY_2 =  chr(0x1f) #  Keyboard 2 and @
KEY_3 =  chr(0x20) #  Keyboard 3 and #
KEY_4 =  chr(0x21) #  Keyboard 4 and $
KEY_5 =  chr(0x22) #  Keyboard 5 and %
KEY_6 =  chr(0x23) #  Keyboard 6 and ^
KEY_7 =  chr(0x24) #  Keyboard 7 and &
KEY_8 =  chr(0x25) #  Keyboard 8 and *
KEY_9 =  chr(0x26) #  Keyboard 9 and (
KEY_0 =  chr(0x27) #  Keyboard 0 and )
KEY_ENTER =  chr(0x28) #  Keyboard Return (ENTER)
KEY_ESC =  chr(0x29) #  Keyboard ESCAPE
KEY_BACKSPACE =  chr(0x2a) #  Keyboard DELETE (Backspace)
KEY_TAB =  chr(0x2b) #  Keyboard Tab
KEY_SPACE =  chr(0x2c) #  Keyboard Spacebar
KEY_MINUS =  chr(0x2d) #  Keyboard - and _
KEY_EQUAL =  chr(0x2e) #  Keyboard = and +
KEY_LEFTBRACE =  chr(0x2f) #  Keyboard [ and {
KEY_RIGHTBRACE =  chr(0x30) #  Keyboard ] and }
KEY_BACKSLASH =  chr(0x31) #  Keyboard \ and |
KEY_HASHTILDE =  chr(0x32) #  Keyboard Non-US # and ~
KEY_SEMICOLON =  chr(0x33) #  Keyboard ; and :
KEY_APOSTROPHE =  chr(0x34) #  Keyboard ' and "
KEY_GRAVE =  chr(0x35) #  Keyboard ` and ~
KEY_COMMA =  chr(0x36) #  Keyboard , and <
KEY_DOT =  chr(0x37) #  Keyboard . and >
KEY_SLASH =  chr(0x38) #  Keyboard / and ?
KEY_CAPSLOCK =  chr(0x39) #  Keyboard Caps Lock
KEY_F1 =  chr(0x3a) #  Keyboard F1
KEY_F2 =  chr(0x3b) #  Keyboard F2
KEY_F3 =  chr(0x3c) #  Keyboard F3
KEY_F4 =  chr(0x3d) #  Keyboard F4
KEY_F5 =  chr(0x3e) #  Keyboard F5
KEY_F6 =  chr(0x3f) #  Keyboard F6
KEY_F7 =  chr(0x40) #  Keyboard F7
KEY_F8 =  chr(0x41) #  Keyboard F8
KEY_F9 =  chr(0x42) #  Keyboard F9
KEY_F10 =  chr(0x43) #  Keyboard F10
KEY_F11 =  chr(0x44) #  Keyboard F11
KEY_F12 =  chr(0x45) #  Keyboard F12
KEY_SYSRQ =  chr(0x46) #  Keyboard Print Screen
KEY_SCROLLLOCK =  chr(0x47) #  Keyboard Scroll Lock
KEY_PAUSE =  chr(0x48) #  Keyboard Pause
KEY_INSERT =  chr(0x49) #  Keyboard Insert
KEY_HOME =  chr(0x4a) #  Keyboard Home
KEY_PAGEUP =  chr(0x4b) #  Keyboard Page Up
KEY_DELETE =  chr(0x4c) #  Keyboard Delete Forward
KEY_END =  chr(0x4d) #  Keyboard End
KEY_PAGEDOWN =  chr(0x4e) #  Keyboard Page Down
KEY_RIGHT =  chr(0x4f) #  Keyboard Right Arrow
KEY_LEFT =  chr(0x50) #  Keyboard Left Arrow
KEY_DOWN =  chr(0x51) #  Keyboard Down Arrow
KEY_UP =  chr(0x52) #  Keyboard Up Arrow
KEY_NUMLOCK =  chr(0x53) #  Keyboard Num Lock and Clear
KEY_KPSLASH =  chr(0x54) #  Keypad /
KEY_KPASTERISK =  chr(0x55) #  Keypad *
KEY_KPMINUS =  chr(0x56) #  Keypad -
KEY_KPPLUS =  chr(0x57) #  Keypad +
KEY_KPENTER =  chr(0x58) #  Keypad ENTER
KEY_KP1 =  chr(0x59) #  Keypad 1 and End
KEY_KP2 =  chr(0x5a) #  Keypad 2 and Down Arrow
KEY_KP3 =  chr(0x5b) #  Keypad 3 and PageDn
KEY_KP4 =  chr(0x5c) #  Keypad 4 and Left Arrow
KEY_KP5 =  chr(0x5d) #  Keypad 5
KEY_KP6 =  chr(0x5e) #  Keypad 6 and Right Arrow
KEY_KP7 =  chr(0x5f) #  Keypad 7 and Home
KEY_KP8 =  chr(0x60) #  Keypad 8 and Up Arrow
KEY_KP9 =  chr(0x61) #  Keypad 9 and Page Up
KEY_KP0 =  chr(0x62) #  Keypad 0 and Insert
KEY_KPDOT =  chr(0x63) #  Keypad . and Delete
KEY_102ND =  chr(0x64) #  Keyboard Non-US \ and |
KEY_COMPOSE =  chr(0x65) #  Keyboard Application
KEY_POWER =  chr(0x66) #  Keyboard Power
KEY_KPEQUAL =  chr(0x67) #  Keypad =
KEY_F13 =  chr(0x68) #  Keyboard F13
KEY_F14 =  chr(0x69) #  Keyboard F14
KEY_F15 =  chr(0x6a) #  Keyboard F15
KEY_F16 =  chr(0x6b) #  Keyboard F16
KEY_F17 =  chr(0x6c) #  Keyboard F17
KEY_F18 =  chr(0x6d) #  Keyboard F18
KEY_F19 =  chr(0x6e) #  Keyboard F19
KEY_F20 =  chr(0x6f) #  Keyboard F20
KEY_F21 =  chr(0x70) #  Keyboard F21
KEY_F22 =  chr(0x71) #  Keyboard F22
KEY_F23 =  chr(0x72) #  Keyboard F23
KEY_F24 =  chr(0x73) #  Keyboard F24
KEY_OPEN =  chr(0x74) #  Keyboard Execute
KEY_HELP =  chr(0x75) #  Keyboard Help
KEY_PROPS =  chr(0x76) #  Keyboard Menu
KEY_FRONT =  chr(0x77) #  Keyboard Select
KEY_STOP =  chr(0x78) #  Keyboard Stop
KEY_AGAIN =  chr(0x79) #  Keyboard Again
KEY_UNDO =  chr(0x7a) #  Keyboard Undo
KEY_CUT =  chr(0x7b) #  Keyboard Cut
KEY_COPY =  chr(0x7c) #  Keyboard Copy
KEY_PASTE =  chr(0x7d) #  Keyboard Paste
KEY_FIND =  chr(0x7e) #  Keyboard Find
KEY_MUTE =  chr(0x7f) #  Keyboard Mute
KEY_VOLUMEUP =  chr(0x80) #  Keyboard Volume Up
KEY_VOLUMEDOWN =  chr(0x81) #  Keyboard Volume Down
KEY_KPCOMMA =  chr(0x85) #  Keypad Comma
KEY_RO =  chr(0x87) #  Keyboard International1
KEY_KATAKANAHIRAGANA =  chr(0x88) #  Keyboard International2
KEY_YEN =  chr(0x89) #  Keyboard International3
KEY_HENKAN =  chr(0x8a) #  Keyboard International4
KEY_MUHENKAN =  chr(0x8b) #  Keyboard International5
KEY_KPJPCOMMA =  chr(0x8c) #  Keyboard International6
KEY_HANGEUL =  chr(0x90) #  Keyboard LANG1
KEY_HANJA =  chr(0x91) #  Keyboard LANG2
KEY_KATAKANA =  chr(0x92) #  Keyboard LANG3
KEY_HIRAGANA =  chr(0x93) #  Keyboard LANG4
KEY_ZENKAKUHANKAKU =  chr(0x94) #  Keyboard LANG5
KEY_KPLEFTPAREN =  chr(0xb6) #  Keypad (
KEY_KPRIGHTPAREN =  chr(0xb7) #  Keypad )
KEY_LEFTCTRL =  chr(0xe0) #  Keyboard Left Control
KEY_LEFTSHIFT =  chr(0xe1) #  Keyboard Left Shift
KEY_LEFTALT =  chr(0xe2) #  Keyboard Left Alt
KEY_LEFTMETA =  chr(0xe3) #  Keyboard Left GUI
KEY_RIGHTCTRL =  chr(0xe4) #  Keyboard Right Control
KEY_RIGHTSHIFT =  chr(0xe5) #  Keyboard Right Shift
KEY_RIGHTALT =  chr(0xe6) #  Keyboard Right Alt
KEY_RIGHTMETA =  chr(0xe7) #  Keyboard Right GUI
KEY_MEDIA_PLAYPAUSE =  chr(0xe8)
KEY_MEDIA_STOPCD =  chr(0xe9)
KEY_MEDIA_PREVIOUSSONG =  chr(0xea)
KEY_MEDIA_NEXTSONG =  chr(0xeb)
KEY_MEDIA_EJECTCD =  chr(0xec)
KEY_MEDIA_VOLUMEUP =  chr(0xed)
KEY_MEDIA_VOLUMEDOWN =  chr(0xee)
KEY_MEDIA_MUTE =  chr(0xef)
KEY_MEDIA_WWW =  chr(0xf0)
KEY_MEDIA_BACK =  chr(0xf1)
KEY_MEDIA_FORWARD =  chr(0xf2)
KEY_MEDIA_STOP =  chr(0xf3)
KEY_MEDIA_FIND =  chr(0xf4)
KEY_MEDIA_SCROLLUP =  chr(0xf5)
KEY_MEDIA_SCROLLDOWN =  chr(0xf6)
KEY_MEDIA_EDIT =  chr(0xf7)
KEY_MEDIA_SLEEP =  chr(0xf8)
KEY_MEDIA_COFFEE =  chr(0xf9)
KEY_MEDIA_REFRESH =  chr(0xfa)
KEY_MEDIA_CALC =  chr(0xfb)