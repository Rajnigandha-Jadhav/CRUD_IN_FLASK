from flask import Flask, request, jsonify
from dataclasses import dataclass, asdict
from pymongo import MongoClient
from flask.json import JSONEncoder
from bson import ObjectId
import instaloader



app = Flask(__name__)

  # create a client object and connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# select the database
db = client["instagram"]

# select the collection
collection = db["profiles"]



class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)

app.json_encoder = CustomJSONEncoder


from dataclasses import dataclass

@dataclass
class InstagramAccount:
    name: str
    email: str
    password: str
    followers: int = 0

@app.route('/api/v1/instagram', methods=['POST'])
def create_instagram_account():
    data = request.get_json()
    account = InstagramAccount(**data)

    # Insert account details into the MongoDB collection
    inserted_id = collection.insert_one(asdict(account)).inserted_id
    inserted_account = collection.find_one({"_id": inserted_id})

    # Serialize the account object into JSON response
    response_data = {
        "status": True,
        "message": "Instagram account created",
        "data": inserted_account
    }

    return jsonify(response_data)


@app.route('/api/v1/instagram/<id>', methods=['GET'])
def get_instagram_account(id):
    # Fetch the account details from the MongoDB collection
    account = collection.find_one({"_id": ObjectId(id)})

    if account is None:
        # Return error message if the account is not found
        response_data = {
            "status": False,
            "message": "Instagram account not found"
        }
    else:
        # Serialize the account object into JSON response
        response_data = {
            "status": True,
            "message": "Instagram account retrieved",
            "data": account
        }

    return jsonify(response_data)






@app.route('/api/v1/instagrams', methods=['GET'])
def get_all_instagram_accounts():
    # Fetch all the accounts from the MongoDB collection
    accounts = list(collection.find())

    if not accounts:
        # Return error message if no accounts are found
        response_data = {
            "status": False,
            "message": "No Instagram accounts found"
        }
    else:
        # Serialize the accounts object into JSON response
        response_data = {
            "status": True,
            "message": "Instagram accounts retrieved",
            "data": accounts
        }

    return jsonify(response_data)





@app.route('/api/v1/instagram/<id>', methods=['PUT'])
def update_instagram_account(id):
# Fetch the account details from the MongoDB collection
  account = collection.find_one({"_id": ObjectId(id)})
  if account is None:
    # Return error message if the account is not found
    response_data = {
        "status": False,
        "message": "Instagram account not found"
    }
  else:
    # Update the account details with request data
    account.update(request.json)
    collection.update_one({"_id": ObjectId(id)}, {"$set": account})

    # Serialize the updated account object into JSON response
  response_data = {
        "status": True,
        "message": "Instagram account updated",
        "data": account
    }

  return jsonify(response_data)





@app.route('/api/v1/instagramdelete/<id>', methods=['DELETE'])
def delete_instagram_account(id):
    # Fetch the account details from the MongoDB collection
    account = collection.find_one({"_id": ObjectId(id)})
    if account is None:
        # Return error message if the account is not found
        response_data = {
            "status": False,
            "message": "Instagram account not found"
        }
    else:
        # Delete the account from the collection
        collection.delete_one({"_id": ObjectId(id)})
        response_data = {
            "status": True,
            "message": "Instagram account deleted"
        }

    return jsonify(response_data)





@app.route('/api/v1/instagram/<account_name>/followers', methods=['PUT'])
def increase_followers(account_name):
    data = request.get_json()
    followers = data.get('followers')

    # Update the followers count in the MongoDB collection
    result = collection.update_one({'name': account_name}, {'$inc': {'followers': followers}})

    if result.modified_count == 0:
        return jsonify({'status': False, 'message': 'Account not found.'}), 404

    return jsonify({'status': True, 'message': 'Followers count updated.'})








# @app.route('/totalfollowers', methods=['GET'])
# def get_instagram_followers(username):
#     print(2+2)
    # Initialize an instance of Instaloader class
    # loader = instaloader.Instaloader()

    # Get the Instagram profile by username
    # profile = instaloader.Profile.from_username(loader.context, username)

    # # Get the total number of followers of the Instagram profile
    # total_followers = profile.followers

    # if not total_followers:
    #     # Return error message if no followers are found
    #     response_data = {
    #         "status": False,
    #         "message": "No followers found for account {}".format(username)
    #     }
    # else:
    #     # Serialize the total followers count into JSON response
    #     response_data = {
    #         "status": True,
    #         "message": "Total followers count retrieved for account {}".format(username),
    #         "data": total_followers
    #     }

    # return jsonify(response_data)





if __name__ == '__main__':
    app.run(debug=True)
