from config import *;
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
        search = search.replace('-',' ')
        model_dir = mdir.model_dir()
        resp = gid.googleimagesdownload()
        if mdir.__len__() == 0:
            try:
                resp.download({"keywords":search,
                               "format":IMAGE_FORMAT,
                               "limit":LIMIT,
                               "aspect_ratio":"square",
                               "output_directory":model_dir,
                               "no_directory":"1",
                               #"proxy":proxy,
                               })
            except:
                pass
            if mdir.__len__() != 0:
                Convert(sneaker_brand, sneaker_model).convert()
            else:
                DOWNLOAD_ERRORS.append(mdir.model_dir())
        else:
            DOWNLOADED.append(sneaker_model)
