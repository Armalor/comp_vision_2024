import ctypes
import time

__all__ = ["key_down", "key_up", "SC_DOWN", "SC_UP", "SC_LEFT", "SC_RIGHT"]

SC_LEFT = (0x4B, True)
SC_RIGHT = (0x4D, True)
SC_UP = (0x48, True)
SC_DOWN = (0x50, True)

sendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput( ctypes.Structure ):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput( ctypes.Structure ):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def unpack_scan_code(scan_code):
    if not isinstance( scan_code, tuple ):
        return scan_code, 0
    else:
        return scan_code[0], 0x0001 if scan_code[1] else 0


def key_down(scan_code):
    extra = ctypes.c_ulong( 0 )
    ii_ = Input_I()
    code, ef = unpack_scan_code(scan_code)
    ii_.ki = KeyBdInput( 0, code, 0x0008 | ef, 0, ctypes.pointer( extra ) )
    x = Input(ctypes.c_ulong(1), ii_ )
    sendInput( 1, ctypes.pointer( x ), ctypes.sizeof( x ) )


def key_up(scan_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    code, ef = unpack_scan_code(scan_code)
    ii_.ki = KeyBdInput( 0, code, 0x0008 | 0x0002 | ef, 0, ctypes.pointer( extra ) )
    x = Input( ctypes.c_ulong( 1 ), ii_ )
    sendInput( 1, ctypes.pointer(x), ctypes.sizeof(x) )


def key_press(hexKeyCode, interval=0.02):
    key_down(hexKeyCode)
    time.sleep(interval)
    key_up(hexKeyCode)


if __name__ == '__main__':
    time.sleep(1)
    key_press(SC_LEFT)
    time.sleep(1)
    key_press(SC_RIGHT)
    time.sleep(1)
    key_press(SC_UP)
    time.sleep(1)
    key_press(SC_DOWN)
