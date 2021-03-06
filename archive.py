import tarfile
from config import *;
from paths import *
from db import *

class Archive:
    def __init__(self, sneaker_brand, sneaker_model):
        self.ArcDir = ArcDir(sneaker_brand, sneaker_model)
        self.extract = ExtractDir(sneaker_brand, sneaker_model)
        self.mdir = ModelDir(sneaker_brand, sneaker_model)
        self.sneaker_brand = sneaker_brand
        self.sneaker_model = sneaker_model
        ARCHIVES = [file for file in self.ArcDir.__ls__()]

    def archive_prep(self):
        files = []
        if len(self.mdir.__ls__()) != 0:
            for d in self.mdir.__ls__():
                if ARCHIVE_FORMAT not in d:
                    if IMAGE_FORMAT in d:
                        files.append(self.mdir.model_dir()+'/'+d)
            Archive(self.sneaker_brand, self.sneaker_model).archive(files)

    def archive(self, files):
        try:
            archive_file = self.ArcDir.archive_file()
            with tarfile.open(archive_file, "w:gz") as tar:
                for file in files:
                    image = self.mdir.basename(file)
                    tar.add(file, arcname=image)
                    try:
                        self.mdir.__rmfile__(file)
                    except:
                        raise
            print("Archive success")
        except:
            ARCHIVE_ERRORS.append([files])
            pass
