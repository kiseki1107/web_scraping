# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask app
app = Flask(__name__)

# Use flask_PyMongo to establish Mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app") # This is an inline PyMongo setting

# Create index route
@app.route("/")
def index(): 
    mars_dict = mongo.db.mars_dict.find_one()
    #mars_dict = scrape_mars.scrape()
    return render_template("index.html", mars_dict=mars_dict)

# Create scrape route
@app.route("/scrape")
def scrape(): 
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    mars_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)