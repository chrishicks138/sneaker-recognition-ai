from db import *

class Stats:
  def shoes_processed(self):
    totals = len(SHOES)
    return str(totals)+' shoes processed.\n'

  def shoes_total(self):
    totals = len(TOTAL)
    return str(totals)+' shoe brands.\n'

  def archive_total(self):
    totals = len(ARCHIVES)
    return str(totals)+' shoe brands converted.\n'
