from flask import Flask, request, jsonify
import random
import datetime


app = Flask(__name__)

def get_current_week_seed():
    now = datetime.now()
    return now.year * 100 + now.isocalendar()[1]

@app.route('/distribute', methods=['GET'])
def distribute():
    names = request.args.getlist('names')
    objects = request.args.getlist('objects')

    if not names or not objects:
        return jsonify({'error': 'Invalid input'}), 400

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

    return jsonify(distribution)

if __name__ == '__main__':
    app.run(debug=True, port=80)
