from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import psycopg2


app = Flask(__name__)
CORS(app)


try:

    conn = psycopg2.connect(
        host='localhost',
        database='gym-tracker',
        user='samueltamiru',
        password='QX6LUst-yBEe*poL8sW23a4LE4Nj8Hwiwbepj!M'
    )

    cursor = conn.cursor()

except psycopg2.Error as e:
    print(f'Connection faield: {e}')

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    plain_password = data['password']

    hashed_password = bcrypt.hashpw(plain_password.encode('uft-8'),bcrypt.gensalt())

    cursor.execute(
        """
        INSERT INTO users(username, password) VALUES (%s,%s)
        """,
        (username, hashed_password.decode('utf-8'))           
                   )
    
    conn.commit()
    print(f'User {username} registered sucessfully')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    plain_password = data['password']

    try:
        # 1. Fetch the stored hash from the DB
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        stored_hash = cursor.fetchone()

        # 2. Check if the username even exists
        if stored_hash is None:
            print("Username not found!")
            return

        # 3. Compare the entered password against the stored hash
        if bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash[0].encode('utf-8')):
            print("Login successful!")
        else:
            print("Wrong password!")

    except psycopg2.OperationalError:
        print("Could not connect to the database!")
    except psycopg2.ProgrammingError:
        print("Database query failed!")
    except psycopg2.DatabaseError:
        print("Something went wrong with the database!")
    

if __name__ == '__main__':
    app.run(debug=True)