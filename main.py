import streamlit as st
import sqlite3
import numpy as np
import pandas as pd
# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('cafe.db')
c = conn.cursor()
def fetch_all_items_as_dataframe():
    c.execute("SELECT * FROM cafe_items")
    # Fetch rows as a list of tuples
    rows = c.fetchall()
    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=['id', 'name', 'price', 'description'])
    return df

# Create table if it doesn't exist (improved for clarity)
c.execute('''CREATE TABLE IF NOT EXISTS cafe_items (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             price REAL NOT NULL,
             description TEXT
             )''')
conn.commit()

# Function to fetch all items from the database
def fetch_all_items():
    c.execute("SELECT * FROM cafe_items")
    rows = c.fetchall()
    return rows

# Function to add a new item to the database
def add_item(name, price, description):
    c.execute("INSERT INTO cafe_items (name, price, description) VALUES (?, ?, ?)", (name, price, description))
    conn.commit()
    st.success("Item added successfully!")

# Function to update an existing item
def update_item(id, name, price, description):
    c.execute("UPDATE cafe_items SET name = ?, price = ?, description = ? WHERE id = ?", (name, price, description, id))
    conn.commit()
    st.success("Item updated successfully!")

# Function to delete an item
def delete_item(id):
    c.execute("DELETE FROM cafe_items WHERE id = ?", (id,))
    conn.commit()
    st.success("Item deleted successfully!")

# Streamlit app layout and functionality
st.title("Cafe Menu Management 🤎 ☕ 🧋")

# Use sidebar for CRUD options
selected_operation = st.sidebar.selectbox("CRUD Operation", ["Create", "Read", "Update", "Delete"])

# Create operation (in sidebar)
if selected_operation == "Create":
    st.subheader("Add New Item")
    new_item_name = st.text_input("Item Name")
    new_item_price = st.number_input("Price (₹)", min_value=0.0)
    new_item_description = st.text_area("Description (Optional)")
    if st.button("Add Item"):
        add_item(new_item_name, new_item_price, new_item_description)

# Read operation (display entire table with column names)
if selected_operation == "Read":
    st.subheader("Current Menu Items")
    items_df = fetch_all_items_as_dataframe()
    if not items_df.empty:
        st.dataframe(items_df, width=800, height=400)  # Use Pandas styling
    else:
        st.info("No items found in the menu.")

# Update operation (sidebar for selecting item, main content for update form)
if selected_operation == "Update":
    items = fetch_all_items()
    if items:
        selected_item_id = st.sidebar.selectbox("Select Item to Update", [item[0] for item in items])
        if selected_item_id:
            c.execute("SELECT * FROM cafe_items WHERE id = ?", (selected_item_id,))
            item_to_update = c.fetchone()
            st.subheader("Update Item")
            updated_name = st.text_input("Item Name", item_to_update[1])
            updated_price = st.number_input("Price (₹)", min_value=0.0, value=item_to_update[2])
            updated_description = st.text_area("Description", item_to_update[3])
            if st.button("Update Item"):
                update_item(selected_item_id, updated_name, updated_price, updated_description)

# Delete operation (sidebar for selecting item, confirmation button in main content)
if selected_operation == "Delete":
    items = fetch_all_items()
    if items:
        selected_item_id = st.sidebar.selectbox("Select Item to Delete", [item[0] for item in items])
        if selected_item_id:
            if st.button("Delete Item", key="delete"):  # Added key to prevent accidental deletion
                delete_item(selected_item_id)

# Close the database connection
conn.close()
