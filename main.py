import psycopg2

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
        query = "SELECT grid_code, ST_AsText(geom) FROM landcover_shp"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Print grid codes and WKT geometries on the same line
        for row in rows:
            print(f"{row[0]},{row[1]}")
            
        # Close cursor
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Call the function to fetch and print grid codes
fetch_grid_codes()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
