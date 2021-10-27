# Importing our tools for web app development
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# Tell Python to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, 
# a uniform resource identifier similar to a URL.
#"mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, 
# using a database named "mars_app".

# The code we create next will set up our Flask routes: one for the main HTML page everyone will 
# view when visiting the web app, and one to actually scrape new data using the code we've written.

# Define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Set up our scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
   app.run()