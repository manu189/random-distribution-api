from flask import Flask, request, jsonify, render_template  
import random
from datetime import datetime


app = Flask(__name__)

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
    random.shuffle(names)

    # Distribute objects
    distribution = {name: [] for name in names}
    for i, obj in enumerate(objects):
        person = names[i % len(names)]
        distribution[person].append(obj)

    # return jsonify(distribution)
    return render_template('result.html', distribution=distribution)

if __name__ == '__main__':
    app.run(debug=True, port=80)
