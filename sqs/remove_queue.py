import boto3

def remove_queue(queue_url):
    sqs = boto3.client('sqs', region_name='us-east-1')

    sqs.delete_queue(QueueUrl=queue_url)
    print("Fila excluída com sucesso.")