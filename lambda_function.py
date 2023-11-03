import boto3
import pandas as pd
import json
import base64
import datetime


# Config AWS SNS y S3 Client
sns = boto3.client('sns', region_name='YOUR_REGION')
s3 = boto3.client('s3')

def convert_csv_and_save_s3(data, status, record):
    
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    
    today = datetime.datetime.now()
    key = f'weblogs/{status}/{today.year}/{today.month}/{today.day}/{record["recordId"]}.csv'
    s3.put_object(
            Bucket='YOUR_PROCESSED_DATA_BUCKET',
            Key=key,
            Body=csv_data,
            ContentType='text/csv'
        )

def lambda_handler(event, context):
    
    for record in event['records']:
        data = record['data']
        decoded_data = base64.b64decode(data).decode('utf-8')
        
        record_json = json.loads(decoded_data)
        
        if 'anomaly_detected' in record_json and record_json['anomaly_detected'] == [False]:
            print('Send files to S3 as Anomaly FALSE')
            data = {
                'timestamp' : record_json.get('timestamp'),
                'user_id' : record_json.get('user_id'),
                'page_url' : record_json.get('page_url'),
                'event_type' : record_json.get('event_type'),
                'element_id' : record_json.get('element_id'),
                'x_coordinate' : record_json.get('x_coordinate'),
                'y_coordinate' : record_json.get('y_coordinate'),
                'anomaly_detected' : record_json.get('anomaly_detected')
            }
            
            convert_csv_and_save_s3(data, 'PROCESSED', record)
                    
        else:
            print("Send files to S3 as Anomaly TRUE")
            user_id = record_json.get('user_id')
            anomaly_detected = record_json.get('anomaly_detected')
            detail = f'Anomaly detected with ID {user_id} and event click {anomaly_detected} in our website'
            subject = 'Anomaly Detected'
            
            # Public mesage to SNS
            sns.publish(
                TopicArn='YOUR ARN SNS',
                Message=detail,
                Subject=subject
            )
            
            convert_csv_and_save_s3(data, 'ANOMALY', record)