-- On Delete Cascade 
ALTER TABLE Transactions
ADD CONSTRAINT fk_block_hash
FOREIGN KEY (block_hash) REFERENCES Block(block_hash) ON DELETE CASCADE;

ALTER TABLE TransactionInput
ADD CONSTRAINT fk_tx_hash_input
FOREIGN KEY (tx_hash) REFERENCES Transactions(tx_hash) ON DELETE CASCADE;

ALTER TABLE TransactionOutput
ADD CONSTRAINT fk_tx_hash_output
FOREIGN KEY (tx_hash) REFERENCES Transactions(tx_hash) ON DELETE CASCADE;

ALTER TABLE Transactions
ADD CONSTRAINT check_tx_fee_positive CHECK (tx_fee >= 0);

ALTER TABLE Block
ADD CONSTRAINT check_block_weight_positive CHECK (block_weight > 0);
