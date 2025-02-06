from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash

# Sample Satisfaction Data
satisfaction_data = {
    "Metric": ["Satisfaction Score", "On-Time Delivery", "Return Rate", "Customer Support", "Product Quality"],
    "Value": [4.5, 92, 8, 4.2, 4.7],
}
df = pd.DataFrame(satisfaction_data)

# Multi-Line Graph Data (Expanded for More Regions)
delivery_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"] * 4,
    "Region": ["North"] * 5 + ["South"] * 5 + ["East"] * 5 + ["West"] * 5,
    "On-Time Delivery %": [88, 91, 92, 94, 96, 85, 89, 90, 92, 95, 80, 85, 87, 89, 90, 78, 82, 85, 88, 91]
})

return_data = pd.DataFrame({
    "Reason": ["Defects", "Wrong Specs", "Late Delivery", "Others"],
    "Count": [40, 30, 20, 10]
})

# Create Flask Blueprint
from flask import Blueprint

customer_satisfaction = Blueprint('customer_satisfaction', __name__)

# Define Dash App
def create_dash_app(flask_app):
    app = dash.Dash(__name__, server=flask_app, external_stylesheets=[dbc.themes.DARKLY])

    # Sidebar Navigation
    sidebar = dbc.NavbarSimple(
        children=[dbc.NavItem(dbc.NavLink("Customer Satisfaction Dashboard", href="#"))],
        brand="JSW Quality Dashboard",
        color="dark",
        dark=True,
        className="sidebar"
    )

    # Layout
    app.layout = html.Div([
        sidebar,
        html.Div([
            html.H1("Customer Satisfaction Overview", className="text-white text-center heading"),

            # Graphs Box with Shadow
            html.Div([
                dbc.Row([
                    dbc.Col(dcc.Graph(id="delivery-graph"), width=7),
                    dbc.Col(dcc.Graph(id="return-graph"), width=5)
                ], className="graph-row"),
            ], className="graph-box shadow-lg p-4 mb-4 bg-dark rounded"),  

            # Satisfaction Metrics
            html.Div([
                dcc.Graph(id="satisfaction-metrics-bar"),
            ], className="graph-box shadow-lg p-4 bg-dark rounded"),  

            # Numeric Analytics Box
            html.Div([
                html.H3("Dynamic Numeric Analytics", className="text-white text-center"),
                html.Div(id="numeric-analytics", className="text-center text-light font-weight-bold")
            ], className="metric-box shadow-lg p-3 bg-secondary rounded"),

            # Dropdown for Month Selection
            html.Div([
                html.Label("Select Delivery Month", className="text-white font-weight-bold"),
                dcc.Dropdown(
                    id="month-dropdown",
                    options=[{'label': month, 'value': month} for month in delivery_data["Month"].unique()],
                    value="Jan",
                    clearable=False,
                    className="dropdown-box shadow-lg p-3 bg-dark rounded"
                )
            ], className="dropdown-box shadow-lg p-3 bg-dark rounded")
        ], className="content")
    ])

    # Callback to update graphs dynamically
    @app.callback(
        Output("delivery-graph", "figure"),
        Output("return-graph", "figure"),
        Output("satisfaction-metrics-bar", "figure"),
        Output("numeric-analytics", "children"),
        Input("month-dropdown", "value")
    )
    def update_graphs(selected_month):
        # Filter Data for Selected Month
        filtered_delivery_data = delivery_data[delivery_data["Month"] == selected_month]
        
        # Multi-Line Chart (On-Time Delivery for Different Regions)
        delivery_fig = px.line(
            filtered_delivery_data,
            x="Month",
            y="On-Time Delivery %",
            color="Region",
            markers=True,
            title=f"On-Time Delivery Trend - {selected_month}",
            line_shape="linear"
        )
        delivery_fig.update_layout(
            paper_bgcolor="#2c2c2c", 
            plot_bgcolor="#2c2c2c", 
            font=dict(color="white"), 
            margin=dict(l=40, r=40, t=40, b=40)
        )
        delivery_fig.update_traces(line=dict(width=3))

        # Pie Chart Update (Return Reasons)
        return_fig = px.pie(
            return_data, names="Reason", values="Count", title="Return Reasons",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        return_fig.update_layout(
            paper_bgcolor="#2c2c2c",
            font=dict(color="white")
        )

        # Satisfaction Metrics Bar Chart
        satisfaction_bar = px.bar(
            df, x="Metric", y="Value", text="Value", title="Satisfaction Metrics",
            color="Metric", color_discrete_sequence=px.colors.qualitative.Bold
        )
        satisfaction_bar.update_layout(
            paper_bgcolor="#2c2c2c", 
            plot_bgcolor="#2c2c2c", 
            font=dict(color="white"), 
            margin=dict(l=40, r=40, t=40, b=40)
        )

        # Dynamic Satisfaction Score
        dynamic_value = df[df["Metric"] == "Satisfaction Score"]["Value"].values[0]
        avg_satisfaction = df["Value"].mean()
        numeric_analytics = f"📊 Satisfaction Score: {dynamic_value}/5 | Avg Score: {round(avg_satisfaction, 2)}/5"

        return delivery_fig, return_fig, satisfaction_bar, numeric_analytics

    return app
