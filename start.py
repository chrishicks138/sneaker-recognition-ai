from flask import Flask, render_template, g, request, redirect, url_for
from flask_socketio import SocketIO
from status import *
from trainer import *
import wtforms
import sql
import sqlConfig
from image_downloader import Samples

sql.main()
app  = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True, async_mode="threading")

class Forms(wtforms.Form):
    @app.route('/', methods=['GET', 'POST'])
    def hello():
        downloads = str(len(DOWNLOADED))+' downloaded'
        form = Forms(request.form)
        return render_template('index.html',
                               form=form,
                               downloads=downloads,
                               )

    def event(self,f):
        if f == 1:
            socketio.emit('stat_event', { 'data' : ' '+str(self.c+1)+'/'+str(len(self.SHOES))+' shoes processed '
                                         +self.archives+' archives '
                                         +self.cerrors+' conversion errors, '
                                         +self.arcErrors+' archive errors '
                                         +str(len(DOWNLOAD_ERRORS))+' download errors '
                                         +str(len(DOWNLOADED))+' shoes downloaded'
                                         })
            socketio.emit('download_event', { 'data' : 'Downloading '+self.shoe[0]+self.shoe[1]})
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
        if f == 7:
            socketio.emit('data event', { 'data' : ' Training'})

    def remove(self):
        f = 2
        self.event(f)
        while len(self.SHOES) > 0:
            for i,shoe in enumerate(self.SHOES):
                self.SHOES.pop(i)
        f = 3
        self.event(f)

    def stats(self):
        self.archives = Stats().archive_total()
        self.cerrors = Stats().conv_errors()
        self.arcErrors = Stats().archive_errors()
        f = 1
        self.event(f)

    def download(self):
        BRANDS = [item[0] for item in sql.get_all(sqlConfig.DATABASE) if item[3] == 'False'] 
        self.SHOES = [(item[0], item[1]) for item in sql.get_all(sqlConfig.DATABASE) if item[3] == 'False']
        for self.c, self.shoe in enumerate(self.SHOES):
            self.stats()
            Samples.download(self.shoe[0], self.shoe[1])
        f = 4
        self.event(f)
        return

@socketio.on('list_event')
def list_event(json, methods=['GET', 'POST']):
    socketio.emit('list_response', { 'data' : len(sql.get_all(sqlConfig.DATABASE))})


  #@socketio.on('shoe_event')
@socketio.on('start')
def handle_event(methods=['GET', 'POST']):
    Forms().download()


@socketio.on('stop_event')
def stop_event(methods=['GET', 'POST']):
    Forms().remove()


@socketio.on('train')
def train():
  f = 7
  Forms().event(f)
  Trainer().run()

@app.route('/stats/total')
def total():
  return Stats().shoes_total()

@app.route('/stats/archive_total')
def archive_total():
  return Stats().archive_total()

@app.route('/stats/conversion_errors')
def conversion_total():
  return Stats().conv_errors()


#init_db()
socketio.run(app, host='0.0.0.0', debug=True)
