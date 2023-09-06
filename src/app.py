import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, CharacterPeople

app = Flask(__name__)
app.url_map.strict_slashes = False

# Set up database URL
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize app components
db.init_app(app)
Migrate(app, db)  # Initialize migration

# CORS setup
CORS(app)
setup_admin(app)

# Error handling for API exceptions
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap endpoint
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get a list of all people
@app.route('/people', methods=['GET'])
def get_all_people():
    people_list = CharacterPeople.query.all()
    people_data = [{"id": person.id, "name": person.name} for person in people_list]
    return jsonify(people_data)

# Get a single person's information
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = CharacterPeople.query.get(people_id)
    if person is None:
        raise APIException("Person not found", status_code=404)

    # Prepare the response data with person's attributes
    person_data = {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "email": person.email,
        "password": person.password,
        "planets": person.planets,
    }

    return jsonify(person_data)

# Get a list of all planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets_list = Planet.query.all()
    planets_data = [{"id": planet.id, "name": planet.name} for planet in planets_list]
    return jsonify(planets_data)

# Get a single planet's information
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    planet_data = {"id": planet.id, "name": planet.name, "population": planet.population}
    return jsonify(planet_data)

# Get a list of all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users_list = User.query.all()
    users_data = [{"id": user.id, "username": user.username} for user in users_list]
    return jsonify(users_data)

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(host='0.0.0.0', port=3000, debug=True)
