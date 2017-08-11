import sys
import ctypes

def reset():
    """This is a super hacky way to reload /etc/resolv.conf.  It seems
    necessary when you switch wifi networks on the go."""
    if sys.platform.startswith('linux'):
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        res_init = libc.__res_init
        res_init()
