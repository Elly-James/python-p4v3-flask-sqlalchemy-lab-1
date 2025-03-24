# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)  # Query the database for the earthquake by ID
    
    if earthquake:
        # If the earthquake is found, return the earthquake's attributes as JSON
        return jsonify({
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }), 200
    else:
        # If the earthquake is not found, return an error message
        return jsonify({'message': f'Earthquake {id} not found.'}), 404





# Add view for getting earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query to find earthquakes with magnitude greater than or equal to the given magnitude
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Check if any earthquakes are found
    if quakes:
        # Prepare the response with the count and details of the earthquakes
        return jsonify({
            'count': len(quakes),
            'quakes': [
                {
                    'id': quake.id,
                    'location': quake.location,
                    'magnitude': quake.magnitude,
                    'year': quake.year
                }
                for quake in quakes
            ]
        }), 200
    else:
        # If no earthquakes found, return a count of 0 and an empty list
        return jsonify({
            'count': 0,
            'quakes': []
        }), 200





if __name__ == '__main__':
    app.run(port=5555, debug=True)
