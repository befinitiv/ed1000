import atexit
import sys
import termios
import os

old_settings=None

def init_anykey():
	global old_settings
	try:
		old_settings = termios.tcgetattr(sys.stdin)
		new_settings = termios.tcgetattr(sys.stdin)
		new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
		new_settings[6][termios.VMIN] = 0  # cc
		new_settings[6][termios.VTIME] = 0 # cc
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)
	except:
		pass

@atexit.register
def term_anykey():
   global old_settings
   if old_settings:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def anykey():
   ch = os.read(sys.stdin.fileno(), 1)
   return ch;
