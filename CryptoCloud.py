import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
from dataProcessing import *
from Threads import *
from flask import send_file
import time
script = ''

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def resultE():
    return render_template('Result.html')

def resultD():
    return render_template('resultD.html')

@app.route('/encrypt/<id>')
def EncryptInput(id):
  Segment()
  gatherInfo()
  HybridCrypt(id)
  return resultE()

@app.route('/decrypt/<id>')
def DecryptMessage(id):
  f=open('Original.txt','rb')
  key=f.read()
  f.close()

  ft = int(key[:2])-11
  lt = int(key[len(key)-2:])-11
  code = str(ft) + str(lt)

  key = str(key)[4:-3]
  key = bytes(key, 'utf-8')

  if code != id:
      return render_template('InvalidCode.html')

  st=time.time()
  HybridDeCrypt(id)
  et=time.time()
  print(et-st)
  trim()
  st=time.time()
  Merge()
  et=time.time()
  print(et-st)
  return resultD()

def start():
  content = open('./Original.txt','r')
  content.seek(0)
  first_char = content.read(1) 
  print(first_char)
  if not first_char:
    return render_template('Empty.html')
  else:
    return render_template('Option.html')


@app.route('/')
def login():
  return render_template('Login.html')

@app.route('/home/')
def index():
  return render_template('index.html')

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/return-files-key/')
def return_files_key():
  try:
    return send_file('./Original.txt',attachment_filename='Original.txt',as_attachment=True)
  except Exception as e:
    return str(e)

@app.route('/return-files-data/')
def return_files_data():
  try:
    return send_file('./Output.txt',attachment_filename='Output.txt',as_attachment=True)
  except Exception as e:
    return str(e)


@app.route('/data/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return render_template('Nofile.html')
    file = request.files['file']
    if file.filename == '':
      return render_template('Nofile.html')
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Original.txt'))
      return start()
       
    return render_template('Invalid.html')
    
if __name__ == '__main__':
  app.run(debug=True)
