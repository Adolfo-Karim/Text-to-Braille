from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import pyscreenshot as ImageGrab
import requests

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)

def make_image_data_list(image_filenames):
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

def make_image_data(image_filenames):
	"""Returns the image data lists as bytes"""
	imgdict = make_image_data_list(image_filenames)
	return json.dumps({"requests": imgdict }).encode()


def request_ocr(image_filenames):
	response = requests.post(ENDPOINT_URL,
							 data=make_image_data(image_filenames),
							 params={'key': "AIzaSyDClAsfjxC7BTztP2od5MoNusn4ytZkaQU"},
							 headers={'Content-Type': 'application/json'})
	return response


if __name__ == '__main__':
	im=ImageGrab.grab()
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

			$ python textindex.py image1.jpg""")
	else:
		response = request_ocr(image_filenames)
		if response.status_code != 200 or response.json().get('error'):
			print(response.text)
		else:
			for idx, resp in enumerate(response.json()['responses']):
				# save to JSON file
				imgname = image_filenames[idx]
				jpath = join(RESULTS_DIR, basename(imgname) + '.json')
				with open(jpath, 'w') as f:
					datatxt = json.dumps(resp, indent=2)
					print("Wrote", len(datatxt), "bytes to", jpath)
					print(datatxt)

				# print the plaintext to screen for convenience
				print("---------------------------------------------")
				t = resp['textAnnotations'][0]
				print("    Bounding Polygon:")
				print(t['boundingPoly'])
				print("    Text:")
				print(t['description'])
				text.write(t['description'])
		text.close()
