from flask import Blueprint, render_template
from pymongo import MongoClient
import os

quality_control = Blueprint('quality_control', __name__)

# MongoDB Atlas connection string
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://<username>:<password>@cluster0.vrqby.mongodb.net/quality_dashboard?retryWrites=true&w=majority')

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.get_database()
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    db = None

@quality_control.route('/quality_control')
def show_quality_control():
    # Placeholder data - replace with actual data from MongoDB when available
    quality_data = {
        'defect_rate': 2.5,
        'first_pass_yield': 97,
        'scrap_rate': 1.8
    }

    return render_template('quality_control.html', data=quality_data)

