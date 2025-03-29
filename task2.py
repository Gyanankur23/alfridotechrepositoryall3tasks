import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset (ensure the file is in the same directory as this script)
file_path = 'superstore.csv'  # Make sure the file name is correct
df = pd.read_csv(file_path, encoding='latin1')  # Adjust encoding if needed

# Fill missing values using forward fill
df.fillna(method='ffill', inplace=True)

# Convert date columns to datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')

# 1. Sales by Category
plt.figure(figsize=(10, 6))
category_sales = df.groupby('Category')['Sales'].sum().reset_index()
sns.barplot(x='Category', y='Sales', data=category_sales)
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Sales')
plt.show()

# 2. Sales by Region
plt.figure(figsize=(10, 6))
region_sales = df.groupby('Region')['Sales'].sum().reset_index()
sns.barplot(x='Region', y='Sales', data=region_sales)
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.show()

# 3. Monthly Sales Trend
df.set_index('Order_Date', inplace=True)
monthly_sales = df['Sales'].resample('M').sum()
plt.figure(figsize=(12, 6))
monthly_sales.plot()
plt.title('Monthly Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.show()

# 4. Ship Mode Distribution
plt.figure(figsize=(10, 6))
ship_mode_counts = df['Ship_Mode'].value_counts()
sns.barplot(x=ship_mode_counts.index, y=ship_mode_counts.values)
plt.title('Distribution of Ship Modes')
plt.xlabel('Ship Mode')
plt.ylabel('Count')
plt.show()

# 5. Segment-wise Sales
plt.figure(figsize=(10, 6))
segment_sales = df.groupby('Segment')['Sales'].sum().reset_index()
sns.barplot(x='Segment', y='Sales', data=segment_sales)
plt.title('Total Sales by Segment')
plt.xlabel('Segment')
plt.ylabel('Sales')
plt.show()

# Save the cleaned dataset
df.to_csv('superstore_cleaned.csv', index=False)
print("Cleaned dataset saved as 'superstore_cleaned.csv'.")