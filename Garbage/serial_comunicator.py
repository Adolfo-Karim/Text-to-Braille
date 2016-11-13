#serial_comunicator.py
import serial
import time

class Terminal (object):
	def __init__(self,COM_port, baud_rate = 9600, byte_size = 8,
	 parity = 'N', stop_bits = 1, name = "default"):
		#Opens a 9600baud,8bit,N,1 serial port at the specified port
		self.ser = serial.Serial()
		self.ser.port = COM_port
		self.ser.baudrate = baud_rate
		self.ser.bytesize = byte_size
		self.ser.parity = parity
		self.ser.stop_bits = stop_bits
		self.ser.open()

	def writeMessage(self,bytes, EOL=''):
		self.ser.write(bytes)

	def termLoop(self):
		user_in = ""
		while user_in != "exit":
			user_in = input("Welcome, terminal started")
			self.writeMessage((user_in+'\n').encode())
			print(self.ser.readline())


	def binarize(self,stream):
		binary_stream =[[],[]]
		for row in [0,len(stream)//2]:
			for col in range(cols):
				binary = int(stream[row][col]+"00"+stream[row+1][col],2)
				binary_stream[row//2][col]=binary
		return binary_stream

	def trivialize(self,stream):
		new_stream = [[0]*len(stream[0]) for col in range(len(stream)//2)]
		for row in [0,len(stream)//2]:
			for col in range(len(stream[0])):
				joined_strings = stream[row][col]+stream[row+1][col]
				print(new_stream)
				new_stream[row//2][col]= joined_strings
		return new_stream



	def input_stream(self,stream):
		stream = self.trivialize(stream)
		for row in range(len(stream)):
			for col in range(len(stream[0])):
				self.writeMessage((stream[row][col]+"\n").encode())

				self.ser.flush()
				print(self.ser.readline())
		print("waiting for result")
		time.sleep(5)


term = Terminal("COM12")


stream = [["111","011","101","111","000","010","001","010","101","101","001","001","101","110","101","011"],
		  ["101","001","111","101","001","110","101","011","101","001","111","101","001","110","101","011"],
		  ["111","011","101","111","000","010","001","010","101","001","111","101","001","110","101","011"],
		  ["101","001","111","101","001","110","101","011","101","001","111","101","001","110","101","011"]]


term.input_stream(stream)