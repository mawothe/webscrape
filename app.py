from flask import Flask
from flask import render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

#Create the instance of Flask
app = Flask(__name__)

#Pymongo to connect to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#home page
@app.route("/")
def home():
    try:
        #look for a record in the database
        mars_db = mongo.db.mars_information.find_one()
        
        #return and report (basically)
        return render_template("index.html", mars_db=mars_db)

    except:
        print("Hello! Please add (/scrape) to the end of the URL to scrape the data.")

#Route to start the scrape
@app.route("/scrape")
def scrape():

    #Run the scrape function which was imported
    new_info = mars_scrape.scrape()

    #Update the Mongo database
    mongo.db.mars_information.update({}, new_info, upsert=True)

    #Return to the home page
    return redirect("/")

if __name__ == "__main__" :
        app.run(debug=True)
