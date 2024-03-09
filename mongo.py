import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("<your_connection_string>")
db = client["game_database"]
collection = db["player_profiles"]

# Function to create a new player profile
def create_player_profile(player_name, score):
    player_profile = {"name": player_name, "score": score}
    collection.insert_one(player_profile)
    print("Player profile created successfully.")

# Function to retrieve player profile by name
def get_player_profile(player_name):
    player_profile = collection.find_one({"name": player_name})
    if player_profile:
        print("Player Name:", player_profile["name"])
        print("Score:", player_profile["score"])
    else:
        print("Player profile not found.")

# Example usage
create_player_profile("Player1", 100)
get_player_profile("Player1")
