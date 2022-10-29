"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
import datetime

api = Blueprint('api', __name__)


@api.route('/signup', methods=['POST', 'GET'])
def signup():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/login', methods=['POST'])
def login():

    body = request.get_json()

    user= User.query.filter_by(email=body['email']).first()
    if(user):
        if (user.password == body['password']):
            
            expiracion = datetime.timedelta(minutes=1)
            token = create_access_token(identity=body['email'], expires_delta= expiracion)
            return jsonify({
        "email": body['email'],
        "mensaje" : "Bienvenido",
        "token": token
    })
        else:
            return jsonify({"mensaje": "Ocurrio un error"})
    else:
        return jsonify({"mensaje": "Usuario no existe"})


@api.route('/private', methods=['GET'])
@jwt_required()
def autenticacion():

   if request.method == 'GET':
        iden= get_jwt_identity()
        return jsonify({"Mensaje ": "Acceso a espacio privado concedido, Bienvenido" , "usuario": iden}), 200