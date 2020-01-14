from console_progressbar import ProgressBar
import sys

class Status:
  def __init__(self):
    super().__init__()
#    self.bt = bt

  def status(self, bt, prestatus, status, m, log_batch_index, log_batch_size):
    progress = ProgressBar(total=bt, prefix=prestatus, suffix=status+'        ', decimals=2, length=50, fill='\u2588', zfill='_')
    progress.print_progress_bar(m - log_batch_index / log_batch_size + 1)
    sys.stdout.write("\u001b[0K")
    return
