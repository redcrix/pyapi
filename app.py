from flask import Flask, request, json
import image_slicer
import os
from PIL import Image
import pytesseract
import re

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def upload_file():
	if request.method == 'POST':

		a = ""

		print(request.files)
		if 'file_idproof' not in request.files:
			message="no file found"
			return json.dumps({"message":message,"dob": a})
		file = request.files['file_idproof']
		file.save("a.jpg")

		text=[]
		image_slicer.slice("a.jpg", 10)

		for f in os.listdir("."):
			if '.png' in f:
				image = Image.open(f)
				t = pytesseract.image_to_string(image, lang='eng')
				text.append(t)

		
		for i in range(len(text)):
			try:
				match = re.search(r'(\d+/\d+/\d+)', text[i]).group(1)
				a = match
			except:
				pass


		if a=="":
			message="id upload failed"
		else:
			message="id uploded successfully"
		return json.dumps({"message":message,"dob": a})



if __name__ == "__main__":
	app.run(debug=True)

