import datetime
from flask_restful import reqparse, Resource
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_raw_jwt)
from werkzeug.security import safe_str_cmp


import re

# local imports
from ..models.auth import userModel
from ...middleware.middleware import both_roles_allowed


class RegisterResource(Resource):
    """
        Register user endpint
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('confirm_password', type=str, required=True)
    parser.add_argument('role', type=int, required=True)
    parser.add_argument('email', type=str, required=True)

    def post(self):
        data = RegisterResource().parser.parse_args()

        # validations for input
        # eliminate space in username
        username = ''.join(data['username'].split())
        role_id = [1, 2]

        if not re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                data['email']):
            return {"message": "invalid email"}, 422
        elif len(data['password']) < 6:
            return {"message":
                    "password should atleast six characters long"}
        elif data['role'] not in role_id:
            return {"message": "role id should either be 1 or 2"}
        elif data['username'] == "":
            return {"message": "username should not be empty"}
        elif data['confirm_password'] != data["password"]:
            return {"message": "passwords do not match"}

        # increment Id
        user_id = userModel.get_length(userModel.get_users()) + 1

        if userModel.get_by_name(data['email'], userModel.get_users()):
            return {"message": "user with email already registred"}, 409

        user_data = {
            "id": user_id, "username": username,
            "email": data["email"], "password": data["password"],
            "role": data["role"]}

        userModel.add_user((user_data))
        user = userModel.get_by_id(user_id, userModel.get_users())
        return {"message": "registration sucessfull"}, 201


class LoginResource(Resource):

    """
        Login user endpoint
    """
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        data = LoginResource.parser.parse_args()

        # validate email

        if not re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                data['email']):
            return {"message": "invalid email"}, 422

        if userModel.get_length(userModel.get_users()) == 0:
            return {"message": "please register"}
        # check if user exists
        user = userModel.get_by_name(data['email'], userModel.get_users())
        # check if password match
        if user and safe_str_cmp(user['password'], data['password']):

            # extend expire time
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=user,
                                               expires_delta=expires)

            return{"access_token": access_token, "message": "logged in"}, 200
        return {"message": "invalid credentials"}, 422


class LogoutResource(Resource):
    """
        logout endpoint
    """

    @both_roles_allowed
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklisted = userModel.blacklist(jti)
        return {"message": "logged out"}, 200
