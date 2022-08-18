from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from config import app_db
import scraping

app = Flask(__name__)

app.config["MONGO_URI"] = app_db     # Localhost:27017/mars_app
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/update")
def update():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect("/", code=302)




if __name__ == "__main__":
    app.run()