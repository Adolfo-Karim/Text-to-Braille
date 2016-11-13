#main.py
import string
from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import pyscreenshot as ImageGrab
import requests

class Translator(object):

	alphabets_braille1={  "":"",
	   					  " ": "000000",
	                      'a': "100000",
	                      'b': "110000",
	                      'c': "100100",
	                      'd': "100110",
	                      'e': "100010",
	                      'f': "110100",
	                      'g': "110110",
	                      'h': "110010" ,
	                      'i': "010100",
	                      'j': "010110",
	                      'k': "10100",
	                      'l': "111000",
	                      'm': "101100",
	                      'n': "101110",
	                      'o': "101010",
	                      'p': "111100",
	                      'q': "111110",
	                      'r': "111010",
	                      's': "011100",
	                      't':  "011110",
	                      'u': "101001",
	                      'v': "111001",
	                     'w': "010111",
	                      'x': "101101",
	                      'y': "101111",
	                      'z': "101011",
	                      '?': "011001"}

	numbers_braille1= {   "0": "010110",
	                      "1": "100000",
	                      "2": "110000",
	                      "3": "100100",
	                      "4": "100110",
	                      "5": "100010",
	                      "6": "110100",
	                      "7": "110110",
	                      "8": "110010" ,
	                      "9": "010100",
	                      "0": "010110",}
	num_initializer= "001111"

	def __init__(self):
		pass

	def convertTextToString(self,symbol):
	    result=""
	    if(symbol.isdigit()):
	        result += Translator.num_initializer+Translator.numbers_braille1[symbol]
	    elif(symbol.isupper()):
	      	result= "000001" + Translator.alphabets_braille1[symbol.lower()]
	    elif(symbol=="."): 
	      	result= "010011"
	    elif(symbol==","): 
	      	result="010000"    
	    else:
	      	result=Translator.alphabets_braille1[symbol] 
	    return result

	def convert(self,string):
	  	resultStr=""
	  	for c in string:
	  		resultStr+=self.convertTextToString(c)
	  	return resultStr

	def filterText(self,text):
	  	text.replace("\n"," ")
	  	result=""
	  	for c in text:
	  		if c in (string.ascii_letters +string.digits+".,?"+" "):
	  			result+=c
	  	return result

	#makes it into strings of 48
	def convertToReadableForm(self,primary_string):
	    mainarray=[]
	    for j in range(0,len(primary_string),48):
	        arr=""
	        for i in range (j,j+48):
	            try:
	            	arr+=str(primary_string[i])
	            except:
	                break
	        mainarray.append(arr)
	    return mainarray


	#########################################################
	def converter(self,primary_string):
		next_string = self.convert(self.filterText(primary_string))
		main_string = self.convertToReadableForm(next_string)
		mainArray=[]
		for string in main_string:
			result=[]
			for i in range(0,len(string),3):
				res=string[i:i+3]
				result.append(res)
			for i in range(len(result),16):
				result.append("000")
			mainArray.append(result)
		for i in range(len(mainArray),4):
			mainArray.append(["000","000","000","000","000","000","000","000","000",\
	                          "000","000","000","000","000","000","000"])
		return mainArray

class ScreenToText (object):
	ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
	RESULTS_DIR = 'jsons'
	makedirs(RESULTS_DIR, exist_ok=True)

	def __init__(self):
		pass

	def make_image_data_list(self,image_filenames):
		"""
		image_filenames is a list of filename strings
		Returns a list of dicts formatted as the Vision API
			needs them to be
		"""
		img_requests = []
		for imgname in image_filenames:
			with open(imgname, 'rb') as f:
				ctxt = b64encode(f.read()).decode()
				img_requests.append({
						'image': {'content': ctxt},
						'features': [{
							'type': 'TEXT_DETECTION',
							'maxResults': 1
						}]
				})
		return img_requests

	def make_image_data(self,image_filenames):
		"""Returns the image data lists as bytes"""
		imgdict = self.make_image_data_list(image_filenames)
		return json.dumps({"requests": imgdict }).encode()


	def request_ocr(self,image_filenames):
		response = requests.post(ScreenToText.ENDPOINT_URL,
								 data=self.make_image_data(image_filenames),
								 params={'key': "AIzaSyDClAsfjxC7BTztP2od5MoNusn4ytZkaQU"},
								 headers={'Content-Type': 'application/json'})
		return response


	def  run(self,box):
		im=ImageGrab.grab(bbox = box)
		im.show()
		ImageGrab.grab_to_file('im.png')
		image_filenames = ["im.png"]
		text= open("text.txt","w")
		text.write("")
		text.close()
		text = open("text.txt","a")
		if not image_filenames:
			print("""
				Please supply an image filename

				$ python translatorMain.py image1.jpg""")
		else:
			response = self.request_ocr(image_filenames)
			if response.status_code != 200 or response.json().get('error'):
				print(response.text)
			else:
				for idx, resp in enumerate(response.json()['responses']):
					# save to JSON file
					imgname = image_filenames[idx]
					jpath = join(ScreenToText.RESULTS_DIR, basename(imgname) + '.json')
					with open(jpath, 'w') as f:
						datatxt = json.dumps(resp, indent=2)
						print("Wrote", len(datatxt), "bytes to", jpath)

					# print the plaintext to screen for convenience
					print("---------------------------------------------")
					t = resp['textAnnotations'][0]
					print (t["description"])
					return t['description']
					"""
					print("    Bounding Polygon:")
					print(t['boundingPoly'])
					print("    Text:")
					print(t['description'])
					"""
					text.write(t['description'])
					
			text.close()

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
		new_stream = [['000']*len(stream[0]) for row in range(len(stream)//2)]
		for row in range(0,len(stream)//2,2):
			for col in range(len(stream[0])):
				joined_strings = stream[row][col]+stream[row+1][col]
				new_stream[row//2][col]= joined_strings
		return new_stream



	def input_stream(self,stream):
		stream = self.trivialize(stream)
		for row in range(len(stream)):
			for col in range(len(stream[0])):
				self.writeMessage((stream[row][col]+"\n").encode())
				self.ser.flush()
			input()
		print("waiting for result")
		time.sleep(5)


def main():
	screen_grabber = ScreenToText()
	braille_to_text = Translator()
	terminal = Terminal("COM4")

	x_coord = float(input("Enter x coord of box on screen"))
	y_coord = float(input("Enter y coord of the top left corner"))
	height = float(input("Enter the height of screen grab box"))
	width = float(input("Enter the width of the screen grab box"))

	text = screen_grabber.run((x_coord,y_coord,height,width))

	stream = braille_to_text.converter(text)
	terminal.input_stream(stream)

if __name__ == "__main__":
    main()


"""

term = Terminal("COM12")

stream = [["111","011","101","111","000","010","001","010","101","101","001","001","101","110","101","011"],
		  ["101","001","111","101","001","110","101","011","101","001","111","101","001","110","101","011"],
		  ["111","011","101","111","000","010","001","010","101","001","111","101","001","110","101","011"],
		  ["101","001","111","101","001","110","101","011","101","001","111","101","001","110","101","011"]]


term.input_stream(stream)

"""