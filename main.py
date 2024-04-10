from flask import Flask, jsonify
import psycopg2
import os

# Initialize Flask application
app = Flask(__name__)

# Database parameters
db_params = {
    'database': os.environ.get('DB_DATABASE'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}

def fetch_grid_codes():
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)

        # Create a cursor
        cursor = conn.cursor()

        # Query to fetch all grid codes with geometries converted to WKT
        query = "SELECT grid_code, ST_AsText(geom) FROM landcover_shp"

        # Execute the query
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Close cursor
        cursor.close()

        return [{'grid_code': row[0], 'geometry': row[1]} for row in rows]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# API endpoint to return grid codes and WKT geometries
@app.route('/grid-codes', methods=['GET'])
def get_grid_codes():
    grid_codes = fetch_grid_codes()
    return jsonify(grid_codes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
