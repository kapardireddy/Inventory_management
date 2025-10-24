# Kafka CDC Pipeline (Postgres → Kafka → MongoDB)

This setup demonstrates Change Data Capture (CDC) using Postgres, Kafka, Debezium, and MongoDB — all running in Docker containers.

---

Start Docker containers:

``` bash
docker-compose up -d  
docker ps
```

---

Once Docker is running, register both connectors using Postman.  
You can open each `.sh` file (for example `register-postgres-connector.sh` and `register-mongo-sink.sh`) and copy the JSON payloads.  
Paste the entire content into Postman as a POST request to:

http://localhost:8083/connectors/

Alternatively, you can run the shell scripts directly if you prefer.

---

Access PostgreSQL through pgAdmin.

URL: http://localhost:5050  
Username and password are defined in docker-compose file.

After logging in, test db will alrady be created using the init.sql script attched to the postgre volume in docker yaml.

## Ensure to turn off the PostgreSQL server on your local machine, it might cause conflict

Run the following SQL commands:
``` pgadmin
CREATE TABLE products (
    id INT PRIMARY KEY,
    product_id INT,
    value INT
);

ALTER TABLE products REPLICA IDENTITY FULL;

SHOW wal_level;
```
The output for wal_level should be "logical".

---

Access MongoDB.

Host: localhost  
Port: 27017  
Username and password are also defined in docker-compose file.

You can connect using MongoDB Compass or from the command line:
```
mongo -u <username> -p <password>
```
---

Check connector plugin availability.

For Postgres Debezium:
```
curl http://localhost:8084/connector-plugins
```
For Kafka to MongoDB sink:
```
curl http://localhost:8085/connector-plugins
```
You should see plugins such as:
```
io.debezium.connector.postgresql.PostgresConnector  
com.mongodb.kafka.connect.MongoSinkConnector  
```
---

Insert test data into Postgres and verify CDC flow.

```
INSERT INTO products(id, product_id, value)
VALUES (1, 1, 10);
```
After running the insert, verify that the changes are reflected automatically in MongoDB in the corresponding collection..

---

(Optional) check Kafka topic messages directly inside Docker:
```
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic postgres.public.products \
  --from-beginning
```
You should see JSON change events whenever inserts, updates, or deletes occur in Postgres.

---

Useful commands:

Stop all containers:
```
docker-compose down
```
Rebuild containers (if configuration changed):
```
docker-compose up -d --build
```
List active connectors:
```
curl http://localhost:8083/connectors
```
Delete a connector:
```
curl -X DELETE http://localhost:8083/connectors/<connector-name>
```
---

Summary of ports:

PostgreSQL - 5432  
pgAdmin - 5050  
Kafka Broker - 9092  
Kafka Connect - 8083  
Debezium - 8084  
MongoDB - 27017  
MongoDB Sink - 8085  

---

Expected data flow:

Postgres → Debezium Source Connector → Kafka Topic → MongoDB Sink Connector → MongoDB

Any insert, update, or delete in Postgres is captured by Debezium, published to Kafka, and written to MongoDB automatically.

---

Author: Kapardi Reddy
Project: Kafka CDC with Postgres and MongoDB  
License: MIT
