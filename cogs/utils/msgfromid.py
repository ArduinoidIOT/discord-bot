from discord import Client, Message


def get_message(client: Client, message_id, channel_id) -> Message:
    return client.get_channel(channel_id).fetch_message(message_id)
