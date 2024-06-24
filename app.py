from flask import Flask, request, jsonify, render_template  
import random
from datetime import datetime


app = Flask(__name__)

trash_dict = {
    "Lunes": "Organico", 
    "Martes": "Plastica",
    "Miercoles": "Organico",
    "Jueves": "Carta e Cartone",
    "Viernes": "Organico",
    "Domingo": "Indifferenziato",
}


def get_current_week_seed():
    now = datetime.now()
    return now.year * 100 + now.isocalendar()[1]

@app.route('/distribute', methods=['GET'])
def distribute():
    names = request.args.getlist('names')
    objects = request.args.getlist('objects')

    # if not names or not objects:
    #     return jsonify({'error': 'Invalid input'}), 400
    
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

    # return jsonify(distribution)
    # return render_template('result.html', distribution=distribution)

    # Get current week and date
    now = datetime.now()
    current_week = now.isocalendar()[1]
    current_date = now.strftime("%Y-%m-%d")

    return render_template('result.html', distribution=distribution, current_week=current_week, current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True, port=80)
