from flask import Flask, jsonify
import psycopg2 
import os

app = Flask(__name__)

# Parameters to connect to the database
db_params = {
    'database': os.environ.get("DB_DATABASE"),  
    'user': os.environ.get("DB_USER"),  
    'password': os.environ.get("DB_PASSWORD"), 
    'host': os.environ.get("DB_HOST"),  
    'port': os.environ.get("DB_PORT") 
}

def get_column_headers(table_name, db_params):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
    column_headers = [row[0] for row in cur.fetchall()]
    conn.close()
    return column_headers

@app.route('/')
def show_column_headers():
    table_name = "landcoverpoint_shp"
    column_headers = get_column_headers(table_name, db_params)
    return jsonify(column_headers)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
