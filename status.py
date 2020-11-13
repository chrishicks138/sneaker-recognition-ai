from db import *


class Stats:
  def shoes_processed(self):
    totals = len(SHOES)
    return str(totals)

  def shoes_total(self):
    totals = len(TOTAL)
    return str(totals)

  def archive_total(self):
    totals = len(ARCHIVES)
    return str(totals)

  def samples(self):
    totals = len(SAMPLES)
    return str(totals)

  def conv_errors(self):
    totals = len(CONVERSION_ERRORS)
    return str(totals)

  def archive_errors(self):
    totals = len(ARCHIVE_ERRORS)
    return str(totals)
