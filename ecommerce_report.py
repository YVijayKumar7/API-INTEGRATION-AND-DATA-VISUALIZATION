import pandas as pd
from fpdf import FPDF

#load data set
df=pd.read_csv('sales_data.csv')
df['Total']=df ['Quantity']*df['Price']
total_revenue = df['Total'].sum()
top_products = df.groupby('Product Name')['Total'].sum().sort_values(ascending=False).head(5)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'E-commerce Sales Report', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page{self.page_no()}', 0, 0, 'C')

pdf=PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 12)

#Summery Information
pdf.cell(0, 10, 'Total Revenue: ${total_revenue,.2f}',ln=True)
pdf.ln(5)

# Step 4: Add Top Products
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Top 5 Products by Revenue:', ln=True)
pdf.set_font('Arial', '', 12)
for name,value in top_products.items():
    pdf.cell(0,10, f'{name}: ${value:.2f}', ln=True)
pdf.ln(10)

# Step 5: Insert Images
pdf.image('sales_by_category.png', x=10, w=190)
pdf.ln(5)
pdf.image('top_products.png', x=10, w=190)

# Step 6: Output the PDF
pdf.output('ecommerce_report.pdf')
print("PDF report generated successfully: ecommerce_report.pdf")