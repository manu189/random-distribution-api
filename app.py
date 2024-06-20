from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/distribute', methods=['GET'])
def distribute():
    names = request.args.getlist('names')
    objects = request.args.getlist('objects')

    if not names or not objects:
        return jsonify({'error': 'Invalid input'}), 400

    # Shuffle objects
    random.shuffle(objects)

    # Distribute objects
    distribution = {name: [] for name in names}
    for i, obj in enumerate(objects):
        person = names[i % len(names)]
        distribution[person].append(obj)

    return jsonify(distribution)

if __name__ == '__main__':
    app.run(debug=True)
