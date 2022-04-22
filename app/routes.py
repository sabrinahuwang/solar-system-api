from flask import Blueprint, jsonify

class Planet: 
    def __init__(self, id, name, description, size):
        self.id = id
        self.name = name
        self.description = description
        self.size = size

planets = [
    Planet(978, "Venus", "67 miles from the sun", "3,760.4 miles"),
    Planet(879, "Mercury", "36 million miles from the sun", "1,516 miles"),
    Planet(696, "Earth", "92,960,000 miles from the sun", "3,963 miles")
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

