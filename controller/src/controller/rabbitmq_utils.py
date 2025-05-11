
gpu_channels = {}
def create_channel_for_device(connection, gpu_id):
    channel = connection.channel()
    channel.queue_declare(queue='batch_queue', durable=True)
    gpu_channels[gpu_id] = channel
    return channel