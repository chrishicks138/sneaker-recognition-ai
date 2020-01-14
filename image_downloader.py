import tarfile
import os, sys
import urllib.request;
import requests;
import mimetypes;
from console_progressbar import ProgressBar;
from data_transform import *;
from config import *;
from google_images_download import google_images_download as gid
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from trainer import *
from progress import *

class HiddenPrints:
  def __enter__(self):
    self._original_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

  def __exit__(self, exc_type, exc_val, exc_tb):
     sys.stdout.close()
     sys.stdout = self._original_stdout


class Samples:
  def __init__(self):
    super().__init__()

  def convert(self, model_dir):
    c = 0
    if len(os.listdir(model_dir)) != 0:
      for file in os.listdir(model_dir):
        c = 1+c
        try:
          im = Image.open(model_dir+'/'+file)
          deg = [0, 22.5, 45, 67.5, 90, 113.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5]
          md = ["NML","FLR","BLR", "BW"]
          for mode in md:
            for theta in deg:
              image_path = os.path.join(model_dir, "{0}_{1}_{2}_{3}_{4}.jpg".format(self.sneaker_brand, self.sneaker_model, c, theta, mode));
              im = im.resize((128, 128))
              im = im.rotate(angle=theta)
              if "FLR" in mode:
                im = im.transpose(method=Image.FLIP_LEFT_RIGHT)
              if "BLR" in mode:
                im = im.filter(ImageFilter.BLUR)
              if "BW" in mode:
                im = im.convert('L')
              im.save(image_path)
              self.prestatus = 'Converting'
              self.status = str(c)+' files'
              self.log_batch_index = c
              self.log_batch_size = len(os.listdir(model_dir))
              Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
        except:
#          raise
#          print(file+' CORRUPTED, REMOVING')
          self.prestatus = "REMOVING"
          self.status = "CORRUPTED FILE"
          self.log_batch_index = c
          self.log_batch_size = len(os.listdir(model_dir))
          Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
          Status().status(self.bt, self.prestatus, self.status, self.m)
          os.remove(model_dir+'/'+file)
          continue
        try:
          os.remove(model_dir+'/'+file)
        except:
#          print('\n'+file+' NOT FOUND!')
          break
#    print('\nREMOVED '+str(c)+'files\n')
    else:
      pass
    samples.archive_prep()

  def archive_prep(self):
    files = []
    for d in os.listdir(self.model_dir):
      if 'tar.bz2' not in d:
        if '.jpg' in d:
          files.append(os.path.join(self.model_dir, d))
    samples.archive(files)

  def archive(self, files):
    arcdir = os.path.join(ARC_DIR, self.sneaker_brand)
    if not os.path.exists(arcdir):
      os.makedirs(arcdir)
    tfile = arcdir+'/'+self.sneaker_model+'.tar.bz2'
    with tarfile.open(tfile, "w:bz2") as tar:
      c = 0
      for f in files:
        c = 1+c
        self.prestatus = 'Archiving'
        self.status = str(c)+' files'
        self.log_batch_index = c
        self.log_batch_size = len(files)
        Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
        image = os.path.basename(f)
        tar.add(f, arcname=image)
        os.remove(f)
      tar.close()
#    print(str(c)+' FILES ARCHIVED\n')
    Trainer().run(tfile)
    try:
      for f in os.listdir(model_dir):
        os.remove(model_dir+'/'+f)
#    print('\rREMOVING '+model_dir+'\r')
      os.rmdir(model_dir)
    except:
#    print('\r'+model_dir+' NOT FOUND!')
      return


  def download(self, sneaker_brand, sneaker_model):
    self.prestatus = 'Downloading'
    self.status = str(LIMIT)+' files'
    self.log_batch_index = self.m
    self.log_batch_size = self.bt
    Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
    search = sneaker_brand+' '+sneaker_model
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model
    s = search.replace(' ','/')
    model_dir = os.path.join(ORIG_IMG_DIR, s)
    resp = gid.googleimagesdownload()
    with HiddenPrints():
      resp.download({"silent_mode":"0","keywords":search,"format":"jpg","limit":LIMIT,"aspect_ratio":"square","output_directory":model_dir,"no_directory":"1"})
      self.model_dir = model_dir
    samples.convert(model_dir)

  def download_images(self):
    sneaks = []
    print('\n')
    self.prestatus = 'Searching'
    self.m = 0
    antiTraversal = ['../', 'cat ../', ]
    with open(DATA_DIR+'/shoes.txt', 'r') as shoes:
      for shoe in shoes:
        for traversal in antiTraversal:
          if traversal not in shoe:
            sneaks.append(shoe)
    for shoe in sneaks:
      self.bt = len(sneaks)
      sneaker_model_names = shoe.split('_')
      sneaker_brand = sneaker_model_names[0];
      sneaker_model = sneaker_model_names[1];
      sneaker_model = sneaker_model.replace('\n','')
      model_dir = os.path.join(ORIG_IMG_DIR, sneaker_brand, sneaker_model);
      self.m = 1+self.m
      self.status = str(self.m)+'/'+str(self.bt)
      self.log_batch_index = self.m
      self.log_batch_size = self.bt
      Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
      if not os.path.exists(model_dir):
        os.makedirs(model_dir);
      arcdir = os.path.join(ARC_DIR, sneaker_brand)
      if not os.path.exists(arcdir):
        os.makedirs(arcdir)
        if (sneaker_model+'.tar.bz2') in os.listdir(arcdir):
          print('Archive found! Skipping...')
          continue
        else:
          samples.download(sneaker_brand, sneaker_model)
      continue

samples = Samples()
samples.download_images()
