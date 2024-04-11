from flask import Flask, jsonify
import psycopg2 
import json
import os

# First, I initialize my Flask application
app = Flask(__name__)

# Next I need to establish the parameters needed to connect to the database
# The login information has been stored as variables on the Google Cloud Run deployment for this.
db_params = {
    'database': 'lab3',  
    'user': os.environ.get("DB_USER"),  
    'password': os.environ.get("DB_PASSWORD"), 
    'host': os.environ.get("DB_HOST"),  
    'port': os.environ.get("DB_PORT") 
}

# Next, this function fetches the geometry as GeoJSON from the database
def fetch_geom_as_geojson(table_name, geom_column, db_params):
    # I connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    # I execute a query to retrieve the geometry as GeoJSON
    cur.execute(f"SELECT ST_AsGeoJSON({geom_column}) FROM {table_name} LIMIT 1")
    geojson_with_slashes = cur.fetchone()[0]  # I fetch the result
    conn.close()  # Then, I close the database connection
    # I remove the slashes from the GeoJSON string in order to more easily submit the GeoJSON to ArcOnline
    geojson_without_slashes = json.loads(geojson_with_slashes.replace("\\", ""))
    return geojson_without_slashes  # And then I return the GeoJSON data

# This is the route for the root URL
@app.route('/')
def get_geojson():
    table_name = "kriging_temper_point"  # First I define the table name
    geom_column = "shape"  # Then I define the geometry column name from which to grab the WKT
    
    geojson = fetch_geom_as_geojson(table_name, geom_column, db_params) # I fetch GeoJSON data from the database
    # And then I can construct structure the GeoJSON into Feature Collection format, per ArcOnline specifications
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": geojson,
                "properties": grid_code  # No additional properties for now
            }
        ]
    }
    return jsonify(feature_collection)  # Finally, I return the GeoJSON as a JSON response

# Now, I can run this script directly and use the Flask app with debugging enabled on host '0.0.0.0' and port 8080
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)




