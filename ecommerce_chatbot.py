# e_commerce_chatbot.py

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt', force=True)

# Load dataset with error handling
try:
    df = pd.read_csv('sales_data.csv')
    df['Total'] = df['Quantity'] * df['Price']

    # Precompute metrics
    total_revenue = df['Total'].sum()
    total_orders = df['Order ID'].nunique()
    top_products = df.groupby('Product Name')['Total'].sum().sort_values(ascending=False).head(3)
    category_sales = df.groupby('Category')['Total'].sum()

except FileNotFoundError:
    print("❌ Error: sales_data.csv not found. Please check your file path.")
    exit()

# Chatbot response logic
def chatbot_response(user_input):
    # tokens = word_tokenize(user_input.lower())
    tokens = user_input.lower().split()
    if 'revenue' in tokens or 'income' in tokens:
        return f"Our total revenue is ₹{total_revenue:,.2f}"

    elif 'orders' in tokens or 'sales' in tokens:
        return f"Total orders received: {total_orders} unique orders."

    elif 'top' in tokens or 'best' in tokens:
        response = "🏆 Top 3 products by sales:\n"
        for name, value in top_products.items():
            response += f"- {name}: ₹{value:,.2f}\n"
        return response

    elif 'category' in tokens or 'categories' in tokens:
        response = "📊 Sales by Category:\n"
        for cat, val in category_sales.items():
            response += f"- {cat}: ₹{val:,.2f}\n"
        return response

    elif 'bye' in tokens:
        return "👋 Bye! Have a great day."

    else:
        return "🤖 Sorry, I didn't understand that. Try asking about revenue, orders, categories, or top products."

# Main chat loop
def main():
    print("💬 E-Commerce Chatbot (type 'bye' to exit)")
    print("👋 Hello! Ask me about revenue, total orders, top products, or category sales.")
    while True:
        user_input = input("You: ")
        response = chatbot_response(user_input)
        print("Bot:", response)
        if 'bye' in user_input.lower():
            break

if __name__ == "__main__":
    main()
