import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import base64
import io

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.title = "AI-Powered Data Visualization"

# Create a sample dataset
def create_sample_dataset():
    data = {
        "Category": ["A", "B", "C", "D"],
        "Sales": [100, 200, 150, 300],
        "Profit": [20, 50, 30, 70],
    }
    df = pd.DataFrame(data)
    df.to_csv("sample_dataset.csv", index=False)
    return df

# Generate sample dataset for testing
sample_df = create_sample_dataset()

# Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("AI-Powered Data Visualization and Insights", className="text-center my-4"),
                width=12,
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dbc.Input(
                                id="user-input", 
                                placeholder="Describe your visualization (e.g., 'Bar chart of sales by category')", 
                                type="text"
                            ),
                            dbc.Button("Generate", id="generate-btn", color="primary"),
                        ],
                        className="mb-4",
                    ),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(
                        id="file-upload",
                        children=html.Div(["Drag and drop or ", html.A("select a CSV file")]),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px",
                        },
                        multiple=False,
                    ),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(id="visualization-output"), width=12, className="mt-4"),
                dbc.Col(html.Div(id="insights-output"), width=12, className="mt-4"),
            ],
            style={"maxHeight": "70vh", "overflowY": "scroll"},
        ),
    ],
    fluid=True,
)

# Helper Function to Parse File Upload
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Attempt to read the uploaded file as a CSV
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df
    except Exception as e:
        raise ValueError(f"Error reading the file: {e}")

# Heuristic Function to Interpret User Input and Suggest Visualization
def infer_visualization_type(user_input, df):
    if "bar" in user_input.lower():
        return "bar", df.columns[:2]
    elif "line" in user_input.lower():
        return "line", df.columns[:2]
    elif "scatter" in user_input.lower():
        return "scatter", df.columns[:2]
    else:
        return "bar", df.columns[:2]  # Default to bar chart

# Callback to handle user input and file upload
@app.callback(
    [Output("visualization-output", "children"), Output("insights-output", "children")],
    [Input("generate-btn", "n_clicks")],
    [State("user-input", "value"), State("file-upload", "contents")],
)
def generate_output(n_clicks, user_input, file_contents):
    if not n_clicks:
        return "Waiting for input...", ""

    if not user_input:
        return "Please provide a description of the visualization.", ""

    # Parse the uploaded file or use the sample dataset
    if file_contents:
        try:
            df = parse_contents(file_contents)
        except ValueError as e:
            return str(e), ""
    else:
        df = sample_df

    # Ensure the DataFrame is valid
    if df.empty:
        return "Dataset is empty or invalid.", ""

    # Infer visualization type
    visualization_type, columns = infer_visualization_type(user_input, df)

    # Generate visualization
    try:
        if visualization_type == "bar":
            fig = px.bar(df, x=columns[0], y=columns[1], title="Bar Chart")
        elif visualization_type == "line":
            fig = px.line(df, x=columns[0], y=columns[1], title="Line Graph")
        elif visualization_type == "scatter":
            fig = px.scatter(df, x=columns[0], y=columns[1], title="Scatter Plot")
        else:
            return f"Unsupported visualization type: {visualization_type}", ""

        graph = dcc.Graph(figure=fig)
    except Exception as e:
        return f"Error generating visualization: {e}", ""

    # Mock insights
    insights = f"Based on the {visualization_type}, the data shows trends between {columns[0]} and {columns[1]}."

    return graph, insights


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
