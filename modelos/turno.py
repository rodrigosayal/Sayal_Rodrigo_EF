class Turno:
    def __init__(self, turno_id, dni, fecha_hora, duracion, servicio, estado="activo"):
        self.turno_id = turno_id
        self.dni = dni
        self.fecha_hora = fecha_hora
        self.duracion = duracion
        self.servicio = servicio
        self.estado = estado

    def a_dict(self):
        return {
            "turno_id": self.turno_id,
            "dni": self.dni,
            "fecha_hora": self.fecha_hora.isoformat(),
            "duracion": self.duracion,
            "servicio": self.servicio,
            "estado": self.estado
        }
