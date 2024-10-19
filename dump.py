import sys
import json

from leap.cleos import CLEOS
from leap.protocol import Name

endpoint = sys.argv[1]

cleos = CLEOS(endpoint=endpoint)

block_num = cleos.get_info()['head_block_num']

print(f'dumping evm at height {block_num}')

config = cleos.get_table('eosio.evm', 'eosio.evm', 'config')[0]

print(f'got config {config}')

accounts = cleos.get_table('eosio.evm', 'eosio.evm', 'account', key_type='i64')

print(f'got {len(accounts)} accounts.')

storage = {}
for account in accounts:
    del account['code']
    addr = account['address']
    idx = account['index']
    accountstate = cleos.get_table('eosio.evm', str(Name.from_int(idx)), 'accountstate')
    storage[addr] = accountstate

    print(f'got storage for {addr}, index {idx}')

with open('dump.json', 'w+') as dump_file:
    data = {
        'block_num': block_num,
        'config': config,
        'accounts': accounts,
        'storage': storage
    }
    json.dump(data, dump_file, indent=4)

print('json dump done')
