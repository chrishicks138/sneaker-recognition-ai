from config import *;
#from shoesql import *
from google_images_download import google_images_download as gid
from archive import *
from convert import *
from paths import *
from status import *
from db import *

class Samples:
  def __init__(self):
    super().__init__()


  def download(sneaker_brand, sneaker_model):
    mdir = ModelDir(sneaker_brand, sneaker_model)
    search = sneaker_brand+' '+sneaker_model
    s = search.replace(' ','/')
    # Remove hyphens
    search = search.replace('-',' ')
    model_dir = mdir.model_dir()
    IMAGE_FORMAT = 'png'
    resp = gid.googleimagesdownload()
    try:
      print(IMAGE_FORMAT)
      resp.download({"keywords":search,
                     "format":IMAGE_FORMAT,
                     "limit":LIMIT,
                     "aspect_ratio":"square",
                     "output_directory":model_dir,
                     "no_directory":"1",
#                     "proxy":proxy,
                     })
    except:
      raise
    print(mdir.__len__())
    if mdir.__len__() != 0:
      print("Converting")
      Convert(sneaker_brand, sneaker_model).convert()
    else:
      DOWNLOAD_ERRORS.append(mdir.model_dir())
