# fastapi_mongos

## 概要

- mongodb をレプリカ構成で動かす.
- pymongo で操作してトランザクションを確認する.
- ※ユーザ・パスワードの認証設定なし

## docker compose 起動

ホスト OS

```shell
docker compose up --build
```

## mongo 用の init.js 実行

ホスト OS

```shell
docker exec -i fastapi_mongos-mongodb-primary-1 mongosh /init.js
```

参考

- [Docker Compose で MongoDB のレプリカセットを構築してみた](https://zenn.dev/puchimilk/articles/54b00b8bfc8477)

## 疎通確認

fastapi コンテナにアタッチ

fastapi コンテナ内で以下を実行

```shell
python3 /app/mongo/transaction.py
```

出力が以下のようになれば成功

```shell
残高一覧:
Alice: 900
Bob: 600
Charlie: 0
```

参考

- [レプリカセットとしての Amazon DocumentDB に接続する](https://docs.aws.amazon.com/ja_jp/documentdb/latest/developerguide/connect-to-replica-set.html)
  ```
  ## Create a MongoDB client, open a connection to Amazon DocumentDB as a
  ## replica set and specify the read preference as secondary preferred
  client = pymongo.MongoClient('mongodb://<user-name>:<password>@mycluster.node.us-east-1.docdb.amazonaws.com:27017/?replicaSet=rs0')
  ```
