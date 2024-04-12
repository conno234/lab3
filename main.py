from flask import Flask, jsonify
import psycopg2 
import json
import os

app = Flask(__name__)

db_params = {
    'database': 'lab3',  
    'user': 'postgres',  
    'password': 'IMissPinole1312!?', 
    'host': '34.16.107.82',  
    'port': '5432' 
}


def fetch_geom_as_geojson_orig(table_name, geom_column, db_params):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute(f"SELECT JSON_BUILD_OBJECT('type','FeatureCollection', 'features', JSON_AGG(ST_AsGeoJSON({table_name}.*)::json)) FROM {table_name}")
    geojson = cur.fetchone()[0]
    conn.close()
    return geojson

def fetch_geom_as_geojson(table_name, geom_column, db_params):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute(f"SELECT JSON_BUILD_OBJECT(JSON_AGG(ST_AsGeoJSON({table_name}.*)::json)) FROM {table_name}")
    geojson = cur.fetchone()[0]
    conn.close()
    return geojson

@app.route('/kriging_point')
def get_kriging_point():
    try:
        table_name = "kriging_temper_point"
        geom_column = "shape"
        geojson = fetch_geom_as_geojson(table_name, geom_column, db_params)
        
        # Wrapping the geojson in a Feature Collection
        feature_collection = {
            "type": "FeatureCollection", # Move "type" to the root level
            "features": geojson  # Assuming geojson is already a list of features
        }
        
        return jsonify(feature_collection)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/kriging_diff')
def get_kriging_diff():
    try:
        table_name = "kriging_difference_elev"
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

@app.route('/idw_point')
def get_idw_point():
    try:
        table_name = "idw_difference_point"
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
