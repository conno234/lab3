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

def fetch_grid_codes_with_geom():
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Query to fetch grid codes and geometries
        query = "SELECT station_id, air_temper, ST_AsText(geom) FROM minn_temp"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Close cursor
        cursor.close()
        
        # Return grid codes and geometries
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        # Close the connection
        if conn is not None:
            conn.close()

@app.route('/')
def index():
    # Call the function to fetch grid codes and geometries
    grid_codes_with_geom = fetch_grid_codes_with_geom()
    if isinstance(grid_codes_with_geom, list):
        # Format output as HTML
        output = ''
        for row in grid_codes_with_geom:
            grid_code, geom = row
            output += f"{station_id}, {air_temper}, {geom},<br>"
        return output
    else:
        return grid_codes_with_geom

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
