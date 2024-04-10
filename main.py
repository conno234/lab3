from flask import Flask
import psycopg2
import csv

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
        query = "SELECT column_name, ST_AsText(geom) FROM landcover_shp"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Get column names
        col_names = [desc[0] for desc in cursor.description]
        
        # Close cursor
        cursor.close()
        
        # Prepare CSV data
        csv_data = ','.join(col_names) + '\n'
        for row in rows:
            csv_data += ','.join(str(cell) for cell in row) + '\n'
        
        # Return CSV data
        return csv_data
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        # Close the connection
        if conn is not None:
            conn.close()

@app.route('/')
def index():
    # Call the function to fetch grid codes
    grid_codes_csv = fetch_grid_codes()
    if isinstance(grid_codes_csv, str):
        return grid_codes_csv
    else:
        return "An error occurred while fetching grid codes."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
