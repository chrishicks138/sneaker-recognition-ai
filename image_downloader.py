from config import *;
from shoesql import *
from google_images_download import google_images_download as gid
from archive import *
from convert import *
from paths import *
from status import *
from db import *

class Samples:
  def __init__(self):
    super().__init__()
    self.procs = []
    self.shoes = SHOES

  def gd(self,IMAGE_FORMAT):
    resp = gid.googleimagesdownload()
    try:
      print(IMAGE_FORMAT)
      resp.download({"keywords":self.search,"format":IMAGE_FORMAT,"limit":LIMIT,"aspect_ratio":"square","output_directory":self.model_dir,"no_directory":"1"})
    except:
      raise

  def download(self, sneaker_brand, sneaker_model):
    mdir = ModelDir(sneaker_brand, sneaker_model)
    search = sneaker_brand+' '+sneaker_model
    s = search.replace(' ','/')
    # Remove hyphens
    self.search = search.replace('-',' ')
    self.model_dir = mdir.model_dir()
    IMAGE_FORMAT = 'png'
    self.gd(IMAGE_FORMAT)
    type = 'downloaded'
    args = (sneaker_brand, sneaker_model)
    InitDB().populate_db(args, type)
    if mdir.__len__() != 0:
      Convert(sneaker_brand, sneaker_model).convert()
    else:
      IMAGE_FORMAT = 'jpg'
      self.gd(IMAGE_FORMAT)
      DOWNLOAD_ERRORS.append(mdir.model_dir())
