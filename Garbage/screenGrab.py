import pyscreenshot as ImageGrab

# API Key:AIzaSyDClAsfjxC7BTztP2od5MoNusn4ytZkaQU

if (__name__ == '__main__'):
	im=ImageGrab.grab()
	im.show()
	ImageGrab.grab_to_file('im.png')