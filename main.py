from flask import Flask, jsonify
import psycopg2 
import json
import os

# Initialize Flask application
app = Flask(__name__)

# Establish parameters to connect to the database
db_params = {
    'database': os.environ.get("DB_DATABASE"),  
    'user': os.environ.get("DB_USER"),  
    'password': os.environ.get("DB_PASSWORD"), 
    'host': os.environ.get("DB_HOST"),  
    'port': os.environ.get("DB_PORT") 
}

# Function to fetch data from the database and convert it to GeoJSON
def get_geojson():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Execute the query to fetch all rows from the table
        cursor.execute("SELECT grid_code, ST_AsText(geom) FROM landcover_shp")

        # Fetch all rows
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Convert fetched data to GeoJSON
        features = []
        for row in rows:
            feature = {
                "type": "Feature",
                "properties": {"grid_code": row[0]},
                "geometry": json.loads(row[1])
            }
            features.append(feature)

        # Construct GeoJSON FeatureCollection
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }

        return geojson_data

    except psycopg2.Error as e:
        print("Error fetching data from PostgreSQL:", e)
        return None

# Route to handle requests for GeoJSON data
@app.route('/geojson', methods=['GET'])
def serve_geojson():
    geojson_data = get_geojson()
    if geojson_data:
        return jsonify(geojson_data)
    else:
        return jsonify({"error": "Failed to fetch GeoJSON data"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
