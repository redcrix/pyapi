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

		value=0

		print(request.files['aid'])
		if 'aid' not in request.files:
			message="no file found"
			value=404
			return json.dumps({"code":value,"message":message,"dob": a})
		file = request.files['aid']
		file.save("a.jpg")
		idpic=str("https://www.pythonanywhere.com/user/redcrix/files/home/redcrix/a.jpg")

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
			value=201
		else:
			message="id uploded successfully"
			value=202
		return json.dumps({"code":value,"img": idpic, "message":message,"dob": a})



if __name__ == "__main__":
	app.run(debug=True)


