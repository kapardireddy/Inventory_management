import time
import json
import psycopg2
from kafka import KafkaConsumer

POSTGRES_CONN = {
    'host': 'postgres',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'dbname': 'test'
}


for attempt in range(10):
    try:
        conn = psycopg2.connect(**POSTGRES_CONN)
        cursor = conn.cursor()
        print("Connected to Postgres")
        break
    except psycopg2.OperationalError as e:
        print(f"Postgres not ready (attempt {attempt+1}/10): {e}")
        time.sleep(3)
else:
    raise Exception("Could not connect to Postgres after 10 tries.")

print(" Connecting to Kafka at kafka:29092")
consumer = KafkaConsumer(
    'postgres.public.products',
    bootstrap_servers='kafka:29092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='products-aggregator',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
)
print("Connected to Kafka. Waiting for messages...")

for message in consumer:
    value = message.value

    if value is None:
        print("Received message where value = None.So, skipping.")
        continue

    if 'op' not in value:
        print("Skipping message without op:", value)
        continue

    op = value['op']
    before = value.get('before')
    after = value.get('after')

    print(f"Kafka Event Received:")
    print(f"Operation: {op.upper()}")
    print(f"Before: {json.dumps(before, indent=2)}")
    print(f"After:  {json.dumps(after, indent=2)}")

    try:
        if op == 'c':  # INSERT
            product_id = after['product_id']
            val = after['value']
            cursor.execute("""
                INSERT INTO totals (product_id, total)
                VALUES (%s, %s)
                ON CONFLICT (product_id) DO UPDATE
                SET total = totals.total + EXCLUDED.total
            """, (product_id, val))

        elif op == 'u':  # UPDATE
            product_id = after['product_id']
            delta = after['value'] - before['value']
            cursor.execute("""
                UPDATE totals SET total = total + %s WHERE product_id = %s
            """, (delta, product_id))

        elif op == 'd':  # DELETE
            product_id = before['product_id']
            val = before['value']
            cursor.execute("""
                UPDATE totals SET total = total - %s WHERE product_id = %s
            """, (val, product_id))

        conn.commit()
        print(f"Processed {op.upper()} for product_id={product_id}")

    except Exception as e:
        conn.rollback()
        print(f"Error processing message: {e}")
