import streamlit as st
import sqlite3

conn = sqlite3.connect("purchase.db", check_same_thread=False)
c = conn.cursor()

# Tables
c.execute("CREATE TABLE IF NOT EXISTS supplier(id INTEGER PRIMARY KEY, name TEXT, contact TEXT, address TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS purchase(id INTEGER PRIMARY KEY, supplier_id INTEGER, total REAL)")

st.title("🛒 Purchase Management System")

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

    st.write(c.execute("SELECT * FROM supplier").fetchall())

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

    st.write(c.execute("SELECT * FROM product").fetchall())

# Purchase
elif choice == "Purchase":
    st.subheader("Record Purchase")
    supplier_id = st.number_input("Supplier ID")
    total = st.number_input("Total Amount")

    if st.button("Record Purchase"):
        c.execute("INSERT INTO purchase(supplier_id, total) VALUES (?, ?)", (supplier_id, total))
        conn.commit()
        st.success("Recorded!")

    st.write(c.execute("SELECT * FROM purchase").fetchall())
