from flask_login import UserMixin

class usuario(UserMixin):

    def __init__(self, id_usuario, nombre_usuario) -> None:
        self.id = id_usuario
        self.nombre_usuario = nombre_usuario