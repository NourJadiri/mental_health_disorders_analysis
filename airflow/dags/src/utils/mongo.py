from pymongo import MongoClient
from pymongo.errors import BulkWriteError


def connect_to_mongo():
    # MongoDB connection details
    mongo_host = 'mongo'  # Docker service name for MongoDB
    mongo_port = 27017

    try:
        # Establish connection to MongoDB
        client = MongoClient(host=mongo_host, port=mongo_port)
        client.list_database_names()
        return True

    except Exception as e:
        print("An error occurred while connecting to MongoDB:", e)
        return False

def clean_ingestion_db():
    client = MongoClient('mongo', 27017)
    db = client['chadd_ingestion_db']
    db.drop_collection('posts')
    db.drop_collection('members')
    print("Collections dropped successfully!")

def clean_staging_db():
    client = MongoClient('mongo', 27017)
    db = client['chadd_staging_db']
    db.drop_collection('posts')
    db.drop_collection('members')
    print("Collections dropped successfully!")

def prepare_ingestion_db():
    client = MongoClient('mongo', 27017)
    db = client['chadd_ingestion_db']
    post_collection = db['posts']
    member_collection = db['members']

    # Create a unique index on the post_id field
    post_collection.create_index('post_id', unique=True)

    return post_collection

def insert_post_ids(post_ids):
    client = MongoClient('mongo', 27017)
    db = client['chadd_ingestion_db']
    post_collection = db['posts']

    # Prepare the documents for bulk insertion
    post_docs = [{'post_id': post_id} for post_id in post_ids]

    try:
    # Use insert_many for bulk insertion
        post_collection.insert_many(post_docs, ordered=False)  # Skip duplicates
        print("Post IDs inserted successfully!")
    except BulkWriteError as e:
        print(f"Duplicate entries found. Continuing with remaining insertions.")

def insert_members(members):
    client = MongoClient('mongo', 27017)
    db = client['chadd_ingestion_db']
    member_collection = db['members']
    member_collection.create_index('username', unique=True)

    # Prepare the documents for bulk insertion
    member_docs = [{'username': member} for member in members]

    # Use insert_many for bulk insertion, allowing duplicates to be ignored
    try:
        member_collection.insert_many(member_docs, ordered=False)  # Skip duplicates
        print(f'{len(members)} members inserted successfully!')
    except BulkWriteError as e:
        print(f"Duplicate entries found. Continuing with remaining insertions.")

def get_post_ids():
    client = MongoClient('mongo', 27017)
    db = client['chadd_ingestion_db']
    post_collection = db['posts']

    # Get the post_ids in batches
    post_ids = []
    for post in post_collection.find():
        post_ids.append(post['post_id'])

    return post_ids

def get_members_usernames():
    client = MongoClient('mongo', 27017)
    db = client['chadd_ingestion_db']
    member_collection = db['members']

    # Get the usernames in batches
    usernames = []
    for member in member_collection.find():
        usernames.append(member['username'])

    return usernames

def insert_post_details(posts):
    client = MongoClient('mongo', 27017)
    db = client['chadd_staging_db']
    post_collection = db['posts']

    # Prepare the documents for bulk insertion
    post_docs = [post.to_dict() for post in posts]

    # Use insert_many for bulk insertion
    post_collection.insert_many(post_docs)
    print("Post details inserted successfully!")

def insert_members_details(members):
    client = MongoClient('mongo', 27017)
    db = client['chadd_staging_db']
    member_collection = db['members']

    # Prepare the documents for bulk insertion
    member_docs = [member.to_dict() for member in members]

    # Use insert_many for bulk insertion
    member_collection.insert_many(member_docs, ordered=False)
    print("Member details inserted successfully!")

def create_production_db():
    client = MongoClient('mongo', 27017)
    db = client['Production_db']
    post_collection = db['posts']
    post_collection.create_index(['id', 'Source'], unique=True)
    member_collection = db['members']

    print("Production database created successfully!")