import requests, json
import mysql.connector
from data import *

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="oof_db")

mycursor = db.cursor()

# mycursor.execute("CREATE DATABASE oof_db")
# mycursor = db.cursor()

# mycursor.execute("DROP TABLES off")


mycursor.execute("CREATE TABLE off(marque VARCHAR(200) NOT NULL, nom VARCHAR(200) NOT NULL, nutriscore VARCHAR(5), store VARCHAR(200) NOT NULL, category VARCHAR(20),code_id BIGINT, productID int PRIMARY KEY AUTO_INCREMENT)")

 
for category in categories:

    parameters= {
        "action": "process",
        "json": True,
        "page_size": 20,
        "tagtype_0": "categories",
        "tag_contains_0": 'contains',
        'tag_0': category,
        "page": 1
    }
    
    while parameters['page'] < 13:

        response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",  parameters)

        for i in range(len(response.json()["products"])):
            try:
                marque= response.json()["products"][i]["brands"]
                nom= response.json()["products"][i]["product_name"]
                nutriscore= response.json()["products"][i]["nutriscore_grade"]
                store= response.json()["products"][i]["stores"]
                code_id = response.json()["products"][i]["id"]

                mycursor.execute("INSERT INTO off (marque, nom, nutriscore,store, category, code_id) VALUES (%s,%s,%s,%s,%s,%s)",(marque,nom,nutriscore,store,category, code_id))
                db.commit()

            except KeyError:
                pass

        parameters['page'] += 1

    mycursor.execute("SELECT * FROM off")

 