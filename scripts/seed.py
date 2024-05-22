import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection details from environment variables
MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

# Connect to the MongoDB server
client = MongoClient(
    host=MONGO_HOST,
    port=27017,
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD
)

# Get the database instance
db = client[MONGO_INITDB_DATABASE]

# Create three collections if they don't exist
users_affiliate3 = db['users_affiliate3']
users_wallet = db['users_wallet']
payout_affiliate = db['payout_affiliate']

# Insert a user document into the users_affiliate3 collection
user_document = {
    'email': 'erfan@gmail.com',
    'user_type': 'admin'
}
inserted_user = users_affiliate3.insert_one(user_document)

# Check if the insertion was successful
if inserted_user.inserted_id:
    print("User document inserted successfully.")
else:
    print("Failed to insert user document.")