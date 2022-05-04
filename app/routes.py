from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app import db

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

def validate(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"Invalid planet id: '{planet_id}'"}, 400))
    planet = Planet.query.get(planet_id)
    if planet:
        return planet

    abort(make_response({"message": f'planet id {planet_id} not found'}, 404))

@planets_bp.route("", methods=["GET"])
def get_all_planet():
    #planets = Planet.query.all()
    params = request.args
    if "name" in params and "description" in params:
        planet_name = params["name"]
        planet_description = params["description"]
        planets = Planet.query.filter_by(name = planet_name, description = planet_description)
    elif "description" in params:
        planet_description = params["description"]
        planets = Planet.query.filter_by(description = planet_description)
    elif "name" in params:
        planet_name = params["name"]
        planets = Planet.query.filter_by(name = planet_name)
    else:
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