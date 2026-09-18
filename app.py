import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Smart Expense Tracker")
st.write("Track, analyze and predict your spending.")



if "expenses" not in st.session_state:
    st.session_state.expenses = []


st.sidebar.header("💰 Monthly Budget")

budget = st.sidebar.number_input(
    "Set your monthly budget (₹)",
    min_value=0.0,
    value=10000.0,
    step=500.0
)



st.subheader("➕ Add Expense")

col1, col2 = st.columns(2)

with col1:

    date = st.date_input("Date")

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Entertainment",
            "Bills",
            "Other"
        ]
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



df = pd.DataFrame(st.session_state.expenses)


if len(df) > 0:

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])


    # =================================================
    # BASIC CALCULATIONS
    # =================================================

    total_expense = np.sum(df["Amount"])

    average_expense = np.mean(df["Amount"])

    highest_expense = np.max(df["Amount"])

    remaining_budget = budget - total_expense


    # =================================================
    # EXPENSE SUMMARY
    # =================================================

    st.divider()

    st.subheader("📊 Expense Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Expense",
        f"₹{total_expense:.2f}"
    )

    col2.metric(
        "Average Expense",
        f"₹{average_expense:.2f}"
    )

    col3.metric(
        "Highest Expense",
        f"₹{highest_expense:.2f}"
    )

    col4.metric(
        "Remaining Budget",
        f"₹{remaining_budget:.2f}"
    )


    if total_expense > budget:

        st.error(
            f"🚨 You are over budget by ₹{total_expense - budget:.2f}"
        )

    elif total_expense >= budget * 0.8:

        st.warning(
            f"⚠️ You have used {total_expense / budget * 100:.1f}% "
            "of your budget."
        )

    else:

        st.success(
            f"✅ You have used {total_expense / budget * 100:.1f}% "
            "of your budget."
        )


    # =================================================
    # ALL EXPENSES
    # =================================================

    st.subheader("📋 All Expenses")

    st.dataframe(
        df,
        use_container_width=True
    )


    # =================================================
    # CATEGORY-WISE ANALYSIS
    # =================================================

    st.subheader("📈 Category-wise Expenses")

    category_expense = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )


    # =================================================
    # BAR CHART
    # =================================================

    fig, ax = plt.subplots()

    category_expense.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Category")

    ax.set_ylabel("Amount (₹)")

    ax.set_title("Category-wise Expenses")

    st.pyplot(fig)


    # =================================================
    # PIE CHART
    # =================================================

    st.subheader("🥧 Expense Distribution")

    fig2, ax2 = plt.subplots()

    ax2.pie(
        category_expense,
        labels=category_expense.index,
        autopct="%.1f%%"
    )

    ax2.set_title("Expense Distribution")

    st.pyplot(fig2)


    # =================================================
    # SPENDING INSIGHTS
    # =================================================

    st.subheader("💡 Spending Insights")

    highest_category = category_expense.idxmax()

    highest_category_amount = category_expense.max()

    highest_category_percentage = (
        highest_category_amount / total_expense
    ) * 100


    st.write(
        f"🍔 **Highest spending category:** "
        f"{highest_category} (₹{highest_category_amount:.2f})"
    )

    st.write(
        f"📊 **{highest_category} represents "
        f"{highest_category_percentage:.1f}% of your total spending.**"
    )

    st.write(
        f"💳 **Average expense per transaction:** "
        f"₹{average_expense:.2f}"
    )


    # =================================================
    # DAILY SPENDING
    # =================================================

    daily_expense = (
        df.groupby("Date")["Amount"]
        .sum()
    )


    st.subheader("📅 Daily Spending")

    fig3, ax3 = plt.subplots()

    daily_expense.plot(
        kind="line",
        marker="o",
        ax=ax3
    )

    ax3.set_xlabel("Date")

    ax3.set_ylabel("Amount (₹)")

    ax3.set_title("Daily Spending Trend")

    st.pyplot(fig3)


    # =================================================
    # ML EXPENSE PREDICTION
    # =================================================

    st.divider()

    st.subheader("🤖 Next Month Expense Prediction")

    # Create monthly data

    monthly_expense = (
        df.groupby(
            df["Date"].dt.to_period("M")
        )["Amount"]
        .sum()
    )


    # Need at least 2 months for prediction

    if len(monthly_expense) >= 2:

        # Convert months into numbers

        X = np.arange(len(monthly_expense)).reshape(-1, 1)

        y = monthly_expense.values


        # Create ML model

        model = LinearRegression()

        model.fit(X, y)


        # Predict next month

        next_month_number = np.array(
            [[len(monthly_expense)]]
        )

        prediction = model.predict(
            next_month_number
        )[0]


        # Prevent negative prediction

        prediction = max(0, prediction)


        st.metric(
            "Predicted Next Month Expense",
            f"₹{prediction:.2f}"
        )


        # Show historical + prediction

        prediction_data = list(y) + [prediction]

        labels = [
            str(month)
            for month in monthly_expense.index
        ]

        labels.append("Next Month")


        fig4, ax4 = plt.subplots()

        ax4.plot(
            labels,
            prediction_data,
            marker="o"
        )

        ax4.set_xlabel("Month")

        ax4.set_ylabel("Expense (₹)")

        ax4.set_title(
            "Historical Spending & Prediction"
        )

        plt.xticks(rotation=45)

        st.pyplot(fig4)


    else:

        st.info(
            "Add expenses from at least 2 different months "
            "to enable ML prediction."
        )


    # =================================================
    # CAN I AFFORD THIS?
    # =================================================

    st.divider()

    st.subheader("🛒 Can I Afford This?")

    purchase_amount = st.number_input(
        "Enter purchase amount (₹)",
        min_value=0.0,
        step=100.0
    )


    if purchase_amount > 0:

        after_purchase = remaining_budget - purchase_amount


        if after_purchase >= 0:

            st.success(
                f"✅ You can afford this purchase. "
                f"Remaining budget: ₹{after_purchase:.2f}"
            )

        else:

            st.error(
                f"❌ This purchase would exceed your budget "
                f"by ₹{abs(after_purchase):.2f}"
            )


    # =================================================
    # DELETE ALL EXPENSES
    # =================================================

    st.divider()

    if st.button("🗑️ Delete All Expenses"):

        st.session_state.expenses = []

        st.rerun()


else:

    st.info(
        "No expenses added yet. "
        "Add your first expense above! 👆"
    )
