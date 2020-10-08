# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace

from model.users import ModelsUser

from wraps import required_params


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

    def get(self):
        """
        Retorna uma lista com todos os usuários cadastrados
        """

        return {"data": [user.list_users() for user in ModelsUser.query.all()]}, 200

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
