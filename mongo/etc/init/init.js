rs.initiate({
  _id: "rs0",
  members: [
    // コンテナの hostname と port を指定
    // priority は優先順位を決める値（任意）
    { _id: 0, host: "mongodb-primary:27017", priority: 100 },
    { _id: 1, host: "mongodb-secondary:27017", priority: 10 },
  ],
});

// docker exec -i fastapi_mongos-mongodb-primary-1 mongosh /init.js
// docker exec -i fastapi_mongos-mongodb-primary-1 mongosh admin -u root -p password /docker-entrypoint-initdb.d/init.js
