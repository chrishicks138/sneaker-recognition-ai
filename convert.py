import sys
from config import *;
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from progress import *
from tempfile import mkstemp
from archive import *

class Convert:
  def __init__(self, sneaker_brand, sneaker_model):
    super().__init__()
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model
    self.mdir = ModelDir(self.sneaker_brand, self.sneaker_model)

  def convert(self):
    c = 0
    self.m = 0
    model_dir = self.mdir.model_dir()
    if self.mdir.__len__() != 0:
      self.prestatus = 'Converting'
      deg = [0, 22.5, 45, 67.5, 90, 113.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5]
      md = ["NML","FLR","BLR", "BW"]
      self.bt = (self.mdir.__len__() * len(deg) * len(md))
      self.log_batch_size = self.bt
      for file in self.mdir.__ls__():
        c = 1+c
        try:
          im = Image.open(model_dir+'/'+file)
          for mode in md:
            for theta in deg:
              self.m = 1+self.m
              image_path = model_dir+'/'+"{0}_{1}_{2}_{3}_{4}.jpg".format(self.sneaker_brand, self.sneaker_model, c, theta, mode)
              im = im.resize((128, 128))
              im = im.rotate(angle=theta)
              if "FLR" in mode:
                im = im.transpose(method=Image.FLIP_LEFT_RIGHT)
              if "BLR" in mode:
                im = im.filter(ImageFilter.BLUR)
              if "BW" in mode:
                im = im.convert('L')
              im.save(image_path)
              self.status = str(c)+' files'
              self.log_batch_index = self.m
              Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
        except:
          raise
#          print(file+' CORRUPTED, REMOVING')
          self.mdir.__rm__()
          continue
        try:
          self.mdir.__rm__()
        except:
#          print('\n'+file+' NOT FOUND!')
          break
#    print('\nREMOVED '+str(c)+'files\n')
    else:
      pass
    Archive().archive_prep(self.sneaker_brand, self.sneaker_model, model_dir)

