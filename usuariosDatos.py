from conexion import DB
from models.usuario import usuario
from conexion import DB

def get_by_id(id):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select id,nombre,correo from usuarios where id = '{id}'")
        resultadoConsultaUsuarios = cursor.fetchall()
        
        if resultadoConsultaUsuarios:
            for rcu in resultadoConsultaUsuarios:
                user = usuario(rcu[0],rcu[1],rcu[2])
                return user

        else:
            return False
             


def loggin_user(nombreUsuario,correoUsuario):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select id from usuarios where correo = '{correoUsuario}'")
        resultadoConsultaUsuarios = cursor.fetchall()
        
        if resultadoConsultaUsuarios:
            for rcu in resultadoConsultaUsuarios:
                user = usuario(rcu[0],nombreUsuario,correoUsuario)
                return user
        else:
            return False