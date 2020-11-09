from config import *;
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from archive import *

class Convert:
  def __init__(self, sneaker_brand, sneaker_model):
    super().__init__()
    self.files = []
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model
    self.mdir = ModelDir(self.sneaker_brand, self.sneaker_model)
    self.deg = [0, 22.5, 45, 67.5, 90, 113.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5]
    self.md = ["NML","FLR","BLR", "BW"]
    self.model_dir = self.mdir.model_dir()
    self.m = 0
    for file in self.mdir.__ls__():
      if len(self.files) < LIMIT:
        self.files.append(file)
      else:
        break

  def convert(self):
    for file in self.files:
      file = self.model_dir+'/'+file
      ext = file.split('.')[1]
      try:
        with Image.open(file) as im:
          im = im.resize((128,128), reducing_gap=2)
          im.save(file)
          for mode in self.md:
            for theta in self.deg:
              image_path = self.model_dir+'/'+self.sneaker_brand+'_'+self.sneaker_model+'_'+self.m+'_'+theta+'_'+mode+'.'+ext
              print(image_path)
              if "FLR" in mode:
                im = im.transpose(method=Image.FLIP_LEFT_RIGHT)
              if "BLR" in mode:
                im = im.filter(ImageFilter.BLUR)
              if "BW" in mode:
                im = im.convert('L')
              im = im.rotate(angle=theta)
              print("Success", mode, theta)
              im.save(image_path)
      except:
        self.mdir.__rmfile__(file)
        CONVERSION_ERRORS.append(file)
        return
      try:
        self.mdir.__rmfile__(file)
      except:
        raise
    Archive(self.sneaker_brand, self.sneaker_model).archive_prep()
