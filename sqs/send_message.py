
import boto3

def send_message(queue_url, message_body):
    sqs = boto3.client('sqs', region_name='us-east-1')
    print(queue_url)
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )

    print("Mensagem enviada com sucesso. ID da mensagem:", response['MessageId'])