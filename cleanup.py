import os, sys

class Clean:

  def __init__(self):
    super().__init__()

  def rmimg(self, ipath):
    for file in os.listdir(ipath):
      if '.jpg' in file:
        os.remove(os.path.join(ipath, file))
    os.rmdir(ipath)
