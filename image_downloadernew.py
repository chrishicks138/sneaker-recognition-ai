import tarfile
import os;
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

def convert():
  c = 0
  for file in os.listdir(model_dir):
    c = 1+c
    try:
      im = Image.open(model_dir+'/'+file)
      deg = [0, 22.5, 45, 67.5, 90, 113.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5]
      md = ["NML","FLR","BLR", "BW"]
      for mode in md:
        for theta in deg:
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
    except:
      os.remove(model_dir+'/'+file)

def archive_prep():
  files = []
  for d in os.listdir(model_dir):
    if 'tar.gz' not in d:
      if '.jpg' in d:
        files.append(os.path.join(model_dir, d))
  archive(files)

def archive(files):
  arcdir = os.path.join(ARC_DIR, sneaker_brand)
  if not os.path.exists(arcdir):
    os.makedirs(arcdir)
  with tarfile.open(arcdir+'/'+sneaker_model+'.tar.gz', "w:gz") as tar:
    for f in files:
      image = os.path.basename(f)
      tar.add(f, arcname=image)
      os.remove(f)
    for tarinfo in tar:
      print(tarinfo.size)
    tar.close()w
  try:
    os.rmdir(model_dir)
  except:
    for f in os.listdir(model_dir):
      os.remove(model_dir+'/'+f)
    os.rmdir(model_dir)




def download_images():
  global model_dir
  global sneaker_brand
  global sneaker_model
  m = 0
  for filename in os.listdir(DATA_DIR):
    bt = len(os.listdir(DATA_DIR))
    if filename.endswith(".txt"):
      sneaker_model_names = os.path.splitext(filename)[0].split('_');
      sneaker_brand = sneaker_model_names[0];
      sneaker_model = sneaker_model_names[1];
      model_dir = os.path.join(ORIG_IMG_DIR, sneaker_brand, sneaker_model);
      m = 1+m
      mpct = m / bt * 100
      print(str(m)+'/'+str(bt), str(mpct)+'%')
      if not os.path.exists(model_dir):
        os.makedirs(model_dir);
        arcdir = os.path.join(ARC_DIR, sneaker_brand)
        if not os.path.exists(arcdir):
          os.makedirs(arcdir)
        if (sneaker_model+'.tar.gz') in os.listdir(arcdir):
          print('Archive found! Skipping...')
        else:
          print('Directory empty!')
          i = 0
          try:
            search = sneaker_brand+' '+sneaker_model
            resp = gid.googleimagesdownload()
            aip = resp.download({"keywords":search,"format":"jpg","limit":10,"aspect_ratio":"square","output_directory":model_dir,"no_directory":"1"})
          except:
            continue;
    convert()
    archive_prep()

if __name__ == "__main__":
  download_images();
