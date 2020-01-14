import os

#Sneaker model categories
MODELS = []
ORIG_IMG_DIR = "./Data/Originals/"
ARC_DIR = "./Data/Archives"

for dir in os.listdir(ARC_DIR):
  for d in os.listdir(ARC_DIR+'/'+dir):
    MODELS.append(dir+'/'+d)

#Data directory path
DATA_DIR = "./Data/Downloads";
#Dataset images directory path
IMG_DIR = "./Data/Images/"
#Model to save directory path
MODEL_SAVE_PATH = "./sneaker_net.pth";
#Test images directory path
TEST_DIR = "./Data/Test";
#Download limit
LIMIT = 10
#Training passes
PASS = 20
