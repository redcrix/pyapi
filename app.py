from flask import Flask, request, json
import image_slicer
import os
from PIL import Image
import pytesseract
import re
import shutil
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def upload_file():
	if request.method == 'POST':
		a = ""
		value=0
		text=[]
		if 'aid' not in request.files:
			message="no file found"
			value=404
			return json.dumps({"code":value,"message":message})
		file = request.files['aid']
		idtype = str(request.form['idtype'])
		file.save("a.jpg")
		for f in os.listdir("/home/redcrix/mysite/static/"):
		    os.remove("/home/redcrix/mysite/static/"+f)
		time = datetime.now().strftime("%d-%b-%Y_%H:%M:%S")
		shutil.copy("a.jpg", "/home/redcrix/mysite/static/"+time+".jpg")
		idpic=str("http://redcrix.pythonanywhere.com/static/"+time+".jpg")
		image = Image.open("a.jpg")
		t = pytesseract.image_to_string(image, lang='eng')
		text.append(t)
		for i in text:
			try:
				match = re.search(r'(\d+/\d+/\d+)', i).group(1)
				a = match
			except:
				pass

		if a=="":

		    image_slicer.slice("a.jpg", 10)
		    for f in os.listdir("."):
    			if '.png' in f:
    				image = Image.open(f)
    				t = pytesseract.image_to_string(image, lang='eng')
    				text.append(t)

		for i in text:
			try:
				match = re.search(r'(\d+/\d+/\d+)', i).group(1)
				a = match
			except:
				pass


		if a=="":
			message="id upload failed"
			value=201
		else:
			message="id uploded successfully"
			value=202
		return json.dumps({"text":text,"code":value,"img": idpic, "message":message,"dob": a})





if __name__ == "__main__":
	app.run(debug=True)

