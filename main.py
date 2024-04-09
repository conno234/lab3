from flask import Flask, jsonify
import psycopg2
import os

# Initialize Flask application
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
        
        # Query to fetch all grid codes
        query = "SELECT grid_code FROM landcover_shp"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Close cursor
        cursor.close()
        
        # Close connection
        conn.close()
        
        # Extract grid codes
        grid_codes = [row[0] for row in rows]
        
        return grid_codes
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

# Define endpoint to retrieve grid codes
@app.route('/grid-codes', methods=['GET'])
def get_grid_codes():
    grid_codes = fetch_grid_codes()
    if grid_codes:
        return jsonify({'grid_codes': grid_codes})
    else:
        return jsonify({'error': 'Failed to retrieve grid codes'}), 500

if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=8080)
