from flask_jwt_extended import JWTManager
from flask import Flask
from .models import Token
from datetime import datetime, timedelta

def setup_jwt(app: Flask):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_database(jwt_header, jwt_payload):
        token = jwt_payload['jti']
        token_entry = Token.query.filter_by(token=token, is_active=True).first()
        return token_entry is None

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # This function can be used to add additional claims to the JWT payload
        return {
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
            "nbf": datetime.utcnow(),
            "jti": identity
        }

    return jwt

