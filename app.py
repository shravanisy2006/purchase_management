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

import random

if st.button("Generate Realistic Data"):
    supplier_names = [
        "ABC Traders", "Sharma Supplies", "Global Distributors",
        "Mahalaxmi Enterprises", "Om Sai Traders", "Prime Wholesale",
        "Reliance Supply Co.", "Kiran Enterprises", "Vijay Suppliers",
        "Metro Distributors"
    ]

    product_names = [
        "Laptop", "Keyboard", "Mouse", "Monitor", "Printer",
        "USB Cable", "Hard Disk", "Router", "SSD", "Graphics Card"
    ]

    # Suppliers
    for i in range(50):
        name = random.choice(supplier_names) + f" {i}"
        contact = "9" + str(random.randint(100000000, 999999999))
        address = f"Pune Area {random.randint(1, 20)}"
        c.execute("INSERT INTO supplier(name, contact, address) VALUES (?, ?, ?)",
                  (name, contact, address))

    # Products
    for i in range(70):
        name = random.choice(product_names)
        price = random.randint(500, 50000)
        quantity = random.randint(1, 100)
        c.execute("INSERT INTO product(name, price, quantity) VALUES (?, ?, ?)",
                  (name, price, quantity))

    # Purchases
    for i in range(100):
        supplier_id = random.randint(1, 50)
        total = random.randint(1000, 100000)
        c.execute("INSERT INTO purchase(supplier_id, total) VALUES (?, ?)",
                  (supplier_id, total))

    conn.commit()
    st.success("Realistic Data Generated!")
menu = ["Supplier", "Product", "Purchase"]
choice = st.sidebar.selectbox("Menu", menu)

# Supplier
if choice == "Supplier":
    st.subheader("Delete Supplier")

    delete_id = st.number_input("Enter Supplier ID to delete", step=1)

    if st.button("Delete Supplier"):
        c.execute("DELETE FROM supplier WHERE id = ?", (delete_id,))
        conn.commit()
        st.success("Supplier Deleted!")
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
    st.subheader("Delete Product")

    delete_id = st.number_input("Enter Product ID to delete", step=1)

    if st.button("Delete Product"):
        c.execute("DELETE FROM product WHERE id = ?", (delete_id,))
        conn.commit()
        st.success("Product Deleted!")
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
    st.subheader("Delete Purchase")

    delete_id = st.number_input("Enter Purchase ID to delete", step=1)
    
    if st.button("Delete Purchase"):
        c.execute("DELETE FROM purchase WHERE id = ?", (delete_id,))
        conn.commit()
        st.success("Purchase Deleted!")
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
