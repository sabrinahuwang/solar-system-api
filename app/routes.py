from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app import db


# class Planet: 
#     def __init__(self, id, name, description, size):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.size = size

# planets = [
#     Planet(1, "Venus", "67 miles from the sun", "3,760.4 miles"),
#     Planet(2, "Mercury", "36 million miles from the sun", "1,516 miles"),
#     Planet(3, "Earth", "92,960,000 miles from the sun", "3,963 miles")
# ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planet():
    planets = Planet.query.all()
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

@planets_bp.route("", methods=["POST"])

def create_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"],
    description=request_body["description"],
    size=request_body["size"])

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created", 201)

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
    except:
        abort(make_response({"message": f"Invalid planet id: '{planet_id}'"}, 400))
    planet = Planet.query.get(planet_id)
    if planet:
        return planet

    abort(make_response({"message": f'planet id {planet_id} not found'}, 404))


@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate(planet_id)
    request_body = request.get_json()
    if "name" not in request_body or \
        "description" not in request_body \
        or "size" not in request_body:
        return jsonify({'msg': f"Request must include name, description, and size"})

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.size = request_body["size"]

    db.session.commit()

    return jsonify({'msg': f"Planet {planet_id} update successful!"})


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{planet.id} successfully deleted")