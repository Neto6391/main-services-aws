import json
import logging
import boto3
from botocore.exceptions import ClientError
import re

AWS_REGION = 'us-east-1'
LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

sns_client = boto3.client('sns', region_name=AWS_REGION)

def validate_phone_number(phone_number):
    cleaned_number = re.sub(r'[\s\-\(\)]', '', phone_number)
    
    if re.match(r'^\+[1-9]\d{1,14}$', cleaned_number):
        return cleaned_number
    
    if re.match(r'^(\+?55)?(\d{10,11})$', cleaned_number):
        return f'+55{cleaned_number[-11:]}' if not cleaned_number.startswith('+') else cleaned_number
    
    logger.error(f"Número de telefone inválido: {phone_number}")
    return None

def create_topic(name):
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info(f"Tópico {name} criado com sucesso.")
        return topic
    except ClientError as e:
        logger.error(f"Erro ao criar tópico {name}: {e}")
        raise

def create_email_subscription(topic_arn, email):
    try:
        subscription = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email,
            Attributes={
                'FilterPolicy': json.dumps({
                    'type': ['email']
                })
            },
            ReturnSubscriptionArn=True
        )
        logger.info(f"E-mail {email} inscrito no tópico {topic_arn}")
        return subscription
    except ClientError as e:
        logger.error(f"Erro ao criar subscrição de e-mail: {e}")
        raise

def create_sms_subscription(topic_arn, phone_number):
    validated_number = validate_phone_number(phone_number)
    if not validated_number:
        logger.error(f"Número de telefone inválido: {phone_number}")
        raise ValueError(f"Número de telefone inválido: {phone_number}")
    
    try:
        subscription = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='sms',
            Endpoint=validated_number,
            Attributes={
                'FilterPolicy': json.dumps({
                    'type': ['sms']
                })
            },
            ReturnSubscriptionArn=True
        )
        logger.info(f"Número {validated_number} inscrito no tópico {topic_arn}")
        return subscription
    except ClientError as e:
        logger.error(f"Erro ao criar subscrição de SMS: {e}")
        raise

def publish_filtered_message(topic_arn, message, message_type):
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageAttributes={
                'type': {
                    'DataType': 'String',
                    'StringValue': message_type
                }
            }
        )
        
        message_id = response['MessageId']
        logger.info(f"Mensagem {message_type} enviada com sucesso. ID: {message_id}")
        return message_id
    except ClientError as e:
        logger.error(f"Erro ao publicar mensagem {message_type}: {e}")
        raise

def publish_sms(topic_arn, subject, message):
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject,
            MessageStructure='raw'
        )
        message_id = response['MessageId']
        logger.info(f"Mensagem enviada com sucesso. ID: {message_id}")
        return message_id
    except ClientError as e:
        logger.error(f"Erro ao publicar mensagem: {e}")
        raise

def send_multiformat_email(topic_arn, subject, message_dict):
    try:
        message_json = json.dumps(message_dict)
        
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message_json,
            Subject=subject,
            MessageStructure='json'
        )
        message_id = response['MessageId']
        logger.info(f"Mensagem multiformato enviada. ID: {message_id}")
        return message_id
    except ClientError as e:
        logger.error(f"Erro ao enviar mensagem multiformato: {e}")
        raise

def main():
    try:
        topic_name = 'spider-web-topic'
        
        topic = create_topic(topic_name)
        topic_arn = topic['TopicArn']
        
        emails = [
            'XXXX@gmail.com',
        ]

        phone_numbers  = [
            '+55XXXXXXXXXXX',
        ]
        
        for email in emails:
            create_email_subscription(topic_arn, email)

        for phone in phone_numbers:
            create_sms_subscription(topic_arn, phone)
        
        publish_filtered_message(
            topic_arn, 
            "Mensagem de teste para e-mail", 
            'email'
        )
        
        publish_filtered_message(
            topic_arn, 
            "Mensagem de teste para SMS", 
            'sms'
        )
        
    except Exception as e:
        logger.error(f"Erro no processo: {e}")

if __name__ == "__main__":
    main()