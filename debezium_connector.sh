curl --location --request POST 'http://localhost:8084/connectors/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "names-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "plugin.name": "pgoutput",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname": "test",
    "topic.prefix": "postgres",
    "table.include.list": "public.products,public.totals",
    "slot.name": "names_slot",
    "publication.name": "names_pub",

    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "value.converter.schemas.enable": "false",

    "decimal.handling.mode": "double",
    "snapshot.mode": "initial",
    "capture.old.data": "true"
  }
}'
