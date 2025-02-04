from flask import Flask, request, render_template, redirect, url_for
import random
from datetime import datetime
import locale
import pytz
from movies import get_movie_details


app = Flask(__name__)

# Set locale to Spanish
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

trash_dict = {
    "Lunes": "Organico", 
    "Martes": "Plastica",
    "Miércoles": "Organico",
    "Jueves": "Carta e Cartone",
    "Viernes": "Organico",
    "Domingo": "Indifferenziato",
}

days_of_week = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

def get_current_week_seed():
    now = datetime.now(pytz.timezone('Europe/Rome'))
    # now = datetime.now()
    return now.year * 100 + now.isocalendar()[1]

@app.route('/distribute', methods=['GET'])
def distribute():
    names = request.args.getlist('names')
    objects = request.args.getlist('objects')
    
    if not names or not objects:
        return render_template('result.html', error='Invalid input')

    seed = get_current_week_seed()
    random.seed(seed)

    # Shuffle objects
    random.shuffle(objects)
    objects = [f"{obj}: {trash_dict[obj]}" for obj in objects]
    random.shuffle(names)

    # Distribute objects
    distribution = {name: [] for name in names}
    for i, obj in enumerate(objects):
        person = names[i % len(names)]
        distribution[person].append(obj)

    now = datetime.now(pytz.timezone('Europe/Rome'))
    current_week = now.isocalendar()[1]
    current_date = now.strftime("%Y-%m-%d")
    current_day_of_week = now.strftime("%A")

    return render_template('result.html', distribution=distribution, current_week=current_week, current_date=current_date, current_day_of_week=current_day_of_week.title())

@app.route('/basura')
def basura():
    return redirect(url_for('distribute', 
        names=['Cele', 'Simo', 'Jime', 'Manu'], 
        objects=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Domingo']))

@app.route('/hoySeVe')
def index():
    movie_title, movie_link, movie_image = get_movie_details()
    return render_template('movies.html', title=movie_title, link=movie_link, image=movie_image)

if __name__ == '__main__':
    app.run(debug=True)
