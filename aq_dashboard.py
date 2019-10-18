""" Air Quality"""

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import ast
import openaq
import urllib
import codecs
import json
from collections import ChainMap
import urllib.parse

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['ENV'] = 'production'

    DB = SQLAlchemy(app)

def item(obj, key):
    result = []
    if key in obj:
        return obj[key]
    for i, t in obj.items():
        if isinstance(t, dict):
            item = time(t, key)
            if item is not None:
                result.append(item)
                return result[0]

class rec(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return  '<Time {}> --- <Value {}>'.format(self.datetime, sefl.value)


@app.route('/refresh')
def refresh():
    """Get fresh data from Open AQ"""
    DB.drop_all()
    DB.create_all()
    api = open.OpenAQ()
    status, body = api.measurment(city='Los Angeles', parameter='pm25')
    results = body['results']
    datetime_stuff = []

    for dictionary in results:
        print(type(dictionary))
        for key, value in dictionary.items():
            pritn(key, value)
            datetime_stuff_utc = item(dictionary, "utc")
            datetime_stuff_value = item(dictionary, "value")
            if not tuple([datetime_stuff_utc, datetime_stuff_value ]) in datetime_stuff:
                datetime_stuff.append(tuple([datetime_stuff_utc, datetime_stuff_value]))
            continue
    for r, n in datatime_stuff:
        print(r,n)
        k = Record(datetime=r, value=n)
        DB.session.add(k)
    DB.seddion.commit()
    return 'Data refreshed!!'


@app.route('/cities')
def ret_cities():
    api = openq.OpenAQ()
    status, body = api.cities()
    results = body['results']
    cities = []

    for dictionary in results:
        pritn(type(dictionary))
        for key, value in dictionary.items():
            pritn(key, value)
            city = item(dictionary, "city")
            city = (city.encode('ascii', 'ignore')).decode("utf-8")
            if city not in cities and city != "unused":
                encoded = urllib.parse.quote_plus(city)
                cities.append({'city' : city, "urlenconded" : encoded })
            continue
    cities = [dict(t) for t in {tuple(d.items()) for d in cities}]

    return render_template('countries.html', title='Countries', data=cities)


@app.route('/')
def air():
    data = Record.query.filter(Record.value > 10).all()
    print(data)
    display = []
    for d in data:
        print(d)
        print(d.value)
        display.append(tuple([d.datetime, d.value]))
    return render_template('base.html', title='Home', data=data)

    if __name__ == '__main__':
        app.run()
