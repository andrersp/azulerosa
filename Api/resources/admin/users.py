# -*- coding: utf-8 -*-

from datetime import timedelta

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required, get_jwt_identity

from model.users import ModelsUser

from wraps import required_params

from blacklist import BLACKLIST


ns_user = Namespace("Gerenciamento de Usuarios",
                    description="Endpoint para gerencimento de usuário")


schema = {
    "id": {"type": "numeric", "required": True, "description": "String vazia ou Int com o ID do produto"},
    "username": {"type": "string", "required": True, "empty": False, "description": "Username, Max: 80 Caracteres"},
    "password": {"type": "string", "required": True, "empty": False, "description": "Password, Max: 80 Caracteres"},
    "enable": {"type": "boolean", "required": True, "empty": False, "description": "Se usuário é habilitado a fazer login."},
}


@ns_user.route("")
class Users(Resource):
    @jwt_required
    def get(self):
        """
        Retorna uma lista com todos os usuários cadastrados
        """
        print(get_jwt_identity())

        return {"data": [user.list_users() for user in ModelsUser.query.all()]}, 200

    @jwt_required
    @ns_user.doc(params=schema)
    @required_params(schema)
    def post(self):
        """
        Adicionar ou Editar novo usuário.
        Para criar envie string vazia em id e para editar envie um int com o ID do usuário
        """
        data = request.json

        user = ModelsUser.find_user(data.get("id"))

        if user:
            return {"message": "update"}, 200

        username = ModelsUser.find_username(data.get("username"))

        if username:
            return {"message": "Nome de usuário já existe. Tente outro."}, 400

        try:

            user = ModelsUser(**data)
            user.generate_hash()
            user.save_user()

            return {"message": "Usuário criado", "data": user.list_users()}, 201

        except Exception as err:
            print(err)


schema = {
    "username": {"type": "string", "required": True, "empty": False, "description": "Nome de usuário para login"},
    "password": {"type": "string", "required": True, "empty": False, "description": "Senha do usuário"}
}

ns_login = Namespace("Login", description="Endpoint Login")


@ns_login.route("")
class UserLogin(Resource):

    @required_params(schema)
    @ns_login.doc(params=schema)
    def post(self):
        """
        Realizar Login para receber o token de acesso
        """

        data = request.json

        user = ModelsUser.find_username(data.get("username"))

        if user and user.check_password(data.get("password")):

            if user.enable:
                expire = timedelta(hours=12)
                token = create_access_token(
                    identity=user.list_users(), expires_delta=expire)
                return {"data": {"id": user.id_user,  "token": token}}, 200

            return {"message": "Usuário desabilitado. Contate o suporte"}, 400
        return {"message": "Usuário ou senha incorretos. Tente Novamente."}, 400


ns_logout = Namespace("Logout", description="Endpoint Logout")


@ns_logout.route("")
class UserLogin(Resource):

    @jwt_required
    def post(self):
        """
        Realizar Logout para revogar Token de acesso. 
        """

        jwt_id = get_raw_jwt()["jti"]
        BLACKLIST.add(jwt_id)

        return {"message": "Logout realizado com sucesso!"}, 200
