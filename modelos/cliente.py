class Cliente:
    def __init__(self, dni, nombre, telefono, email=""):
        self.dni = dni
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def a_dict(self):
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email
        }
