from flask import Flask, request, json
import image_slicer
import os
from PIL import Image
import pytesseract
#import cv2
#from .cv2 import *
import re

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def upload_file():
	if request.method == 'POST':
		#print(request.files)
		if 'file' not in request.files:
			return "No file found"
		file = request.files['file']
		file.save("a.jpg")

		text=[]
		image_slicer.slice("a.jpg", 10)

		for f in os.listdir("."):
			if '.png' in f:
				image = Image.open(f)
				t = pytesseract.image_to_string(image, lang='eng')
				text.append(t)

		a = ""
		for i in range(len(text)):
			try:
				match = re.search(r'(\d+/\d+/\d+)', text[i]).group(1)
				a = match
			except:
				pass

		return json.dumps({"dob": a})



if __name__ == "__main__":
	app.run(debug=True)

