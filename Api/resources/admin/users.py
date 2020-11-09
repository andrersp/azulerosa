# -*- coding: utf-8 -*-

from datetime import timedelta

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required, get_jwt_identity

from model.users import ModelsUser

from cerberus_validate import CustomValidator

from blacklist import BLACKLIST


schema = {
    "username": {"type": "string", "required": True, "empty": False, "description": "Username, Max: 80 Caracteres"},
    "password": {"type": "string", "required": True, "empty": False, "description": "Password, Max: 80 Caracteres"},
    "enable": {"type": "boolean", "required": True, "empty": False, "description": "Se usuário é habilitado a fazer login."},
}


class UsersApi(MethodView):
    @jwt_required
    def get(self, user_id):
        """
        Retorna uma lista com todos os usuários cadastrados
        """

        if user_id:
            user = ModelsUser.find_user(user_id)
            if user:
                return jsonify({"data": user.list_users()}), 200

            return jsonify({"message": "User not found"}), 404

        return jsonify({"data": [user.list_users() for user in ModelsUser.query.all()]}), 200

    @jwt_required
    def post(self):
        """
        Adicionar ou Editar novo usuário.
        Para criar envie string vazia em id e para editar envie um int com o ID do usuário
        """
        data = request.json if request.json else{}

        v = CustomValidator(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document

        username = ModelsUser.find_username(data.get("username"))

        if username:
            return jsonify({"message": "Nome de usuário já existe. Tente outro."}), 400

        try:

            user = ModelsUser(**data)
            user.generate_hash()
            user.save_user()

            return jsonify({"message": "Usuário criado", "data": user.list_users()}), 201

        except:

            return jsonify({"message": "Internal Error"}), 500

    @jwt_required
    def put(self, user_id):

        data = request.json if request.json else{}

        v = CustomValidator(schema)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document

        user = ModelsUser.find_user(user_id)

        if not user:
            return jsonify({"message": "user not Found"}), 404

        username = ModelsUser.find_username(data.get("username"))

        if username:
            if len(username) > 1 or username[0] != user_id:
                return jsonify({"message": "Nome de usuário já existe. Tente outro."}), 400

        try:
            user.update_user(**data)
            user.generate_hash()
            user.save_user()

            return jsonify({"message": "User Updated", "data": user.list_users()}), 200

        except:

            return jsonify({"message": "Internal error"})


schema_login = {
    "username": {"type": "string", "required": True, "empty": False, "description": "Nome de usuário para login"},
    "password": {"type": "string", "required": True, "empty": False, "description": "Senha do usuário"}
}


class LoginApi(MethodView):

    def post(self):
        """
        Realizar Login para receber o token de acesso
        """

        data = request.json if request.json else{}

        v = CustomValidator(schema_login)

        if not v.validate(data):
            return jsonify({"message": v.errors}), 400

        data = v.document

        user = ModelsUser.user_login(data.get("username"))

        if not user:
            return jsonify({"message": "User Or Password Error"}), 401

        if not user.check_password(data.get("password")):
            return jsonify({"message": "User Or Password Error"}), 401

        if not user.enable:
            return jsonify({"message": "Usuário desabilitado. Contate o suporte"}), 401

        expire = timedelta(hours=12)
        token = create_access_token(
            identity=user.list_users(), expires_delta=expire)
        return jsonify({"data": {"id": user.id_user,  "token": token}}), 200


class LogoutApi(MethodView):

    @jwt_required
    def post(self):
        """
        Realizar Logout para revogar Token de acesso.
        """

        jwt_id = get_raw_jwt()["jti"]
        BLACKLIST.add(jwt_id)

        return jsonify({"message": "Logout realizado com sucesso!"}), 200
