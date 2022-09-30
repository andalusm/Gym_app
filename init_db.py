import random
import time


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)


def fill_db(exercise_db):
    """

    :param exercise_db: dataset with all the exercises for a given user
    :return: fills the dataset with 100 entries
    """
    for i in range(50):
        date = random_date("2022-09-22", "2022-01-01", random.random())
        hours = random.randint(0, 24)
        minutes = random.randint(0, 60)
        exerc_name = random.choice(['Swimming', 'Running', 'Yoga', 'Weight lifting'])
        if hours < 24 and minutes < 60 and (hours > 0 or minutes > 0):
            before_insert(exercise_db, date, exerc_name)
            exercise_db.insert_one({'date': date, 'exercise': exerc_name, 'hours': hours, 'minutes': minutes})
            if random.random() > 0.5:
                exerc_name = random.choice(['Swimming', 'Running', 'Yoga', 'Weight lifting'])
                before_insert(exercise_db, date, exerc_name)
                exercise_db.insert_one({'date': date, 'exercise': exerc_name, 'hours': hours, 'minutes': minutes})


def before_insert(exercise_db, date, name):
    docs = exercise_db.find({'$expr': {
        '$and': [
            {'$eq': ['$date', date]},
            {'$eq': ['$exercise', name]},
        ],
    }})
    if len(list(docs)) > 0:
        exercise_db.delete_one({'$expr': {
            '$and': [
                {'$eq': ['$date', date]},
                {'$eq': ['$exercise', name]},
            ],
        }})