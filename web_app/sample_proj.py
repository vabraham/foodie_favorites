from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import psycopg2
from random import sample
 
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/sample_proj'
# db = SQLAlchemy(app)
 

# Create our database model
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, email):
#         self.email = email

#     def __repr__(self):
#         return '<E-mail %r>' % self.email


# class Restaurant(db.Model):
#     __tablename__ = 'restaurants'
#     id = db.Column(db.Integer, primary_key=True)
#     rest_id = db.Column(db.Integer)
#     rest_name = db.Column(db.String(120))
#     menu_item = db.Column(db.String(120))
#     menu_section = db.Column(db.String(120))
#     count = db.Column(db.Integer)

#     def __init__(self, rest_id, rest_name, menu_item, menu_section, count):
#         self.rest_id = rest_id
#         self.rest_name = rest_name
#         self.menu_item = menu_item
#         self.menu_section = menu_section
#         self.count = self.count


# Set "homepage" to index.html
@app.route('/')
def index():
    conn = psycopg2.connect(database='sample_proj', user='vabraham24', host="/tmp/")
    c = conn.cursor()
    c.execute("""   SELECT DISTINCT(city)
            FROM restaurants
            ORDER BY city; """)
    cities = c.fetchall()
    # c.execute("""   SELECT DISTINCT(rest_name)
    #         FROM restaurants
    #         ORDER BY rest_name; """)
    # rests = c.fetchall()
    conn.close()
    sample_cities = [x[0] for x in cities]
    # sample_rests = [x[0] for x in rests]
    return render_template('index.html', sample_cities=sample_cities)
    # , sample_rests=sample_rests

# Save e-mail to database and send to success page
@app.route('/city/<city_name>', methods=['GET','POST'])
def city(city_name):
    # return "test"
    # return request.form['item']
    name = city_name
    # name = str(name)
    # return restaurant_name
    # if request.method == 'GET':
    conn = psycopg2.connect(database='sample_proj', user='vabraham24', host="/tmp/")
    c = conn.cursor()
    c.execute("""   SELECT DISTINCT(rest_name)
        FROM restaurants
        WHERE city = %s
        ORDER BY rest_name; """, (name,))
    rests = c.fetchall()
    conn.close()
    sample_rests = [x[0] for x in rests]
    return render_template('restaurants.html', sample_rests=sample_rests)
    # , name=name
    # return render_template('index.html')


# Save e-mail to database and send to success page
@app.route('/restaurant/<restaurant_name>', methods=['GET', 'POST'])
def restaurant(restaurant_name):
    name = restaurant_name
    zingers = ["Bingo!", "Yum!", "And the votes are in...", "De-licious"]
    phrase = sample(zingers, 1)[0]
    conn = psycopg2.connect(database='sample_proj', user='vabraham24', host="/tmp/")
    c = conn.cursor()
    c.execute("""   SELECT menu_item
        FROM restaurants
        WHERE rest_name = %s
        ORDER BY count DESC
        LIMIT 10    ; """, (name,))
    menu = c.fetchall()
    conn.close()
    menu_items = [x[0] for x in menu]
    return render_template('success.html', menu_items=menu_items, name=name,
        phrase=phrase)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8090)