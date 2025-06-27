import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load data set 
df =pd.read_csv("sales_data.csv")
df['Total']=df ['Quantity']*df['Price']
#total Revenue
total_revenue = df['Total'].sum()
print(f"total revenue: ${total_revenue}")
#sales by category
category_sales=df.groupby('Category')['Total'].sum()
# Top Products
top_products =df.groupby ('Product Name')['Total'].sum().sort_values(ascending=False).head(5)

# Plot: Sales by Category
plt.figure(figsize=(10, 6))
sns.barplot(x=category_sales.index, y=category_sales.values, palette='viridis')
plt.title('Sales by category')
plt.xlabel('Category')
plt.ylabel('Revenue ($)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('sales_by_category.png')
plt.show()

 #Plot: Top 5 Products
plt.figure(figsize=(8,6))
top_products.plot(kind='pie', autopct='%1.1f%%', startangle=90, shadow=True)
plt.title('Top 5 Products by Revenue')
plt.ylabel('')
plt.tight_layout()
plt.savefig('top_products.png')
plt.show()