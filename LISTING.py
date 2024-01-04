import asyncio
import json
import requests
from pytoniq_core import Cell, StateInit, Builder, begin_cell, Address
from pytoniq import LiteClient, Contract, WalletV4R2

# ДЛЯ ОТПРАВКИ ТРАНСФЕРА
def form(data: dict):
    return begin_cell()\
            .store_uint(0, 32)\
            .store_snake_string('data:application/json,' \
                + json.dumps(data, separators=(',', ':')))\
           .end_cell()
def transfer(amount: int, ticker: str, recipient: str):
    return form({
        "p": "ton-20",
        "op": "transfer",
        "tick": ticker,
        "to": recipient,
        "amt": str(int(amount * 1e9))
    })

# ЗАПРОС С DTON и ФОРМИРОВАНИЕ state_init
tick='dedust.io'
list_amount=1
unit_price=1
mnemo='MY_MNEMO'
endpoint = 'https://dton.io/graphql/'
query = f'''
  query {{
    ton20listing(
      tick: "{tick}"
      initiator: "UQCk-Q27rbvLfSiY52SQepu7XPt4dt7wBHu9ZB3dkJKfB0qW"
      amt: "{list_amount}"
      ton_price: "{unit_price}"
    ) {{
      address
      stateInit
      payload
      amount
      __typename
    }}
  }}
'''

response = requests.post(endpoint, json={'query': query})
data = response.json()
state1=data["data"]["ton20listing"][0]["stateInit"]

if response.status_code == 200:
    data = response.json()
    address_1=data["data"]["ton20listing"][0]["address"]
    s3 = Address(address_1).to_str(True, True, False)
    print(address_1)
    amount_1 = data["data"]["ton20listing"][0]["amount"]
    print(amount_1)
    payload_1 = data["data"]["ton20listing"][0]["payload"]
    # print(payload_1)
    state1=data["data"]["ton20listing"][0]["stateInit"]
    # print(state1)
    adrress_2 = data["data"]["ton20listing"][1]["address"]
    s4=Address(adrress_2).to_str(True, True, False)
    print(adrress_2)
    amount_2 = data["data"]["ton20listing"][1]["amount"]
    print(amount_2)
    payload_2 = data["data"]["ton20listing"][1]["payload"]
    # print(payload_2)
    state2=data["data"]["ton20listing"][1]["stateInit"]


# ПРЕОБРАЗОВАНИЕ STATE_INIT В ТРЕБУЕМЫЙ ФОРМАТ

code_boc = f'{state1}'
COUNTER_CODE = Cell.one_from_boc(code_boc)
data = begin_cell().store_uint(1, 32).store_uint(0, 32).end_cell()
state_init = StateInit(code=COUNTER_CODE, data=data)

address = Address((0, state_init.serialize().hash))

print(address.to_str(is_bounceable=True))

# ДЕПЛОЙ КОНТРАКТА И СОЗДАНИЕ ТРАНСФЕРА TON-20 токена
async def deploy():
    client = LiteClient.from_mainnet_config(7, trust_level=1)
    await client.connect()
    wallet = await WalletV4R2.from_mnemonic(client, mnemo, 0)
    print(wallet)
    # ТРАНСФЕР
    body=transfer(list_amount,tick,address_1)
    msg1=wallet.create_wallet_internal_message(destination=address,state_init=state2,value=int(amount_2),body=body)
    #ДЕПЛОЙ
    contract = await Contract.from_state_init(client, 0, state_init)
    print(contract.state_init)
    print(contract.address)
    print(contract.is_active)
    print(contract.account)

    # ВЫЗОВ КОНТРАКТА
    msg = await wallet.transfer(
        destination=address,
        amount=int(amount_1),
        body=begin_cell()
            .store_uint(0x7038d7ea, 32)
            .store_uint(0, 64)
            .store_uint(10, 32)
            .end_cell(),
        state_init=state_init
    )
    # ОТПРАВКА ТРАНСФЕРА И ВЫЗОВ КОНТРАКТА
    result = await wallet.raw_transfer(msgs=[msg,msg1])
    print(result)
    print(contract)



    await client.close()

    print(contract)
if __name__ == '__main__':
    await deploy()
