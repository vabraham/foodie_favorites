from flask import Flask, render_template
from random import sample
import psycopg2


app = Flask(__name__)


# Set "homepage" to index.html
@app.route('/')
def index():
    conn = psycopg2.connect(database='yelp', user='postgres',
                            password='testing1')
    c = conn.cursor()
    c.execute("""   SELECT DISTINCT(city)
            FROM restaurants
            ORDER BY city; """)
    cities = c.fetchall()
    conn.close()
    sample_cities = [x[0] for x in cities]
    return render_template('index.html', sample_cities=sample_cities)


@app.route('/city/<city_name>', methods=['GET', 'POST'])
def city(city_name):
    city_name = city_name
    conn = psycopg2.connect(database='yelp', user='postgres',
                            password='testing1')
    c = conn.cursor()
    c.execute("""   SELECT DISTINCT(rest_name)
        FROM restaurants
        WHERE city = %s
        ORDER BY rest_name; """, (city_name,))
    rests = c.fetchall()
    conn.close()
    sample_rests = [x[0] for x in rests]
    return render_template('restaurants.html', sample_rests=sample_rests,
                           city_name=city_name)


@app.route('/restaurant/<city_name>/<restaurant_name>',
           methods=['GET', 'POST'])
def restaurant(restaurant_name, city_name):
    name = restaurant_name
    city = city_name
    zingers = ["Bingo!", "Yum!", "And the votes are in...", "De-licious"]
    phrase = sample(zingers, 1)[0]
    conn = psycopg2.connect(database='yelp', user='postgres',
                            password='testing1')
    c = conn.cursor()
    c.execute("""   SELECT menu_item
        FROM restaurants
        WHERE rest_name = %s
        AND city = %s
        ORDER BY count DESC
        LIMIT 10    ; """, (name, city))
    menu = c.fetchall()
    conn.close()
    menu_items = [x[0] for x in menu]
    return render_template('success.html', menu_items=menu_items,
                           name=name, phrase=phrase)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
