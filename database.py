from pymongo import MongoClient

def insert_data(firstname, lastname, birthday, age, sex, address, contact_number, emergency_contact_name, emergency_contact_number, marital_status, video):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['registration']
    collection = db['patients']

    # Create a document with the form data
    data = {
        'firstname': firstname,
        'lastname': lastname,
        'birthday': birthday,
        'age': age,
        'sex': sex,
        'address': address,
        'contact_number': contact_number,
        'emergency_contact_name': emergency_contact_name,
        'emergency_contact_number': emergency_contact_number,
        'marital_status': marital_status,
        'video': video
    }

    # Insert the document into the collection
    collection.insert_one(data)

    # Close the MongoDB connection
    client.close()

def get_latest_record():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['registration']
    collection = db['patients']

    # Fetch the latest record from the database
    document = collection.find_one(sort=[('_id', -1)])

    # Close the MongoDB connection
    client.close()

    return document


def get_document_id():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['registration']
    collection = db['patients']

    # Fetch the latest record from the database
    document = collection.find_one(sort=[('_id', -1)])

    # Extract the document ID
    document_id = str(document['_id'])

    # Close the MongoDB connection
    client.close()

    return document_id


def check_video_presence(document_id):
    client = MongoClient('mongodb://localhost:27017')
    db = client['registration']
    collection = db['patients']

    document = collection.find_one({'_id': document_id})
    if 'video' in document:
        print('Video is present in the document.')
    else:
        print('Video is not present in the document.')


