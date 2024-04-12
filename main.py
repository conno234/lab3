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


def fetch_geom_as_geojson(table_name, geom_column, db_params):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute(f"SELECT JSON_BUILD_OBJECT('type','FeatureCollection', 'features', JSON_AGG(ST_AsGeoJSON({table_name}.*)::json)) FROM {table_name}")
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


I need to modify these geojsons so they follow this format: { "type": "FeatureCollection",
    "features": [
      { "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [102.0, 0.5]
          },
          "properties": {
            "prop0": "value0"
          }
        },
      { "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
            ]
          },
        "properties": {
          "prop0": "value0",
          "prop1": 0.0
          }
        },
      { "type": "Feature",
         "geometry": {
           "type": "Polygon",
           "coordinates": [
             [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
               [100.0, 1.0], [100.0, 0.0] ]
             ]
         },
         "properties": {
           "prop0": "value0",
           "prop1": {"this": "that"}
           }
         }
       ]
     }

