# fastapi_mongos

## 概要

- mongodb をレプリカ構成で動かす.
- pymongo で操作してトランザクションを確認する.
- ユーザ・パスワードの認証設定あり

## key 作成

```shell
openssl rand -base64 756 > mongo/etc/mongod-keyfile
chmod 600 mongo/etc/mongod-keyfile
sudo chown 999 mongo/etc/mongod-keyfile
```

参考

- [MongoDB 6.0 のレプリケーション（レプリカセット）を Docker コンテナ上で構築する方法](https://n-laboratory.jp/articles/mongodb-replicaset-docker)

## docker compose 起動

ホスト OS

```shell
docker compose up --build
```

## mongo 用の init.js 実行

ホスト OS

```shell
docker exec -i fastapi_mongos-mongodb-primary-1 mongosh admin -u root -p password /docker-entrypoint-initdb.d/init.js
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

## 補足

### レプリカセット名

レプリカセットの名前は `rs0`  
以下のファイルでそれぞれ登場

- mongo/init.js
  ```javascript
  rs.initiate({
    _id: "rs0",
  ```
- docker-compose.yml
  ```yaml
  command:
    [
      "mongod",
      "--replSet",
      "rs0",
      "--bind_ip_all",
      "--auth",
      "--keyFile",
      "/etc/mongod-keyfile",
    ]
  ```
- app/mongo/transaction.py
  ```python
  client = MongoClient("mongodb://root:password@mongodb-primary:27017/?replicaSet=rs0")
  ```
