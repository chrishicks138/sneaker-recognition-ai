from flask import Flask
from shoes import *
from status import *
from trainer import Trainer

app  = Flask(__name__)
lock = threading.Lock()

@app.route('/')
def hello():
  return 'Enter http://localhost:5000/start to start downloading.\n  Wait a few seconds and check terminal output.'

@app.route('/start')
def start():
  Search().search()

@app.route('/stats/processed')
def processed():
  return Stats().shoes_processed()

@app.route('/stats/total')
def total():
  return Stats().shoes_total()

@app.route('/stats/archive_total')
def archive_total():
  return Stats().archive_total()

@app.route('/train')
def train():
  Trainer().run()

app.run(debug=True)
