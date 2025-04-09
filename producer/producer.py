import json
import time
import random
from kafka import KafkaProducer

print('WAITING FOR OTHER SERVICES TO START...')
time.sleep(5)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_data():
    return {
        "id": f"meteor_{random.randint(10000, 99999)}",
        "timestamp": int(time.time()),
        "position": {
            "x": round(random.uniform(-500.0, 500.0), 2),
            "y": round(random.uniform(-500.0, 500.0), 2),
            "z": round(random.uniform(0.0, 1000.0), 2)
        },
        "vitesse": round(random.uniform(5.0, 50.0), 1),
        "taille": round(random.uniform(1.0, 50.0), 1),
        "type": random.choice(["asteroide", "comete", "bolide", "yasser"])
    }

if __name__ == "__main__":
    while True:
        data = generate_data()
        print("Producing:", data)
        producer.send('space_data', data)
        time.sleep(1)
