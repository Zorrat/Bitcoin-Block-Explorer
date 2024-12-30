
-- Indexes on Transactions Table
CREATE INDEX idx_transactions_block_hash ON Transactions(block_hash); 
CREATE INDEX idx_transactions_tx_fee ON Transactions(tx_fee); 
CREATE INDEX idx_transactions_tx_output_value ON Transactions(tx_output_value); 

-- Indexes on TransactionInput Table
CREATE INDEX idx_transactioninput_tx_hash ON TransactionInputs(tx_hash); 

-- Indexes on TransactionOutput Table
CREATE INDEX idx_transactionoutput_tx_hash ON TransactionOutputs(tx_hash); 
CREATE INDEX idx_transactionoutput_value ON TransactionOutputs(value); 

CLUSTER Transactions USING idx_transactions_block_hash;

-- Composite index on block_hash and tx_fee
CREATE INDEX idx_transactions_block_hash_tx_fee ON Transactions(block_hash, tx_fee);


