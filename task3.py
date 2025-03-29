import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Load and process the dataset
file_path = 'traffic.csv'
try:
    # Load dataset
    df = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    print("Dataset loaded successfully!")
except FileNotFoundError:
    raise FileNotFoundError("Error: Dataset file 'traffic.csv' not found! Ensure it is in the same folder.")

# Validate required columns
required_columns = ['event', 'date', 'country', 'city', 'artist', 'album', 'track', 'isrc', 'linkid']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise KeyError(f"Missing columns in the dataset: {missing_columns}")

# Data preprocessing
df.columns = df.columns.str.strip()  # Strip whitespace from column names
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert 'date' to datetime
df.dropna(subset=['date'], inplace=True)  # Remove rows with invalid dates
df['Month'] = df['date'].dt.to_period('M').astype(str)  # Add 'Month' column for grouping
df['city'] = df['city'].fillna('Unknown')  # Fill missing cities with 'Unknown'

# Generate dropdown options for countries
country_options = [{'label': country, 'value': country} for country in df['country'].dropna().unique()]
default_country = country_options[0]['value'] if country_options else None

# Initialize Dash app
app = Dash(__name__)

# Dark theme styling
dark_theme = {
    "paper_bgcolor": "black",
    "plot_bgcolor": "black",
    "font_color": "white"
}

# Define layout
app.layout = html.Div([
    html.H1("Traffic Data Interactive Dashboard", style={'text-align': 'center', 'color': 'white'}),

    html.Label("Select a Country:", style={'color': 'white'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=country_options,
        value=default_country,  # Default value for dropdown
        clearable=False,
        style={'backgroundColor': 'black', 'color': 'white'}
    ),

    dcc.Graph(id='line-chart'),
    dcc.Graph(id='city-bar-chart'),
    dcc.Graph(id='event-pie-chart'),
    dcc.Graph(id='track-scatter-chart'),
])

# Define callback for updating graphs
@app.callback(
    [Output('line-chart', 'figure'),
     Output('city-bar-chart', 'figure'),
     Output('event-pie-chart', 'figure'),
     Output('track-scatter-chart', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_dashboard(selected_country):
    # Filter data for the selected country
    filtered_df = df[df['country'] == selected_country]

    # Handle empty data
    if filtered_df.empty:
        placeholder_chart = px.scatter(title="No Data Available", template='plotly_dark').update_layout(dark_theme)
        return placeholder_chart, placeholder_chart, placeholder_chart, placeholder_chart

    # Line Chart: Monthly Event Trends
    monthly_events = filtered_df.groupby('Month')['event'].count().reset_index()
    line_chart = px.line(
        monthly_events, x='Month', y='event', title='Monthly Event Trends',
        markers=True, template='plotly_dark'
    ).update_layout(dark_theme)

    # Bar Chart: Events by City
    city_events = filtered_df['city'].value_counts().reset_index()
    city_events.columns = ['city', 'count']
    city_bar_chart = px.bar(
        city_events, x='city', y='count', title='Events by City',
        color='city', template='plotly_dark'
    ).update_layout(dark_theme)

    # Pie Chart: Event Distribution
    event_distribution = filtered_df['event'].value_counts().reset_index()
    event_distribution.columns = ['event', 'count']
    event_pie_chart = px.pie(
        event_distribution, names='event', values='count', title='Event Distribution',
        template='plotly_dark'
    ).update_layout(dark_theme)

    # Scatter Plot: Tracks by ISRC
    track_scatter_chart = px.scatter(
        filtered_df, x='track', y='isrc', size=filtered_df['track'].apply(len), color='city',
        title='Tracks and ISRCs', template='plotly_dark'
    ).update_layout(dark_theme)

    # Return all updated charts
    return line_chart, city_bar_chart, event_pie_chart, track_scatter_chart

# Run the app
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("Server stopped.")