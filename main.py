from flask import Flask, jsonify
import certifi
import pymongo
from pymongo import MongoClient
from bson import json_util
import json

# PyMongo
cluster = MongoClient("mongodb+srv://Esmeralda:VWs6NR4CHtbFf2cW@gettingstarted.hnuzv.mongodb.net/Pune?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["pune"]
collection_restaurants = db["pune_restaurants"]
collection_restaurants2 = db["pune_restaurants2"]
collection_wards = db["wards"]

# PyMongo Examples (use db: "test" and collection: "test")
# --------------------

# Insert one document
# post = {"_id": 0, "name": "Joe", "score": 5}
# collection.insert_one(post)

# Insert many documents
# post1 = {"_id": 5, "name": "Joe"}
# post2 = {"_id": 6, "name": "Bill"}
# collection.insert_many([post1, post2])

# Find in Collection
    # Find all by Name
# results = collection.find({"name": "Bill"})
# for result in results:
#     print(result)
#     print(result["_id"])

    # Find all by ID
# results = collection.find({"_id": 5})
# for result in results:
#     print(result["_id"])

    # Find just one document
# results = collection.find_one({"_id": 0})
# print(results)

    # Find everything in collection
# results = collection.find({})
# print(results)

# Delete in Collection
# results = collection.delete_one({"_id": 0})
# results = collection.delete_many({"_id": 0})

# Update
# results = collection.update_one({"_id": 5}, {"$set": {"name": "Tim"}})
# Create new field
# results = collection.update_one({"_id": 5}, {"$set": {"hello": 5}})
# Increment
# results = collection.update_many({"_id": 5}, {"$inc": {"hello": 5}})

# Count Documents
# post_count = collection.count_documents({})
# print(post_count)

# --------------------
# End of PyMongo Examples


# API
app = Flask(__name__)
app.config["DEBUG"] = True

# API Examples
# --------------------

# Basic Version
# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"about": "Hello World!"})

# More Advanced Version
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if (request.method == 'POST'):
#         some_json = request.get_json()
#         return jsonify({'you sent': some_json}), 201
#     else:
#         return jsonify({"about": "Hello World!"})

# @app.route('/multi/<int:num>', methods=['GET'])
# def get_multiply10(num):
#     return jsonify({'result': num*10})

# def home():
#     return ("<h1>Sample Python Page</h1>"
#             "<p>Hello World!</p>")

# --------------------
# End of API Examples



# Python API Project
# --------------------

# Resources and References
    # MongoDB Query Docs: https://docs.mongodb.com/manual/reference/operator/query/
    # Ideas for PyMongo Queries: https://stackoverflow.com/questions/12064764/pymongo-query-on-list-field-and-or
    # Querying Mongo using PyMongo: https://www.analyticsvidhya.com/blog/2020/08/query-a-mongodb-database-using-pymongo/#h2_7
    # Serializing/Sanitizing JSON data (Fixed -> TypeError: ObjectId is not JSON serializable): https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
# Notes
    # response = jsonify({'results':results_sanitized}) -> just adds 'results:' to beginning of output

# Get Restaurants by Category
@app.route('/category/<string:category>', methods=['GET'])
def get_restaurants_by_category(category):
    # test with category: Steak
    results = collection_restaurants.find({"Category": category})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Names by Category
@app.route('/categoryrestnames/<string:category>', methods=['GET'])
def get_restaurant_names_by_category(category):
    # test with category: Steak
    results = collection_restaurants.distinct("Restaurant_Name", {"Category": category})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurants near Latitude and Longitude
@app.route('/restaurants/<float:latitude>/<float:longitude>', methods=['GET'])
def get_restaurants_near_location(latitude, longitude):
    # test with latitude: 18.56184774, longitude: 73.917229135
    results = collection_restaurants.find({"Location": {"$near": {"$geometry": {"type": "Point", "coordinates": [latitude, longitude]}, "$minDistance": 50, "$maxDistance": 1000}}})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Names near Latitude and Longitude
@app.route('/restaurantnames/<float:latitude>/<float:longitude>', methods=['GET'])
def get_restaurant_names_near_location(latitude, longitude):
    # test with latitude: 18.56184774, longitude: 73.917229135
    results = collection_restaurants.distinct("Restaurant_Name", {"Location": {"$near": {"$geometry": {"type": "Point", "coordinates": [latitude, longitude]}, "$minDistance": 50, "$maxDistance": 1000}}})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Name at Latitude and Longitude
@app.route('/restaurantname/<float:latitude>/<float:longitude>', methods=['GET'])
def get_restaurant_name_at_location(latitude, longitude):
    # test with latitude: 18.53257323, longitude: 73.87665387
    results = collection_restaurants.distinct("Restaurant_Name", {"Latitude": latitude, "Longitude": longitude})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Names with Minimum Delivery Rating
@app.route('/restaurantdelivery/<float:rating>', methods=['GET'])
def get_restaurant_names_with_delivery_rating(rating):
    # test with rating: 4.5
    results = collection_restaurants.distinct("Restaurant_Name", {"Delivery_Rating": {"$gte": rating}})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Names with Minimum Dining Rating
@app.route('/restaurantdining/<float:rating>', methods=['GET'])
def get_restaurant_names_with_dining_rating(rating):
    # test with rating: 4.5
    results = collection_restaurants.distinct("Restaurant_Name", {"Dining_Rating": {"$gte": rating}})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Names with Minimum Dining Rating and Maximum Price
@app.route('/restaurantdiningandprice/<float:rating>/<int:price>', methods=['GET'])
def get_restaurant_names_with_dining_rating_and_price(rating, price):
    # test with rating: 4.5, price: 3700
    results = collection_restaurants.distinct("Restaurant_Name", {"$and": [{"Dining_Rating": {"$gte": rating}}, {"Pricing_for_2": {"$lte": price}}]})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Neighborhood at Latitude and Longitude
@app.route('/neighborhood/<float:latitude>/<float:longitude>', methods=['GET'])
def get_neighborhood_at_location(latitude, longitude):
    # test with latitude: 18.51609685, longitude: 73.861532527
    results = collection_wards.find({"geometry": {"$geoIntersects": {"$geometry": {"type": "Point", "coordinates": [longitude, latitude]}}}})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Neighborhood Name at Latitude and Longitude
@app.route('/neighborhoodname/<float:latitude>/<float:longitude>', methods=['GET'])
def get_neighborhood_name_at_location(latitude, longitude):
    # test with latitude: 18.51609685, longitude: 73.861532527
    results = collection_wards.distinct("properties.name", {"geometry": {"$geoIntersects": {"$geometry": {"type": "Point", "coordinates": [longitude, latitude]}}}})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurants near Neighborhood at Latitude and Longitude
@app.route('/neighborhoodrestaurants/<float:latitude>/<float:longitude>', methods=['GET'])
def get_restaurants_near_neighborhood_at_location(latitude, longitude):
    # test with latitude: 18.51609685, longitude: 73.917229135
    neighborhood = collection_wards.find_one({"geometry": {"$geoIntersects": {"$geometry": {"type": "Point", "coordinates": [longitude, latitude]}}}})
    results = collection_restaurants2.find({"Location": {"$geoWithin": {"$geometry": neighborhood["geometry"]}}})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Names Known For Atmosphere
@app.route('/restaurantatmosphere/<string:knownforatmosphere>',methods=['GET'])
def get_restaurant_name_by_atmosphere(knownforatmosphere):
    # test with knownforatmosphere: Healthy Food Options
    results = collection_restaurants.distinct("Restaurant_Name", {"Known_for_Atmosphere": knownforatmosphere})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response

# Get Restaurant Names Known For Atmosphere
@app.route('/restaurantfood/<string:knownforfood>',methods=['GET'])
def get_restaurant_name_by_food(knownforfood):
    # test with knownforatmosphere: Valet
    results = collection_restaurants.distinct("Restaurant_Name", {"Known_for_Food": knownforfood})
    results_sanitized = json.loads(json_util.dumps(results))
    response = jsonify(results_sanitized)
    return response


@app.route('/', methods=['GET'])
def home():
    message = ("<h1>Welcome to the Pune, India Restaurants Python API!</h1>"
    "<p>Restaurant(s) with Category</p>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/category/Steak'>/category/Steak</a> to get all restaurants with a category of Steak</li>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/categoryrestnames/Steak'>/categoryrestnames/Steak</a> to get all restaurant names with a category of Steak</li>"
    "<p>Restaurant(s) at/near Location</p>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurants/18.56184774/73.917229135'>/restaurants/18.56184774/73.917229135</a> to get all restaurants near latitude: 18.56184774 and longitude: 73.917229135</li>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurantnames/18.56184774/73.917229135'>/restaurantnames/18.56184774/73.917229135</a> to get all restaurant names near latitude: 18.56184774 and longitude: 73.917229135</li>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurantname/18.53257323/73.87665387'>/restaurantname/18.53257323/73.87665387</a> to get the restaurant name at latitude: 18.53257323 and longitude: 73.87665387</li>"
    "<p>Restaurant(s) with Certain Rating and/or Price</p>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurantdelivery/4.5'>/restaurantdelivery/4.5</a> to get the restaurant name(s) with a delivery rating of 4.5 or greater</li>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurantdining/4.5'>/restaurantdining/4.5</a> to get the restaurant name(s) with a dining rating of 4.5 or greater</li>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurantdiningandprice/4.5/3700'>/restaurantdiningandprice/4.5/3700</a> to get the restaurant name(s) with a dining rating of 4.5 or greater and pricing for 2 that is 3700 rupees or less</li>"
    "<p>Neighborhood at Location</p>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/neighborhood/18.51609685/73.861532527'>/neighborhood/18.51609685/73.861532527</a> to get the neighborhood at latitude: 18.51609685 and longitude: 73.861532527</li>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/neighborhoodname/18.51609685/73.861532527'>/neighborhoodname/18.51609685/73.861532527</a> to get the neighborhood name at latitude: 18.51609685 and longitude: 73.861532527</li>"
    "<p>Restaurants near Neighborhood at Location</p>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/neighborhoodrestaurants/18.51609685/73.917229135'>/neighborhoodrestaurants/18.51609685/73.917229135</a> to get the restaurants near the neighborhood at latitude: 18.51609685 and longitude: 73.917229135</li>"
    "<p>Restaurant(s) known for Atmosphere/Food</p>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurantatmosphere/Healthy Food Options'>/restaurantatmosphere/Healthy Food Options</a> to get all restaurant names known for an atmosphere with Healthy Food Options</li>"
    "<li>Try <a href='https://cit374newmongoproject-dvann.uc.r.appspot.com/restaurantfood/Valet'>/restaurantfood/Valet</a> to get all restaurant names known for Valet as a food option</li>")
    return message


if __name__ == '__main__':
    # This is used when running locally only.
    app.run(host='127.0.0.1', port=8080, debug=True)