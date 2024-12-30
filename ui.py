import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Database connection configuration
DATABASE_URL = "postgresql://postgres:ubandroid@localhost:5432/bitcoin_db"  # Update credentials
engine = create_engine(DATABASE_URL)

# Helper function to fetch data from the database
def fetch_data(query, params=None):
    with engine.connect() as conn:
        result = pd.read_sql(query, conn, params=params)
    return result

# Streamlit UI
st.title("Blockchain Explorer")

# Tabbed UI
tab1, tab2, tab3 = st.tabs(["Search", "Blocks Explorer", "Visualizations"])

# Search Tab
with tab1:
    st.header("Search Blockchain")
    search_type = st.selectbox("Search by:", ["Blocks Hash", "Blocks Number", "Transaction Hash"])
    
    if search_type == "Blocks Hash":
        block_hash = st.text_input("Enter Blocks Hash:")
        if block_hash:
            query = "SELECT * FROM Blocks WHERE block_hash = %s"
            block_data = fetch_data(query, (block_hash,))
            if not block_data.empty:
                st.subheader("Blocks Details")
                st.dataframe(block_data)
                st.subheader("Transactions in Blocks")
                tx_query = "SELECT * FROM Transactions WHERE block_hash = %s"
                transactions = fetch_data(tx_query, (block_hash,))
                st.dataframe(transactions)
            else:
                st.warning("No block found for the given hash.")
    
    elif search_type == "Blocks Number":
        block_number = st.number_input("Enter Blocks Number:", min_value=0, step=1)
        if block_number:
            query = "SELECT * FROM Blocks WHERE block_number = %s"
            block_data = fetch_data(query, (block_number,))
            if not block_data.empty:
                st.subheader("Blocks Details")
                st.dataframe(block_data)
            else:
                st.warning("No block found for the given number.")
    
    elif search_type == "Transaction Hash":
        tx_hash = st.text_input("Enter Transaction Hash:")
        if tx_hash:
            query = "SELECT * FROM Transactions WHERE tx_hash = %s"
            transaction_data = fetch_data(query, (tx_hash,))
            if not transaction_data.empty:
                st.subheader("Transaction Details")
                st.dataframe(transaction_data)
                st.subheader("Transaction Inputs")
                tx_input_query = "SELECT * FROM TransactionInputs WHERE tx_hash = %s"
                tx_inputs = fetch_data(tx_input_query, (tx_hash,))
                st.dataframe(tx_inputs)
                st.subheader("Transaction Outputs")
                tx_output_query = "SELECT * FROM TransactionOutputs WHERE tx_hash = %s"
                tx_outputs = fetch_data(tx_output_query, (tx_hash,))
                st.dataframe(tx_outputs)
            else:
                st.warning("No transaction found for the given hash.")

# Blocks Explorer Tab
with tab2:
    st.header("Blocks Explorer")
    limit = st.number_input("Number of Blocks to Display:", min_value=1, max_value=100, value=10, step=1)
    query = "SELECT * FROM Blocks ORDER BY block_number DESC LIMIT %s"
    blocks = fetch_data(query, (limit,))
    st.dataframe(blocks)

    block_hash = st.text_input("Enter Blocks Hash to Explore:")
    if block_hash:
        st.subheader("Transactions in Blocks")
        tx_query = "SELECT * FROM Transactions WHERE block_hash = %s"
        transactions = fetch_data(tx_query, (block_hash,))
        st.dataframe(transactions)

with tab3:
    st.header("Blockchain Data Visualizations")

    st.subheader("Transaction Volume Over Time")
    query = """
    SELECT block_timestamp::date AS date, SUM(tx_output_value) AS total_transaction_volume
    FROM Transactions
    JOIN Blocks ON Transactions.block_hash = Blocks.block_hash
    GROUP BY date
    ORDER BY date;
    """
    volume_data = fetch_data(query)
    st.line_chart(volume_data.set_index("date")["total_transaction_volume"])

    st.subheader("Top Blocks by Total Transaction Value")
    query = """
    SELECT Blocks.block_hash, SUM(TransactionOutputs.value) AS total_value
    FROM Transactions
    JOIN Blocks ON Transactions.block_hash = Blocks.block_hash
    JOIN TransactionOutputs ON Transactions.tx_hash = TransactionOutputs.tx_hash
    GROUP BY Blocks.block_hash
    ORDER BY total_value DESC
    LIMIT 10;
    """
    top_blocks_data = fetch_data(query)
    st.bar_chart(top_blocks_data.set_index("block_hash")["total_value"])


    st.subheader("Average Transaction Fee Per Day")
    query = """
    SELECT block_timestamp::date AS date, AVG(tx_fee) AS avg_fee
    FROM Transactions
    JOIN Blocks ON Transactions.block_hash = Blocks.block_hash
    GROUP BY date
    ORDER BY date;
    """
    avg_fee_data = fetch_data(query)
    st.line_chart(avg_fee_data.set_index("date")["avg_fee"])

    st.subheader("Transaction Output Distribution")
    query = """
    SELECT value, COUNT(*) AS count
    FROM TransactionOutputs
    GROUP BY value
    ORDER BY count DESC
    LIMIT 20;
    """
    output_distribution = fetch_data(query)
    st.bar_chart(output_distribution.set_index("value")["count"])

    st.subheader("Transactions Per Day")
    query = """
    SELECT block_timestamp::date AS date, COUNT(*) AS transaction_count
    FROM Transactions
    JOIN Blocks ON Transactions.block_hash = Blocks.block_hash
    GROUP BY date
    ORDER BY date;
    """
    transactions_per_day = fetch_data(query)
    st.line_chart(transactions_per_day.set_index("date")["transaction_count"])

    st.subheader("Largest Transactions by Output Value")
    query = """
    SELECT tx_hash, MAX(value) AS largest_output
    FROM TransactionOutputs
    GROUP BY tx_hash
    ORDER BY largest_output DESC
    LIMIT 10;
    """
    largest_transactions = fetch_data(query)
    st.bar_chart(largest_transactions.set_index("tx_hash")["largest_output"])
