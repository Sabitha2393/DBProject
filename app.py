from flask import Flask, render_template
from utils.dbconnection import MongoDBConnection
import os
app = Flask(__name__)

# MongoDB URI and Database Name
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')


# Initialize and Connect to MongoDB
mongo_util = MongoDBConnection()
db = mongo_util.connect()



@app.route('/')
def index():
    return render_template('login.html')



# Example Usage
@app.route('/test_connection', methods=['GET'])
def test_connection():
    # Test the connection by listing collections
    collections = db.list_collection_names()
    return {"collections": collections}, 200


if __name__ == '__main__':
    app.run(debug=True)
