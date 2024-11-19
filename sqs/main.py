from create_queue import create_queue
from send_message import send_message
from process_message import process_message
from remove_queue import remove_queue


def main():
    name_queue = 'Ada_Fila'
    delay_seconds = '5'
    region = 'us-east-1'
    message = 'Student 01 delivered the project'
    queue_url = create_queue(name_queue, delay_seconds)
    send_message(queue_url, message)
    process_message(queue_url, region)
    remove_queue(queue_url)

if __name__ == "__main__":
    main()