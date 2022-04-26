from flask import Blueprint, jsonify, abort, make_response

class Planet: 
    def __init__(self, id, name, description, size):
        self.id = id
        self.name = name
        self.description = description
        self.size = size

planets = [
    Planet(1, "Venus", "67 miles from the sun", "3,760.4 miles"),
    Planet(2, "Mercury", "36 million miles from the sun", "1,516 miles"),
    Planet(3, "Earth", "92,960,000 miles from the sun", "3,963 miles")
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planet():
    response = []
    for planet in planets:
        response.append(
            {"id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "size": planet.size
            }
        )
    
    return jsonify(response)

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate(planet_id)
    return jsonify(
            {"id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "size": planet.size
            }
        )

def validate(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({"message": f"Invalid planet id: '{planet_id}'"}, 400))
    
    for planet in planets:
        if planet_id == planet.id:
            return planet
    abort(make_response({"message": f'planet id {planet_id} not found'}, 404))
