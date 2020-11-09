DATABASE = "shoes.db"

TABLE = "SHOES"

COLUMN = "downloaded"

COLUMNS = [
  "brand",
  "model",
  "url",
  "downloaded",
]

CREATE_TABLE = """ CREATE TABLE IF NOT EXISTS """+TABLE+''' (brand text NOT NULL, model text NOT NULL, url text NOT NULL, downloaded text NOT NULL);'''


