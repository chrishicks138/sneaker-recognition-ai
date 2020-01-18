from flask import Flask
import threading
from shoes import *
from status import *
from db import *

app  = Flask(__name__)
lock = threading.Lock()

@app.route('/')
def hello():
  return 'Enter http://localhost:5000/start to start downloading.\n  Wait a few seconds and check terminal output.'

@app.route('/start')
def start():
  Parser().parse()

app.run(debug=True)
