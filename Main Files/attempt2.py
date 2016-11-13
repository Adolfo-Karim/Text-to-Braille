
import os
from flask import Flask, request, render_template,redirect, url_for
from werkzeug.utils import secure_filename
import mainNoGrab

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('home.html')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploaded_file():
   if request.method == 'POST':
      f = request.files['file']
      # os.rename(f.filename,"steamingpileofshit.txt")
      f.save("steamingpileofshit.png")
      print(f.filename)
      mainNoGrab.run()
      return 'file uploaded successfully'


