from torch.utils.tensorboard import SummaryWriter

import random
from config import *
from dataset import *
from model import *
from resnet import *
import tarfile

class Trainer:
  tensorboard = SummaryWriter('runs/sneaker_net');
  def __init__(self):
    super().__init__();

  def plug_net(self, net):
    self.net = net;

  def plug_data_set(self, data_set, batch_size=4, shuffle=True):
    self.data_set = data_set;
    self.batch_size = batch_size
    self.data_loader = torch.utils.data.DataLoader(data_set, batch_size=batch_size, num_workers=0, shuffle=shuffle);

  def train(self, epochs=10, use_gpu=False):
    if use_gpu: self.net.cuda();

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(self.net.parameters(), lr=1e-3)
    
    sub_epoch = 0;
    for epoch in range(epochs):

      running_loss = 0.0;
      total_loss = 0.0;
      running_correct = 0.0;
      total_correct = 0.0;

      train_list = enumerate(self.data_loader, 0);

      log_batch_size = 100;
      log_batch_index = 0;
#      progress = ProgressBar(total=log_batch_size, prefix='Training', suffix='Now', decimals=3, length=50, fill='\u2588', zfill='-')

      for i, data in train_list:
#        progress.print_progress_bar(i - log_batch_index * log_batch_size + 1);
        inputs, labels = data;
        if use_gpu:
          inputs = inputs.cuda();
          labels = labels.cuda();

        #zero the parameter gradients
        optimizer.zero_grad()

        #forward + backward + optimize
        outputs = self.net(inputs);
        loss = criterion(outputs, labels);
        loss.backward();
        optimizer.step();

        #statistics
        running_loss += loss.item();
        running_correct += self.__get_correct_total(outputs, labels);
        total_loss += loss.item();
        total_correct += self.__get_correct_total(outputs, labels);

        if i % log_batch_size == log_batch_size - 1:
          processed_count = self.batch_size * log_batch_size;
 #         print('[%d, %5d] loss: %.3f correct: %5d' %(epoch + 1, i + 1, running_loss / log_batch_size, running_correct))
          self.tensorboard.add_scalar("Loss", running_loss, sub_epoch);
          self.tensorboard.add_scalar("Correct", running_correct, sub_epoch);
          self.tensorboard.add_scalar("Accuracy", running_correct / processed_count, sub_epoch);
          running_loss = 0.0;
          running_correct = 0.0;
          log_batch_index += 1;
          sub_epoch += 1;

    self.tensorboard.close();
    print('\nFinished Training');

  def load_model(self, path):
    self.net.load_state_dict(torch.load(path))

  def save_model(self, path):
    torch.save(self.net.state_dict(), path);

  def __get_correct_total(self, preds, labels):
    return preds.argmax(dim=1).eq(labels).sum().item()

  def rmimg(self):
    for file in os.listdir(mpath[0]):
      if '.jpg' in file:
        os.remove(os.path.join(epath, file))
#    print('\r\nREMOVED '+epath+'\r\n')

  def model_pick(self):
    model = random.choice(oMODELS)
#    print('\nOPENING ARCHIVE: '+model)
    smodel = model.split('/')[0]
    apath = os.path.join(ARC_DIR, model)
    epath = os.path.join(IMG_DIR, smodel)
    mpath = epath.split('/')
    bpath = mpath[3]
    rmodel = model.split('.')[0]
    ipath = epath+'/'+rmodel.split('/')[1]
    if not os.path.exists(ipath):
      os.makedirs(ipath)
    try:
      with tarfile.open(apath) as tar:
        tar.extractall(ipath)
    except:
      return
    global MODEL
    MODEL = []
    MODEL.append(rmodel)

  def run(self):
    trainer = Trainer()
    trainer.model_pick()
    net = Net();
    resnet = resnet101(3, len(MODEL));
    try:
      train_set = SneakersDataset(IMG_DIR, MODEL);
      trainer.plug_net(net);
      trainer.plug_data_set(train_set);
      trainer.load_model(MODEL_SAVE_PATH);
    except:
      print('Training failed!')

#  print("\nInit training :\n")
    trainer.train(20, use_gpu=False);
    trainer.save_model(MODEL_SAVE_PATH);
    trainer.rmimg()
