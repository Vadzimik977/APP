from pytonconnect import TonConnect

import config
from tc_storage import TcStorage


def get_connector(chat_id: int):
    print('start')
    return TonConnect(config.MANIFEST_URL, storage=TcStorage(chat_id))