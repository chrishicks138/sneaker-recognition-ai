from flask import Flask, render_template, g, request, redirect, url_for
from flask_socketio import SocketIO
#from database_init import *
from status import *
from trainer import *
from shoesql import *
import wtforms

app  = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True, async_mode="threading")

class Forms(wtforms.Form):
  search = wtforms.TextField('search')
  @app.route('/', methods=['GET', 'POST'])
  def hello():
    args = '-1'
    type = 'brand'
    Forms().query(type,args)
    downloads = str(len(DOWNLOADED))+' downloaded'
    form = Forms(request.form)
    brands = set(BRANDS)
    brandlen = str(len(brands))+' brands'
    return render_template('index.html', form=form, downloads=downloads, brandlen=brandlen, brands=brands)

  def event(self,f):
    if f == 1:
      socketio.emit('stat event', { 'data' : ' '+str(self.c+1)+'/'+str(len(SHOES))+' shoes '+self.archives+' archives '+self.cerrors+' errors, '})
      socketio.emit('data event', { 'data' : ' Downloading '+self.brand+', '+str(len(SHOES))+' models'})
    if f == 2:
      socketio.emit('data event', { 'data' : ' Stopping'})
    if f == 3:
      socketio.emit('data event', { 'data' : ' Stopped'})
    if f == 4:
      socketio.emit('data event', { 'data' : ' Finished'})
    if f == 5:
      socketio.emit('data event', { 'data' : ' Initializing Database'})
    if f == 6:
      socketio.emit('data event', { 'data' : ' Done'})

  def remove(self):
    while len(SHOES) > 0:
      for i,shoe in enumerate(SHOES):
        SHOES.pop(i)

  def stats(self):
    self.archives = Stats().archive_total()
    self.cerrors = Stats().conv_errors()
    f = 1
    self.event(f)

  def download(self,brand,stop):
    shoes = enumerate(SHOES)
    self.brand = brand
    for self.c,shoe in shoes:
      self.stats()
      shoe = brand+'_'+shoe
      Download().do_work(shoe)
      if stop():
        f = 2
        self.event(f)
        self.remove()
        f = 3
        self.event(f)
        break
    f = 4
    self.event(f)
    return

  def start(self,brand):
    stop = False
    self.download(brand, lambda : stop)

  def query(self,type,args):
    for model in Query().query_db(type,args):
      if (model['downloaded'] == 0):
        if type == 'brand':
          brand = model['brand']
          BRANDS.append(brand)
        if type == 'model':
          shoe = model['model']
          SHOES.append(shoe)
      else:
        if model not in DOWNLOADED:
          DOWNLOADED.append(model)

  @socketio.on('shoe event')
  def handle_event(json, methods=['GET', 'POST']):
    for item,brands in json.items():
      print(item,brands)
      for brand in brands:
        args = '%'+brand+'%'
        type = 'model'
        Forms().query(type,args)
        Forms().start(brand)

  @socketio.on('stop event')
  def stop_event(methods=['GET', 'POST']):
    stop = True
    brand = None
    Forms().download(brand, lambda : stop)

  @socketio.on('reinit event')
  def reinit(methods=['GET', 'POST']):
    f = 5
    Forms().event(f)
    Download().main()
    f = 6
    Forms().event(f)

@app.route('/init')
def initdb():
  Download().main()

@app.route('/restart')
def restart():
  return Thread().start()

@app.route('/stats/processed')
def processed():
  return Stats().shoes_processed()

@app.route('/stats/total')
def total():
  return Stats().shoes_total()

@app.route('/stats/archive_total')
def archive_total():
  return Stats().archive_total()

@app.route('/stats/conversion_errors')
def conversion_total():
  return Stats().conv_errors()

#@app.route('/stats/download_errors')
#def download_total():
#  return Stats().down_errors()

@app.route('/train')
def train():
  Trainer().run()

#init_db()
socketio.run(app, host='0.0.0.0', debug=True)
