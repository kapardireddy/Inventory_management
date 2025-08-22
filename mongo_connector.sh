curl --location --request POST 'http://localhost:8085/connectors/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "mongo-sink-connector",
  "config": {
    "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
    "tasks.max": "1",
    "topics": "postgres.public.products,postgres.public.totals",
    "connection.uri": "mongodb://mongo:27017",
    "database": "inventory_cdc",
    "collection": "changes",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",

    "writemodel.strategy": "com.mongodb.kafka.connect.sink.writemodel.strategy.InsertOneDefaultStrategy",
    "document.id.strategy": "com.mongodb.kafka.connect.sink.processor.id.strategy.UuidStrategy",

    "errors.tolerance": "all",
    "errors.log.enable": "true",
    "errors.log.include.messages": "true"
  }
}'
