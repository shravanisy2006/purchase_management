import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("purchase.db", check_same_thread=False)
c = conn.cursor()

# Tables
c.execute("CREATE TABLE IF NOT EXISTS supplier(id INTEGER PRIMARY KEY, name TEXT, contact TEXT, address TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS purchase(id INTEGER PRIMARY KEY, supplier_id INTEGER, total REAL)")

st.title("🛒 Purchase Management System")

if st.button("Generate Dummy Data"):
    # Suppliers
    for i in range(1, 21):
        c.execute("INSERT INTO supplier(name, contact, address) VALUES (?, ?, ?)",
                  (f"Supplier {i}", f"99999{i:05}", f"Address {i}"))

    # Products
    for i in range(1, 31):
        c.execute("INSERT INTO product(name, price, quantity) VALUES (?, ?, ?)",
                  (f"Product {i}", i*10, i*5))

    # Purchases
    for i in range(1, 51):
        c.execute("INSERT INTO purchase(supplier_id, total) VALUES (?, ?)",
                  (i % 20 + 1, i * 100))

    conn.commit()
    st.success("Dummy Data Generated!")
menu = ["Supplier", "Product", "Purchase"]
choice = st.sidebar.selectbox("Menu", menu)

# Supplier
if choice == "Supplier":
    st.subheader("Add Supplier")
    name = st.text_input("Name")
    contact = st.text_input("Contact")
    address = st.text_input("Address")

    if st.button("Add Supplier"):
        c.execute("INSERT INTO supplier(name, contact, address) VALUES (?, ?, ?)", (name, contact, address))
        conn.commit()
        st.success("Added!")


    data = c.execute("SELECT * FROM supplier").fetchall()
    df = pd.DataFrame(data, columns=["ID", "Name", "Contact", "Address"])
    st.table(df)

# Product
elif choice == "Product":
    st.subheader("Add Product")
    name = st.text_input("Product Name")
    price = st.number_input("Price")
    quantity = st.number_input("Quantity")

    if st.button("Add Product"):
        c.execute("INSERT INTO product(name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        st.success("Added!")

    data = c.execute("SELECT * FROM product").fetchall()
    df = pd.DataFrame(data, columns=["ID", "Name", "Price", "Quantity"])
    st.table(df)

# Purchase
elif choice == "Purchase":
    st.subheader("Record Purchase")
    supplier_id = st.number_input("Supplier ID")
    total = st.number_input("Total Amount")

    if st.button("Record Purchase"):
        c.execute("INSERT INTO purchase(supplier_id, total) VALUES (?, ?)", (supplier_id, total))
        conn.commit()
        st.success("Recorded!")

    data = c.execute("SELECT * FROM purchase").fetchall()
    df = pd.DataFrame(data, columns=["ID", "Supplier_ID", "Total"])
    st.table(df)
