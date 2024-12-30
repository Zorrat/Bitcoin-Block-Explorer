import json
import pandas as pd
from sqlalchemy import create_engine

blocks_file = 'blocks.json'
transactions_file = 'transactions.json'

DATABASE_URL = "postgresql://postgres:ubandroid@127.0.0.1:5432/bitcoin_db" 


engine = create_engine(DATABASE_URL)

blocks_df = pd.read_json(blocks_file, lines=True)
blocks_df = blocks_df.rename(columns={
    'hash': 'block_hash',
    'size': 'block_size',
    'stripped_size': 'block_stripped_size',
    'weight': 'block_weight',
    'number': 'block_number',
    'version': 'block_version',
    'merkle_root': 'block_merkle_root',
    'timestamp': 'block_timestamp',
    'nonce': 'block_nonce',
    'bits': 'block_bits',
    'coinbase_param': 'block_coinbase_param',
    'transaction_count': 'block_transaction_count'
})

block_reference_df = blocks_df[['block_hash', 'block_timestamp']].drop_duplicates()

def load_blocks():
    blocks_df.to_sql('blocks', engine, if_exists='append', index=False)
    block_reference_df.to_sql('blockreference', engine, if_exists='append', index=False)
    print("Blocks and BlockReference data loaded successfully.")

def load_transactions(batch_size=10000):
    transactions_batch = []
    inputs_batch = []
    outputs_batch = []

    with open(transactions_file, 'r') as f:
        with engine.connect() as conn:
            for line_num, line in enumerate(f, start=1):
                transaction = json.loads(line)

                # Prepare transaction data
                transactions_batch.append({
                    'tx_hash': transaction['hash'],
                    'tx_size': transaction['size'],
                    'tx_virtual_size': transaction['virtual_size'],
                    'tx_version': transaction['version'],
                    'tx_lock_time': transaction['lock_time'],
                    'block_hash': transaction['block_hash'],
                    'tx_is_coinbase': transaction['is_coinbase'],
                    'tx_index': transaction['index'],
                    'tx_input_count': transaction['input_count'],
                    'tx_output_count': transaction['output_count'],
                    'tx_input_value': transaction['input_value'],
                    'tx_output_value': transaction['output_value'],
                    'tx_fee': transaction['fee']
                })

        
                for input_item in transaction['inputs']:
                    inputs_batch.append({
                        'tx_hash': transaction['hash'],
                        'input_index': input_item.get('index'),
                        'prev_tx_hash': input_item.get('prev_tx_hash'),
                        'prev_output_index': input_item.get('prev_output_index'),
                        'script_asm': input_item.get('script_asm'),
                        'script_hex': input_item.get('script_hex'),
                        'sequence': input_item.get('sequence')
                    })

                
                for output_item in transaction['outputs']:
                    outputs_batch.append({
                        'tx_hash': transaction['hash'],
                        'output_index': output_item.get('index'),
                        'value': output_item.get('value'),
                        'script_asm': output_item.get('script_asm'),
                        'script_hex': output_item.get('script_hex')
                    })

                
                if line_num % batch_size == 0:
                    pd.DataFrame(transactions_batch).to_sql('transactions', conn, if_exists='append', index=False)
                    pd.DataFrame(inputs_batch).to_sql('transactioninputs', conn, if_exists='append', index=False)
                    pd.DataFrame(outputs_batch).to_sql('transactionoutputs', conn, if_exists='append', index=False)

                    # Clear batches
                    transactions_batch.clear()
                    inputs_batch.clear()
                    outputs_batch.clear()
                    print(f"Processed {line_num} transactions...")

            # Insert remaining records after the last batch
            if transactions_batch:
                pd.DataFrame(transactions_batch).to_sql('transactions', conn, if_exists='append', index=False)
            if inputs_batch:
                pd.DataFrame(inputs_batch).to_sql('transactioninputs', conn, if_exists='append', index=False)
            if outputs_batch:
                pd.DataFrame(outputs_batch).to_sql('transactionoutputs', conn, if_exists='append', index=False)

    print("Transaction data loaded successfully.")


if __name__ == "__main__":

    load_blocks()
    load_transactions(batch_size=100000)
    print("Database created and populated successfully.")
  