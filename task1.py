import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Load the dataset
file_path = 'ecommerce.csv'
try:
    df = pd.read_csv(file_path, encoding='latin1')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    raise FileNotFoundError("Error: Dataset file 'ecommerce.csv' not found! Ensure it is in the same folder.")

# Column validation
required_columns = [
    'Customer ID', 'Purchase Date', 'Product Category', 'Product Price', 'Quantity',
    'Total Purchase Amount', 'Payment Method', 'Customer Age', 'Returns',
    'Customer Name', 'Age', 'Gender', 'Churn'
]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise KeyError(f"Missing columns in the dataset: {missing_columns}")

# Data preprocessing
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'], errors='coerce')
df.dropna(subset=['Purchase Date'], inplace=True)
df['Month'] = df['Purchase Date'].dt.to_period('M').astype(str)

# Initialize Dash app
app = Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("Ecommerce Sales Interactive Dashboard", style={'text-align': 'center'}),

    # Dropdown for selecting Product Category
    html.Label("Select Product Category:"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': category, 'value': category} for category in df['Product Category'].dropna().unique()],
        value=df['Product Category'].dropna().unique()[0],
        clearable=False
    ),

    # Graphs for the dashboard
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='bubble-chart'),
])

# Define callback to update graphs based on dropdown input
@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('bubble-chart', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_dashboard(selected_category):
    # Filter data by selected category
    filtered_df = df[df['Product Category'] == selected_category]

    # Line chart: Monthly Sales Trends
    monthly_sales = filtered_df.groupby('Month')['Total Purchase Amount'].sum().reset_index()
    line_chart = px.line(
        monthly_sales, x='Month', y='Total Purchase Amount',
        title='Monthly Sales Trends', markers=True
    )

    # Bar chart: Total Sales by Gender
    bar_chart = px.bar(
        filtered_df, x='Gender', y='Total Purchase Amount',
        color='Gender', title='Total Sales by Gender'
    )

    # Pie chart: Payment Method Distribution
    pie_chart = px.pie(
        filtered_df, names='Payment Method', values='Total Purchase Amount',
        title='Payment Method Distribution'
    )

    # Bubble chart: Quantity vs Price
    bubble_chart = px.scatter(
        filtered_df, x='Product Price', y='Total Purchase Amount',
        size='Quantity', color='Gender',
        title='Quantity vs Total Purchase Amount (Bubble Chart)'
    )

    return line_chart, bar_chart, pie_chart, bubble_chart

# Run the app
if __name__ == '__main__':
    app.run(debug=True)