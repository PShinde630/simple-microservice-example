from flask import Flask
from flask import jsonify
from pymongo import MongoClient
import redis

def getdb():
    client = MongoClient(host='localhost',
                         port=27017,
                         username='admin',
                         password='admin',
                         authSource="admin")
    db = client["quotedb"]
    return db

def getredis():
    r = redis.Redis(host='127.0.0.1',
                    port=6379)
    return r


a quote
class Quote(object):
    def init(self, quote, by):
        self.quote = quote
        self.by = by

# # Loads quotes from a file
def loadQuotes():
with open(QUOTES_FILE) as file:
lines = file.readlines()
lines = [x.strip() for x in lines]
for line in lines:
quote, by = line.split("-")
quotes.append(Quote(quote, by))
app = Flask(name)

Gets a random quote
@app.route("/api/quote")
def quote():
    db=""
    try:
        db = getdb()
        r = get_redis()
        count = r.get("count")
        if count is None:
            r.set("count", 1)
            count = 0
        else:
            count = int(count) + 1
            r.set("count", count)
        pipe2 = [{ '$sample': { 'size': 1 } }]
        result = db.quote_tb.aggregate(pipeline=pipe2).try_next()
        app.logger.info(type(result))
        app.logger.info(result)
        if result:
            return jsonify({"quote": result['quote'], "by": result['author'], "count": count})
        else:
            return jsonify({"quote": "No quotes found", "by": "Unknown", "count": count})
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()

404 Erorr for unknown routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Resource not found"}), 404

if __name == '__main':
    app.run(host='0.0.0.0', port=5000, debug=True) # run application
