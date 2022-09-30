import calendar

from flask import Flask, render_template, request
from datetime import date
from pymongo import MongoClient
from init_db import *

app = Flask(__name__)

""" Data base operations"""
client = MongoClient('localhost', 27017)
db = client.flask_db
exer = db.exercises
# Clear DB
exer.drop()
# Init DB
fill_db(exer)


def get_docs_via_month(month):
    this_year = date.today().year
    docs = exer.find({'$expr': {
        '$and': [
            {'$eq': [{'$month': {'$toDate': "$date"}}, month]},
            {'$eq': [{'$year': {'$toDate': "$date"}}, this_year]},
        ],
    }, }).distinct("date")
    return list(docs)


def exercise_in_month():
    """
    :return:the number of days in which the user entered anything in one month period (the current month for the current year)
    """
    this_month = date.today().month
    list_cur = get_docs_via_month(this_month)
    return len(list_cur)


def max_month_exercises():
    """
    :return: the month which has the highest number of days which have entries in the current year
    """
    days_exercised_month = {}
    max = [0,0]

    for i in range(1,13):
        list_cur = get_docs_via_month(i)
        days_exercised_month[i] = len(list_cur)
        if days_exercised_month[i] > max[0]:
            max[0] = days_exercised_month[i]
            max[1] = i

    return calendar.month_name[max[1]]


@app.route('/', methods = ['GET'])
def start_main():  # put application's code here
    today = str(date.today())
    best_month = max_month_exercises()
    exercised_days = exercise_in_month()
    return render_template("blog-single.html", date=today, best_month=best_month, exercised_days=exercised_days)


@app.route("/", methods = ['POST'])
def add_sport():
    """
    enter exercises the user does per day he can enter multiple exercises per day it should be post endpoint
    (data required from user :exerciseName(string),hours(tinyint),mins(tinyint))
    """
    today = str(date.today())
    hours = int(request.form.get('hours'))
    minutes = int(request.form.get('minutes'))
    exerc_name = request.form.get('exercise_name')
    if hours < 24 and minutes < 60 and (hours > 0 or minutes > 0):
        before_insert(exer, today, exerc_name)
        exer.insert_one({'date': today, 'exercise': exerc_name, 'hours':hours, 'minutes': minutes})
    best_month = max_month_exercises()
    exercised_days = exercise_in_month()
    return render_template("blog-single.html", date=today, best_month=best_month, exercised_days=exercised_days)


if __name__ == '__main__':
    app.run()
