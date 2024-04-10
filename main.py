from flask import Flask
import psycopg2

app = Flask(__name__)

# Database parameters
db_params = {
    'database': 'lab1.2',  
    'user': 'postgres',  
    'password': 'IMissPinole1312!?', 
    'host': '34.16.107.82',  
    'port': '5432' 
}

def fetch_grid_codes():
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Query to fetch all grid codes with geometries converted to WKT
        query = "SELECT ST_AsText(geom) FROM landcover_shp"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Close cursor
        cursor.close()
        
        # Return grid codes
        return [row[0] for row in rows]
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        # Close the connection
        if conn is not None:
            conn.close()

@app.route('/')
def index():
    # Call the function to fetch grid codes
    grid_codes = fetch_grid_codes()
    if isinstance(grid_codes, list):
        return '<br>'.join(grid_codes)
    else:
        return grid_codes

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
