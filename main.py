from flask import Flask, jsonify
import psycopg2 
import json
import os

app = Flask(__name__)

def fetch_geom_as_geojson(table_name, geom_column, db_params):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute(f"SELECT ST_AsGeoJSON({geom_column}) FROM {table_name} LIMIT 1")
        geojson_with_slashes = cur.fetchone()[0]
        conn.close()
        geojson_without_slashes = json.loads(geojson_with_slashes.replace("\\", ""))
        return geojson_without_slashes
    except (psycopg2.Error, json.JSONDecodeError) as e:
        # Handle exceptions gracefully, log or return appropriate error response
        return jsonify({'error': str(e)}), 500

@app.route('/')
def get_geojson():
    try:
        table_name = "kriging_temper_point"
        geom_column = "shape"
        geojson = fetch_geom_as_geojson(table_name, geom_column, db_params)
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
        return jsonify(feature_collection)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)




