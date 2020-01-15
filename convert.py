import os, sys
from config import *;
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from progress import *
from tempfile import mkstemp
from archive import *


class Convert:
  def __init__(self):
    super().__init__()

  def convert(self, model_dir, sneaker_brand, sneaker_model):
    c = 0
    self.m = 0
    if len(os.listdir(model_dir)) != 0:
      for file in os.listdir(model_dir):
        c = 1+c
        try:
          im = Image.open(model_dir+'/'+file)
          deg = [0, 22.5, 45, 67.5, 90, 113.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5]
          md = ["NML","FLR","BLR", "BW"]
          for mode in md:
            for theta in deg:
              self.m = 1+self.m
              image_path = os.path.join(model_dir, "{0}_{1}_{2}_{3}_{4}.jpg".format(sneaker_brand, sneaker_model, c, theta, mode));
              im = im.resize((128, 128))
              im = im.rotate(angle=theta)
              if "FLR" in mode:
                im = im.transpose(method=Image.FLIP_LEFT_RIGHT)
              if "BLR" in mode:
                im = im.filter(ImageFilter.BLUR)
              if "BW" in mode:
                im = im.convert('L')
              im.save(image_path)
              self.bt = len(os.listdir(model_dir))
              self.prestatus = 'Converting'
              self.status = str(c)+' files'
              self.log_batch_index = c
              self.log_batch_size = len(os.listdir(model_dir))
              Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
        except:
          raise
#          print(file+' CORRUPTED, REMOVING')
          self.prestatus = "REMOVING"
          self.status = "CORRUPTED FILE"
          self.log_batch_index = c
          self.log_batch_size = len(os.listdir(model_dir))
          Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
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
    Archive().archive_prep(sneaker_brand, sneaker_model, model_dir)

