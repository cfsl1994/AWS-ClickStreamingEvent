#######################
# ClickStreamingEvent #
#######################

import boto3
import random
import datetime
import time
import json

# 1. Create a client for Kinesis Data Firehose
firehose_client = boto3.client('firehose',
                                aws_access_key_id='YOUR_ACCESS_KEY_ID',
                                aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
                                region_name='YOUR_REGION')


# 2. Function for generate random click event
def generar_evento_clic():
    evento = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": random.randint(1, 1000),
        "page_url": f"/pagina-{random.randint(1, 10)}",
        "event_type": "click",
        "element_id": f"boton-{random.randint(1, 10)}",
        "x_coordinate": random.randint(0, 1920),  # Resolución típica de pantalla
        "y_coordinate": random.randint(0, 1080),  # Resolución típica de pantalla
        "anomaly_detected": random.choices([True, False])  # Indica si es un evento anómalo
    }

    return evento

# 3. Send stream data to Kinesis Data Firehose
while True:

  data_streaming = json.dumps(generar_evento_clic())+ '\n'
  time.sleep(1)
  print(data_streaming)

  response = firehose_client.put_record(
  DeliveryStreamName='ClickStreamingFirehose',
  Record={
        'Data': data_streaming  # Los datos en formato JSON
    }
  )