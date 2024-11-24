# from flask import Flask, jsonify
# from pymongo import MongoClient, errors as mongo_errors
# import redis


# def get_db():
#     client = MongoClient(host='mongodb_container',
#                             port=27017,
#                             username='root',
#                             password='pass',
#                             authSource="admin")
#     db = client["quote_db"]

#     return db


# def get_redis():
#     r = redis.Redis(host='container_of_redis', port=6379)
#     return r


# # Quote class
# class Quote:
#     def __init__(self, quote, by):
#         self.quote = quote
#         self.by = by


# app = Flask(__name__)



# # Getting the random quote 
# @app.route("/api/quote")
# def quote():
#     try:
#         db = get_db()
#         r = get_redis()
#         count = r.get("count")
#         if count is None:
#             r.set("count", 1)
#             count = 0
#         else:
#             count = int(count) + 1
#             r.set("count", count)


#         # a random quote fetched from the Mongo
#         pipe2 = [{'$sample': {'size': 1}}]
#         result = db.quote_tb.aggregate(pipeline=pipe2).try_next()


#         app.logger.info(type(result))
#         app.logger.info(result)


#         if result:
#             return jsonify({"quote": result['quote'], "by": result['author'], "count": count})
#         else:
#             return jsonify({"quote": "No quotes found", "by": "Unknown", "count": count})


#     except:
#         pass
#     finally:
#         if type(db)==MongoClient:
#             db.close()


# # 404 Error handler for unknown routes
# @app.errorhandler(404)
# def page_not_found(e):
#     app.logger.error(f"404 Error: {e}")
#     return jsonify({"message": "Resource not found"}), 404


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)  # Run the application




from flask import Flask, jsonify
from pymongo import MongoClient, errors as mongo_errors
import redis
import os
import json

# Default static IPs
DEFAULT_MONGO_HOST = "192.168.1.2"
DEFAULT_REDIS_HOST = "192.168.1.5"

# Path to shared configuration file
CONFIG_FILE_PATH = "/shared-data/config.json"

# Load configuration from `config.json` or fallback to static IPs
mongo_host = DEFAULT_MONGO_HOST
redis_host = DEFAULT_REDIS_HOST

if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, "r") as config_file:
        config = json.load(config_file)
        mongo_host = config.get("mongoServiceUrl", DEFAULT_MONGO_HOST)
        redis_host = config.get("redisServiceUrl", DEFAULT_REDIS_HOST)

app = Flask(__name__)

# Function to connect to MongoDB
def get_db():
    try:
        client = MongoClient(
            host=mongo_host,
            port=27017,
            username="root",
            password="pass",
            authSource="admin"
        )
        db = client["quote_db"]
        return client, db
    except mongo_errors.PyMongoError as e:
        app.logger.error(f"MongoDB Connection Error: {e}")
        return None, None

# Function to connect to Redis
def get_redis():
    try:
        return redis.Redis(host=redis_host, port=6379)
    except redis.RedisError as e:
        app.logger.error(f"Redis Connection Error: {e}")
        return None

# Endpoint to fetch a random quote
@app.route("/api/quote", methods=["GET"])
def quote():
    client, db = get_db()
    if not db:
        return jsonify({"message": "Failed to connect to MongoDB"}), 500

    redis_client = get_redis()
    if not redis_client:
        return jsonify({"message": "Failed to connect to Redis"}), 500

    try:
        # Increment Redis counter
        count = redis_client.incr("quote_count")

        # Fetch a random quote from MongoDB
        pipeline = [{'$sample': {'size': 1}}]
        result = db.quote_tb.aggregate(pipeline).try_next()

        if result:
            return jsonify({
                "quote": result['quote'],
                "by": result['author'],
                "count": count
            })
        else:
            return jsonify({
                "quote": "No quotes found",
                "by": "Unknown",
                "count": count
            })
    except Exception as e:
        app.logger.error(f"Error fetching quote: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if client:
            client.close()

# 404 Error handler
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
