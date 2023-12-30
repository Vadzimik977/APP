from pytoniq.contract.wallets import WalletV3R2,Wallet,BaseWallet,WalletV3,WalletV3R1,WalletV4R2
from pytoniq import Address
from pytoniq import LiteClient
import base64
import json
from pytoniq_core import begin_cell,StateInit
from base64 import urlsafe_b64encode
import requests
import asyncio
import time
from pytoniq.liteclient.balancer import LiteBalancer
from pytoniq_core.boc import Cell
from pytoniq_core.crypto.keys import private_key_to_public_key, mnemonic_to_private_key
provider = LiteBalancer.from_mainnet_config(trust_level=1)
mnemonics='MY_MNEMO'

await provider.start_up()


wallet=await  WalletV4R2.from_mnemonic(provider=provider,mnemonics=mnemonics)
print(wallet.wallet_id)
s=await wallet.get_account_state()
print(s)
j=await wallet.get_balance()
print(j)



def form(data: dict):
    return begin_cell()\
            .store_uint(0, 32)\
            .store_snake_string('data:application/json,' \
                + json.dumps(data, separators=(',', ':')))\
           .end_cell()
def transfer(amount: int, ticker: str, recipient: str):
    return ({
        "p": "ton-20",
        "op": "transfer",
        "tick": ticker,
        "to": recipient,
        "amt": amount,
        "memo":""
    })



try:
    w = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)
    # Получение строкового представления адреса кошелька w
    ss = w.address.to_str()
        # Преобразование адреса в строку с использованием класса Address
    s2 = Address(ss).to_str(True, True, False)
        # Получение баланса кошелька w
    bal = await w.get_balance()
    print(bal)
        # # Вывод информации о текущем кошельке, его адресе и балансе
    print(s2, ss, "%.2f" % (bal / 1000000000))
    tick='nano'
    list_amount='1'
    unit_price='1'
    # Иницилиазация смарт-контракта
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
    if response.status_code == 200:
        data = response.json()
        address_1=data["data"]["ton20listing"][0]["address"]
        s3 = Address(address_1).to_str(True, True, False)
        amount_1 = data["data"]["ton20listing"][0]["amount"]
        payload_1 = data["data"]["ton20listing"][0]["payload"]
        state1=data["data"]["ton20listing"][0]["stateInit"]
        # print(state1)
        adrress_2 = data["data"]["ton20listing"][1]["address"]
        s4=Address(adrress_2).to_str(True, True, False)
        amount_2 = data["data"]["ton20listing"][1]["amount"]
        payload_2 = data["data"]["ton20listing"][1]["payload"]
        state2=data["data"]["ton20listing"][1]["stateInit"]

        body = transfer(amount_2,tick,adrress_2)

        code_boc = f'{state1}'
        COUNTER_CODE = Cell.one_from_boc(code_boc)

        data = begin_cell().store_uint(1, 32).store_uint(0, 32).end_cell()

        state_init = StateInit(code=COUNTER_CODE, data=data)

        body2=deploy_transaction(address_1,amount_1,payload_1,state1)

        msg=wallet.create_wallet_internal_message(destination=Address(s2),state_init=state_init,value=int(amount_1),body=begin_cell().store_uint(0x7038d7ea, 32).store_uint(0, 64).store_uint(10, 32).end_cell())
        msg1=wallet.create_wallet_internal_message(destination=Address(s2),state_init=state2,value=int(amount_2),body=body)
        result = await wallet.raw_transfer(msgs=[msg,msg1])



        print('Success')
   # за в выполнении на 3 секунды, вероятно, для ожидания завершения транзакции
   #   await asyncio.sleep(3)
    await provider.close_all()

except Exception as e:
    # Обработка исключений с выводом ошибки и ожидание 3 секунд
    print(e)
    await asyncio.sleep(3)
    # Закрытие клиента provider
    await provider.close()
await provider.close_all()




