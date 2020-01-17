import json
import pymongo

data_file = '../scratch/kesenhuang/graphics.json'

with open(data_file, 'r') as f:
    data = json.load(f)

cg_client = pymongo.MongoClient("mongodb://localhost:27017")
cg_db = cg_client["kesenhuang"]
cg_col = cg_db["papers"]

cg_col.insert_many(data)

