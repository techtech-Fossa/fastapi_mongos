from pymongo import MongoClient, errors

# MongoDBに接続（レプリカセットが必要）
client = MongoClient("mongodb://mongodb-primary:27017/?replicaSet=rs0")
db = client["test_db"]
accounts = db["accounts"]
logs = db["logs"]

# 初期化（テスト用）
accounts.delete_many({})
logs.delete_many({})
accounts.insert_many(
    [
        {"user": "Alice", "balance": 1000},
        {"user": "Bob", "balance": 500},
        {"user": "Charlie", "balance": 0},
    ]
)


def transfer_funds(session, from_user, to_user, amount):
    from_account = accounts.find_one({"user": from_user}, session=session)

    accounts.update_one(
        {"user": from_user}, {"$inc": {"balance": -amount}}, session=session
    )
    accounts.update_one(
        {"user": to_user}, {"$inc": {"balance": amount}}, session=session
    )
    logs.insert_one(
        {"from": from_user, "to": to_user, "amount": amount}, session=session
    )

    if from_user == "Bob":
        raise ValueError(f"{from_user} の残高不足")


# 1. トランザクション（成功）
with client.start_session() as session:
    try:
        with session.start_transaction():
            transfer_funds(session, "Alice", "Bob", 100)
        print("1. トランザクション成功")
    except Exception as e:
        print("1. トランザクション失敗:", e)

# 2. トランザクション（失敗 → ロールバック）
with client.start_session() as session:
    try:
        with session.start_transaction():
            transfer_funds(session, "Bob", "Charlie", 99999)  # 残高不足
        print("2. トランザクション成功")
    except Exception as e:
        print("2. トランザクション失敗（ロールバック）:", e)

# 結果確認
print("\n残高一覧:")
for acc in accounts.find():
    print(f"{acc['user']}: {acc['balance']}")

print("\nログ一覧:")
for log in logs.find():
    print(log)
