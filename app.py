import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Expense Tracker")
st.write("Track and analyze your daily expenses.")

# Initialize expense data
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# -----------------------------
# Add Expense
# -----------------------------

st.subheader("➕ Add Expense")

col1, col2 = st.columns(2)

with col1:
    date = st.date_input("Date")

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Entertainment", "Bills", "Other"]
    )

with col2:
    description = st.text_input("Description")

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0
    )

if st.button("Add Expense"):

    if amount > 0:

        expense = {
            "Date": date,
            "Category": category,
            "Description": description,
            "Amount": amount
        }

        st.session_state.expenses.append(expense)

        st.success("Expense added successfully! ✅")

    else:
        st.warning("Please enter an amount greater than 0.")


# -----------------------------
# Convert to DataFrame
# -----------------------------

df = pd.DataFrame(st.session_state.expenses)


if len(df) > 0:

    st.divider()

    # -----------------------------
    # Expense Summary
    # -----------------------------

    st.subheader("📊 Expense Summary")

    total_expense = np.sum(df["Amount"])
    average_expense = np.mean(df["Amount"])
    highest_expense = np.max(df["Amount"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Expense", f"₹{total_expense:.2f}")
    col2.metric("Average Expense", f"₹{average_expense:.2f}")
    col3.metric("Highest Expense", f"₹{highest_expense:.2f}")


    # -----------------------------
    # All Expenses
    # -----------------------------

    st.subheader("📋 All Expenses")

    st.dataframe(
        df,
        use_container_width=True
    )


    # -----------------------------
    # Category-wise Analysis
    # -----------------------------

    category_expense = df.groupby("Category")["Amount"].sum()

    st.subheader("📈 Category-wise Expenses")

    fig, ax = plt.subplots()

    category_expense.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Amount (₹)")
    ax.set_title("Category-wise Expenses")

    st.pyplot(fig)


    # -----------------------------
    # Pie Chart
    # -----------------------------

    st.subheader("🥧 Expense Distribution")

    fig2, ax2 = plt.subplots()

    ax2.pie(
        category_expense,
        labels=category_expense.index,
        autopct="%.1f%%"
    )

    ax2.set_title("Expense Distribution")

    st.pyplot(fig2)


    # -----------------------------
    # Delete All Expenses
    # -----------------------------

    if st.button("🗑️ Delete All Expenses"):

        st.session_state.expenses = []

        st.rerun()

else:

    st.info("No expenses added yet. Add your first expense above! 👆")