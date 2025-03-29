import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Load the dataset
file_path = 'traffic.csv'
try:
    df = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: Dataset file 'traffic.csv' not found! Ensure it is in the same folder.")
    raise SystemExit  # Exit gracefully if the file is not found

# Column validation
required_columns = [
    'event', 'date', 'country', 'city', 'artist', 'album', 'track', 'isrc', 'linkid'
]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise KeyError(f"Missing columns in the dataset: {missing_columns}")

# Clean and prepare data
df.columns = df.columns.str.strip()  # Strip whitespace from column names
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert date column to datetime
df.dropna(subset=['date'], inplace=True)  # Remove rows with invalid dates
df['Month'] = df['date'].dt.to_period('M').astype(str)  # Create a month column for grouping
df['city'] = df['city'].fillna('Unknown')  # Replace missing city values with 'Unknown'

# Prepare dropdown options
artist_options = [{'label': artist, 'value': artist} for artist in df['artist'].unique()]
default_artist = artist_options[0]['value'] if artist_options else None  # Handle empty artist list

# Initialize Dash app
app = Dash(__name__)

# Define a dark theme for the dashboard
dark_theme = {
    "paper_bgcolor": "black",
    "plot_bgcolor": "black",
    "font_color": "white"
}

# Define the layout of the app
app.layout = html.Div([
    html.H1("Traffic Data Interactive Dashboard", style={'text-align': 'center', 'color': 'white'}),

    # Dropdown for selecting an artist
    html.Label("Select an Artist:", style={'color': 'white'}),
    dcc.Dropdown(
        id='artist-dropdown',
        options=artist_options,
        value=default_artist,  # Set default value for the dropdown
        clearable=False
    ),

    # Graphs for the dashboard
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='country-bar-chart'),
    dcc.Graph(id='city-pie-chart'),
    dcc.Graph(id='album-bar-chart'),
    dcc.Graph(id='track-scatter-chart'),
])

# Define the callback to update graphs
@app.callback(
    [Output('line-chart', 'figure'),
     Output('country-bar-chart', 'figure'),
     Output('city-pie-chart', 'figure'),
     Output('album-bar-chart', 'figure'),
     Output('track-scatter-chart', 'figure')],
    [Input('artist-dropdown', 'value')]
)
def update_dashboard(selected_artist):
    # Filter data for the selected artist
    filtered_df = df[df['artist'] == selected_artist]

    # Handle empty filtered data
    if filtered_df.empty:
        # Return placeholder charts if no data is available
        placeholder_chart = px.scatter(title="No Data Available", template='plotly_dark').update_layout(dark_theme)
        return placeholder_chart, placeholder_chart, placeholder_chart, placeholder_chart, placeholder_chart

    # 1. Line Chart for Monthly Event Trends
    monthly_events = filtered_df.groupby('Month')['event'].count().reset_index()
    line_chart = px.line(
        monthly_events, x='Month', y='event', title='Monthly Event Trends',
        markers=True, template='plotly_dark'
    ).update_layout(dark_theme)

    # 2. Bar Chart for Events by Country
    country_events = filtered_df.groupby('country')['event'].count().reset_index()
    country_bar_chart = px.bar(
        country_events, x='country', y='event', title='Events by Country',
        color='country', template='plotly_dark'
    ).update_layout(dark_theme)

    # 3. Pie Chart for City-wise Event Distribution
    city_events = filtered_df['city'].value_counts().reset_index()
    city_events.columns = ['city', 'count']
    city_pie_chart = px.pie(
        city_events, names='city', values='count', title='City-wise Event Distribution',
        template='plotly_dark'
    ).update_layout(dark_theme)

    # 4. Bar Chart for Top Albums
    album_counts = filtered_df['album'].value_counts().reset_index()
    album_counts.columns = ['album', 'count']
    album_bar_chart = px.bar(
        album_counts, x='album', y='count', title='Top Albums',
        color='album', template='plotly_dark'
    ).update_layout(dark_theme)

    # 5. Scatter Plot for Tracks and ISRCs
    track_scatter_chart = px.scatter(
        filtered_df, x='track', y='isrc', size=filtered_df['track'].apply(len), color='city',
        title='Tracks and ISRCs', template='plotly_dark'
    ).update_layout(dark_theme)

    # Return all updated charts
    return line_chart, country_bar_chart, city_pie_chart, album_bar_chart, track_scatter_chart

# Run the app
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("Server stopped.")