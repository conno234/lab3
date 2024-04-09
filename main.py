# Importing necessary libraries
from flask import Flask, jsonify
import psycopg2
import json
import os

# Initialize Flask application
app = Flask(__name__)

# Database connection parameters
db_params = {
    'database': os.environ.get("DB_DATABASE"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD"),
    'host': os.environ.get("DB_HOST"),
    'port': os.environ.get("DB_PORT")
}

# Function to fetch geometry as GeoJSON from the database
def fetch_geom_as_geojson(table_name, geom_column, db_params):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    # Execute a query to retrieve the geometry as GeoJSON
    cur.execute(f"SELECT ST_AsGeoJSON({geom_column}) FROM {table_name} LIMIT 1")
    geojson_with_slashes = cur.fetchone()[0]  # Fetch the result
    conn.close()  # Close the database connection
    # Remove the slashes from the GeoJSON string to submit the GeoJSON to ArcOnline
    geojson_without_slashes = json.loads(geojson_with_slashes.replace("\\", ""))
    return geojson_without_slashes  # Return the GeoJSON data

# Route for the root URL
@app.route('/')
def get_geojson():
    table_name = "landcover_shp"  # Define the table name
    geom_column = "geom"  # Define the geometry column name
    
    # Fetch GeoJSON data from the database
    geojson = fetch_geom_as_geojson(table_name, geom_column, db_params)
    
    # Structure the GeoJSON into Feature Collection format, per ArcOnline specifications
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": geojson,
                "properties": {}  # No additional properties for now
            }
        ]
    }
    return jsonify(feature_collection)  # Return the GeoJSON as a JSON response

# Run the Flask app with debugging enabled on host '0.0.0.0' and port 8080
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
