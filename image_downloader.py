from config import *;
from google_images_download import google_images_download as gid
from trainer import *
from archive import *
from convert import *
from paths import *
from status import *
from db import *

class Samples:
  def __init__(self, shoe):
    super().__init__()
    self.hidden = HiddenPrints()
    self.shoe = shoe

  def download(self):
    search = self.sneaker_brand+' '+self.sneaker_model
    s = search.replace(' ','/')
    print('\n'+search)
    model_dir = self.mdir.model_dir()
    resp = gid.googleimagesdownload()
    with self.hidden:
      resp.download({"keywords":search,"format":IMAGE_FORMAT,"limit":LIMIT,"aspect_ratio":"square","output_directory":model_dir,"no_directory":"1"})
    if self.mdir.__len__() != 0:
      Convert(self.sneaker_brand, self.sneaker_model).convert()

  def check(self):
    SHOES.append(self.shoe)
    sneaker_model_names = self.shoe.split('_')
    sneaker_brand = sneaker_model_names[0]
    sneaker_model = sneaker_model_names[1]
    self.sneaker_brand = sneaker_brand
    self.sneaker_model = sneaker_model
    self.mdir = ModelDir(sneaker_brand, sneaker_model)
    arcDir = ArcDir(sneaker_brand, sneaker_model)
    try:
      arcDir.arc_dir()
      if arcDir.lsarc() is False:
        self.download()
      else:
        print('Archive found')
    except:
      raise

