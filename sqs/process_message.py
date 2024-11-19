import boto3

def process_message(queue_url, region_name):
    sqs = boto3.client('sqs', region_name)

    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,  # Número máximo de mensagens a serem recebidas
        WaitTimeSeconds=10  # Tempo de espera  
    )

    # Verifica se há mensagens e exibe a primeira
    if 'Messages' in response:
        message = response['Messages'][0]
        print("Mensagem recebida:", message['Body'])

        
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
        print("Mensagem processada e excluída.")
    else:
        print("Nenhuma mensagem encontrada na fila.")