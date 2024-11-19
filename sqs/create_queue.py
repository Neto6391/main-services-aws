import boto3


def create_queue(name_queue, delaySeconds):
    sqs = boto3.client('sqs', region_name='us-east-1') 

    # Cria a fila SQS
    response = sqs.create_queue(
        QueueName=name_queue,
        Attributes={
            'DelaySeconds': delaySeconds # Atraso opcional para as mensagens
        }
    )

    # Obtém a URL da fila criada
    queue_url = response['QueueUrl']
    print("Fila criada com sucesso. URL da Fila:", queue_url)
    return queue_url