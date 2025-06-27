import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import nltk
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import io
import os

nltk.download('punkt')

# ---------- SIDEBAR ----------
st.sidebar.title("📦 E-Commerce Dashboard")
section = st.sidebar.radio("Choose Task", [
    "📊 Sales Visualization",
    "📄 Generate PDF Report",
    "🤖 Product Chatbot",
    "🧠 Purchase Prediction"
])

# ---------- COMMON SALES DATA ----------
@st.cache_data
def load_sales_data():
    df = pd.read_csv("sales_data.csv")
    df["Total"] = df["Quantity"] * df["Price"]
    return df

sales_df = load_sales_data()

# ---------- TASK 1: SALES VISUALIZATION ----------
if section == "📊 Sales Visualization":
    st.title("📊 Sales Data Visualization")

    st.subheader("Sales by Category")
    cat_data = sales_df.groupby("Category")["Total"].sum()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=cat_data.index, y=cat_data.values, palette="Blues_d", ax=ax1)
    st.pyplot(fig1)

    st.subheader("Top 5 Products by Revenue")
    prod_data = sales_df.groupby("Product Name")["Total"].sum().sort_values(ascending=False).head(5)
    fig2, ax2 = plt.subplots()
    prod_data.plot(kind="pie", autopct='%1.1f%%', startangle=90, ax=ax2)
    ax2.axis("equal")
    st.pyplot(fig2)

# ---------- TASK 2: PDF REPORT ----------
elif section == "📄 Generate PDF Report":
    st.title("📄 Download PDF Sales Report")

    prod_data = sales_df.groupby("Product Name")["Total"].sum().sort_values(ascending=False).head(5)
    total_revenue = sales_df["Total"].sum()

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "E-Commerce Sales Report", ln=True, align="C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 10)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Total Revenue: ₹{total_revenue:,.2f}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Top 5 Products:", ln=True)
    pdf.set_font("Arial", size=12)
    for name, val in prod_data.items():
        pdf.cell(0, 10, f"- {name}: ₹{val:,.2f}", ln=True)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    st.download_button("📥 Download Report", data=pdf_buffer.getvalue(), file_name="sales_report.pdf")

# ---------- TASK 3: CHATBOT ----------
elif section == "🤖 Product Chatbot":
    st.title("🤖 Ask About Sales")

    user_input = st.text_input("Ask your question (e.g., total revenue, top products)")

    def chatbot_reply(msg):
        tokens = nltk.word_tokenize(msg.lower())

        if 'revenue' in tokens:
            return f"💰 Our total revenue is ₹{sales_df['Total'].sum():,.2f}."
        elif 'orders' in tokens:
            return f"📦 We received {sales_df['Order ID'].nunique()} orders."
        elif 'top' in tokens:
            top_items = sales_df.groupby("Product Name")["Total"].sum().sort_values(ascending=False).head(3)
            return "🏆 Top 3 Products:\n" + "\n".join([f"{p}: ₹{v:,.2f}" for p, v in top_items.items()])
        elif 'category' in tokens:
            cat_items = sales_df.groupby("Category")["Total"].sum()
            return "📊 Sales by Category:\n" + "\n".join([f"{c}: ₹{v:,.2f}" for c, v in cat_items.items()])
        else:
            return "🤖 Sorry, I didn't understand. Ask about revenue, orders, or top products."

    if user_input:
        response = chatbot_reply(user_input)
        st.success(response)

# ---------- TASK 4: PURCHASE PREDICTION ----------
elif section == "🧠 Purchase Prediction":
    st.title("🧠 Predict User Purchase")

    uploaded_file = st.file_uploader("Upload user_behavior.csv", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df['Device'] = LabelEncoder().fit_transform(df['Device'])
        X = df[['Time on Site', 'Pages Visited', 'Added to Cart', 'Device']]
        y = df['Purchase']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        st.subheader("Classification Report")
        st.text(classification_report(y_test, y_pred))

        st.subheader("Confusion Matrix")
        fig, ax = plt.subplots()
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Greens", ax=ax)
        st.pyplot(fig)
