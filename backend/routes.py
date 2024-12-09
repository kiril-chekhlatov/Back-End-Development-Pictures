from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """
    Return all pictures as a JSON response.
    """
    if not data:
        return {"message": "No data found"}, 404

    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """
    Get a specific picture by ID.
    """
    # Search for the picture with the given ID
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture:
        return jsonify(picture), 200
    
    return {"message": f"Picture with ID {id} not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """
    Create a new picture.
    """
    if not request.is_json:
        return {"Message": "Request body must be JSON"}, 400

    new_picture = request.get_json()

    # Check for duplicate ID
    if any(p["id"] == new_picture["id"] for p in data):
        return {"Message": f"picture with id {new_picture['id']} already present"}, 302

    # Add the new picture to the dataset
    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """
    Update an existing picture by ID.
    """
    if not request.is_json:
        return {"message": "Request body must be JSON"}, 400

    updated_picture = request.get_json()

    # Find the picture to update
    picture = next((item for item in data if item["id"] == id), None)

    if not picture:
        return {"message": f"Picture with ID {id} not found"}, 404

    # Update the fields
    picture.update(updated_picture)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """
    Delete a picture by ID.
    """
    global data
    original_length = len(data)
    data = [item for item in data if item["id"] != id]
    
    if len(data) < original_length:
        return "", 204  # Return 204 No Content for successful deletion
    
    return {"Message": f"Picture with ID {id} not found"}, 404
