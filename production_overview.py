from flask import Blueprint, render_template, jsonify
from pymongo import MongoClient
import os
from datetime import datetime
from io import BytesIO
import base64
import plotly.express as px
import pandas as pd


production_overview = Blueprint('production_overview', __name__)

# MongoDB Atlas connection string
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://nikhilvjagtap2003:ra9be97kyhd8wsR9@cluster0.vrqby.mongodb.net/quality_dashboard?retryWrites=true&w=majority')

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.get_database("quality_dashboard")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    db = None

@production_overview.route('/production_overview')
def show_production_overview():
    if db is None:
        return jsonify({'error': 'Database connection error'}), 500
        
    try:
        # Fetch production schedule data
        production_data = list(db.production_schedule.find({}, {'_id': 0}).sort('product', 1))
        
        # Fetch maintenance log data
        maintenance_data = list(db.maintenance_log.find({}, {'_id': 0}))
        
        # Generate production output chart
        chart = generate_production_chart()
        
        if not production_data:
            production_data = {'error': 'No production data available'}
        
        if not maintenance_data:
            maintenance_data = {'error': 'No maintenance data available'}
            
        return render_template(
            'production_overview.html', 
            production_data=production_data,
            maintenance_data=maintenance_data,
            chart=chart
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_production_chart():
    # Fetch production output data from MongoDB
    output_data = list(db.production_output.find({}, {'_id': 0, 'date': 1, 'output': 1}).sort('date', 1))
    
    if not output_data:
        return None

    # Convert data to DataFrame
    df = pd.DataFrame(output_data)

    # Convert 'date' to datetime format for sorting
    df['date'] = pd.to_datetime(df['date'])

    # Generate Plotly chart
    fig = px.line(
        df, 
        x='date', 
        y='output', 
        title='Production Output Over Time',
        labels={'date': 'Date', 'output': 'Output'},
    )
    fig.update_traces(mode='lines+markers')
    fig.update_layout(xaxis_title="Date", yaxis_title="Output", xaxis=dict(tickformat='%Y-%m-%d'))
    
    # Convert Plotly chart to HTML for embedding
    chart_html = fig.to_html(full_html=False)
    
    return chart_html


