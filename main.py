from flask import Flask, jsonify
import psycopg2 
import json
import os

# First, I initialize my Flask application
app = Flask(__name__)

# Next I need to establish the parameters needed to connect to the database
# The login information has been stored as variables on the Google Cloud Run deployment for this.
db_params = {
    'database': os.environ.get("DB_DATABASE"),  
    'user': os.environ.get("DB_USER"),  
    'password': os.environ.get("DB_PASSWORD"), 
    'host': os.environ.get("DB_HOST"),  
    'port': os.environ.get("DB_PORT") 
}

from flask import Flask, jsonify
import psycopg2 
import os
from geojson import Feature, FeatureCollection, dumps

# Initialize Flask application
app = Flask(__name__)

# Function to establish connection to PostGIS database
def connect_to_db():
    return psycopg2.connect(
        database=os.environ.get("DB_DATABASE"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )

# Function to fetch data from PostGIS and convert to GeoJSON
def get_geojson_from_postgis():
    connection = connect_to_db()
    cursor = connection.cursor()

    # Fetch data from the table
    cursor.execute("SELECT grid_code, ST_AsText(geom) FROM landcover_shp")

    features = []
    for row in cursor.fetchall():
        grid_code, geom_wkt = row
        # Convert WKT to GeoJSON
        feature = Feature(geometry=geom_wkt, properties={"grid_code": grid_code})
        features.append(feature)

    cursor.close()
    connection.close()

    feature_collection = FeatureCollection(features)
    return feature_collection

# API endpoint to return GeoJSON
@app.route('/geojson', methods=['GET'])
def geojson():
    geojson_data = get_geojson_from_postgis()
    return jsonify(geojson_data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
