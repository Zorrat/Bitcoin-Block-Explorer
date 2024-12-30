
CREATE TABLE Blocks (
    block_hash TEXT PRIMARY KEY,
    block_size BIGINT,   
    block_stripped_size BIGINT,   
    block_weight BIGINT,   
    block_number BIGINT,   
    block_version INTEGER,
    block_merkle_root TEXT,
    block_timestamp TIMESTAMP,
    block_nonce TEXT,
    block_bits TEXT,
    block_coinbase_param TEXT,
    block_transaction_count BIGINT   
);

CREATE TABLE BlockReference (
    block_hash TEXT PRIMARY KEY REFERENCES Blocks(block_hash),
    block_timestamp TIMESTAMP
);


CREATE TABLE Transactions (
    tx_hash TEXT PRIMARY KEY,
    tx_size BIGINT,   
    tx_virtual_size BIGINT,   
    tx_version INTEGER,
    tx_lock_time BIGINT,   
    block_hash TEXT,
    tx_is_coinbase BOOLEAN,
    tx_index BIGINT,   
    tx_input_count BIGINT,   
    tx_output_count BIGINT,   
    tx_input_value BIGINT,   
    tx_output_value BIGINT,   
    tx_fee BIGINT,   
    FOREIGN KEY (block_hash) REFERENCES Blocks(block_hash)
);

CREATE TABLE TransactionInputs (
    tx_hash TEXT,
    input_index BIGINT,   
    prev_tx_hash TEXT,
    prev_output_index BIGINT,   
    script_asm TEXT,
    script_hex TEXT,
    sequence BIGINT,
    PRIMARY KEY (tx_hash, input_index),
    FOREIGN KEY (tx_hash) REFERENCES Transactions(tx_hash)
);

CREATE TABLE TransactionOutputs (
    tx_hash TEXT,
    output_index BIGINT,   
    value BIGINT,   
    script_asm TEXT,
    script_hex TEXT,
    PRIMARY KEY (tx_hash, output_index),
    FOREIGN KEY (tx_hash) REFERENCES Transactions(tx_hash)
);
