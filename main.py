import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💸 Personal Expense Tracker")

# Input form
with st.form("expense_form"):
    exp_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Other"])
    desc = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_data = pd.DataFrame([[exp_date, category, desc, amount]],
                            columns=["Date", "Category", "Description", "Amount"])
    try:
        old_data = pd.read_csv("data.csv")
        data = pd.concat([old_data, new_data], ignore_index=True)
    except FileNotFoundError:
        data = new_data
    data.to_csv("data.csv", index=False)
    st.success("Expense added successfully!")

# Analysis
if st.button("📊 Show Analysis"):
    df = pd.read_csv("data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    # Pie chart
    category_sum = df.groupby("Category")["Amount"].sum()
    st.subheader("Category-wise Spending")
    st.pyplot(category_sum.plot.pie(autopct='%1.1f%%', figsize=(6,6)).get_figure())

    # Line chart
    month_sum = df.groupby("Month")["Amount"].sum()
    st.subheader("Monthly Spending")
    st.line_chart(month_sum)

    # Raw data
    st.subheader("📄 All Expenses")
    st.dataframe(df.sort_values("Date", ascending=False))