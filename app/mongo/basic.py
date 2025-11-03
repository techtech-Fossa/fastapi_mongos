from pymongo import MongoClient

# MONGO_URL = "mongodb://mongodb-primary:27017,mongodb-secondary:27017/?replicaSet=rs0"
MONGO_URL = "mongodb://mongodb-primary:27017/"

# MongoDBに接続
client = MongoClient(MONGO_URL)

# データベースとコレクションを選択
db = client["sample_db"]
collection = db["users"]

# ドキュメントの挿入
collection.insert_one({"name": "Alice", "age": 30})

# ドキュメントの検索
user = collection.find_one({"name": "Alice"})
print(user)
