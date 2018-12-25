import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

import kb

# requires python3!

fs = 44100       # sampling rate, Hz, must be integer
baud = 50.0
duration = 1.0/baud   # in seconds, may be float
f0 = 500.0
f1 = 700.0


# (figures, code)

char2ccit =	{
  'a': (0, 0b00011),
  'b': (0, 0b11001),
  'c': (0, 0b01110),
  'd': (0, 0b01001),
  'e': (0, 0b00001),
  'f': (0, 0b01101),
  'g': (0, 0b11010),
  'h': (0, 0b10100),
  'i': (0, 0b00110),
  'j': (0, 0b01011),
  'k': (0, 0b01111),
  'l': (0, 0b10010),
  'm': (0, 0b11100),
  'n': (0, 0b01100),
  'o': (0, 0b11000),
  'p': (0, 0b10110),
  'q': (0, 0b10111),
  'r': (0, 0b01010),
  's': (0, 0b00101),
  't': (0, 0b10000),
  'u': (0, 0b00111),
  'v': (0, 0b11110),
  'w': (0, 0b10011),
  'x': (0, 0b11101),
  'y': (0, 0b10101),
  'z': (0, 0b10001),
 '\r': (0, 0b01000),
 '\n': (0, 0b00010),
  ' ': (0, 0b00100),
	'-': (1, 0b00011),
	'?': (1, 0b11001),
	':': (1, 0b01110),
	'3': (1, 0b00001),
	'8': (1, 0b00110),
	'(': (1, 0b01111),
	')': (1, 0b10010),
	'.': (1, 0b11100),
	',': (1, 0b01100),
	'9': (1, 0b11000),
	'0': (1, 0b10110),
	'1': (1, 0b10111),
	'4': (1, 0b01010),
 '\'': (1, 0b00101),
	'5': (1, 0b10000),
	'7': (1, 0b00111),
	'=': (1, 0b11110),
	'2': (1, 0b10011),
	'/': (1, 0b11101),
	'6': (1, 0b10101),
	'+': (1, 0b10001)
}

figletmap = {
	0 : 0b11111,
	1 : 0b11011
}

figstate = 0

def add_char(c):
	global figstate
	snd = []

	#check if char exists, otherwise transform it to ?
	try:
		fig, d = char2ccit[c]	
	except:
		fig, d = char2ccit['?']

	if fig != figstate:
		snd.append(add_data(figletmap[fig]))
		figstate = fig

	snd.append(add_data(d))

	# add an extra CR after newline (doesnt hurt for dos, required for unix)
	if c == '\n':
		fig, d = char2ccit['\r']
		snd.append(add_data(d))

	return np.concatenate(snd)

def add_data(d):
	#start bit
	snd = [samples0]
	for i in range(0,6):
		if (d & (1 << i)) == 0:
			snd.append(samples0)
		else:
			snd.append(samples1)
	
	#stop bit
	snd.extend([samples1, samples1])

	return np.concatenate(snd)

# samples0 ^= logic low, samples1 ^= logic high (length 1 bit)
samples0 = (np.sin(2*np.pi*np.arange(fs*duration)*f0/fs)).astype(np.float32)
samples1 = (np.sin(2*np.pi*np.arange(fs*duration)*f1/fs)).astype(np.float32)

# enable char by char stdin reading
kb.init_anykey()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)

# starting tone
for i in range(0,int(2.0*baud)):
	stream.write(samples1, len(samples1))

while True:
	key = kb.anykey()
	if key != b'':
		c = chr(key[0])
		snd = add_char(c)
		stream.write(snd, len(snd))
		sys.stdout.write(c)
		sys.stdout.flush()
	else:
		stream.write(samples1, len(samples1))
			
stream.stop_stream()
stream.close()

p.terminate()


