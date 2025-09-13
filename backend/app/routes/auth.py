from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.revoked_token import RevokedToken
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username, email, password = data.get("username"), data.get("email"), data.get("password")

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(RevokedToken(jti=jti))
    db.session.commit()
    return jsonify({"msg": "Successfully logged out"}), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return jsonify({"access_token": create_access_token(identity=identity)})
