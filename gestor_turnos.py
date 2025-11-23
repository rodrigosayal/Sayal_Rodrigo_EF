from datetime import timedelta
from modelos.cliente import Cliente
from modelos.turno import Turno
from persistencia.manejador_csv import ManejadorCSV


class GestorTurnos:

    def __init__(self):
                                                                                    # Diccionarios donde se guardan los datos
        self.clientes = ManejadorCSV.cargar_clientes("data/clientes.csv")
        self.turnos = ManejadorCSV.cargar_turnos("data/turnos.csv")

    
    # VALIDAR DNI
   
    def validar_dni(self, dni):
        if not dni.isdigit():
            return False
        if len(dni) < 7 or len(dni) > 8:
            return False
        return True

    
    # REGISTRAR CLIENTE
    
    def registrar_cliente(self, dni, nombre, telefono, email=""):

        if not self.validar_dni(dni):
            return "DNI inválido."

        if dni in self.clientes:
            return "Ese DNI ya está registrado."

        datos = {
            "dni": dni,
            "nombre": nombre,
            "telefono": telefono,
            "email": email
        }

        nuevo_cliente = Cliente(**datos)
        self.clientes[dni] = nuevo_cliente

        ManejadorCSV.guardar_clientes("data/clientes.csv", self.clientes)

        return "Cliente registrado."

    
    # REVISAR SI UN TURNO SE PISA CON OTRO
    
    def hay_superposicion(self, fecha_hora_nueva, duracion_nueva):

        inicio_nuevo = fecha_hora_nueva
        fin_nuevo = fecha_hora_nueva + timedelta(minutes=duracion_nueva)

        for turno in self.turnos.values():

            if turno.estado != "activo":
                continue                                                                # los turnos cancelados no molestan

            inicio_existente = turno.fecha_hora
            fin_existente = turno.fecha_hora + timedelta(minutes=turno.duracion)

                                                                                        # Si se pisa el horario
            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                return True

        return False

    
    # PEDIR TURNO
    
    def pedir_turno(self, dni, fecha_hora, duracion, servicio):

        if dni not in self.clientes:
            return "Ese DNI no está registrado."

                                                                            # Control de superposición de horarios
        if self.hay_superposicion(fecha_hora, duracion):
            return "Ese horario ya está ocupado. Elegí otro."

        nuevo_id = str(len(self.turnos) + 1)

        datos = {
            "turno_id": nuevo_id,
            "dni": dni,
            "fecha_hora": fecha_hora,
            "duracion": duracion,
            "servicio": servicio,
            "estado": "activo"
        }

        nuevo_turno = Turno(**datos)

        self.turnos[nuevo_id] = nuevo_turno

        ManejadorCSV.guardar_turnos("data/turnos.csv", self.turnos)

        return nuevo_turno

    
    # LISTAR CLIENTES
    
    def listar_clientes(self):
        return list(self.clientes.values())

    
    # LISTAR TURNOS
    
    def listar_turnos(self):
        return list(self.turnos.values())

    
    # CANCELAR TURNO POR DNI
    
    def cancelar_turno(self, dni):

        if dni not in self.clientes:
            return "Ese DNI no existe."

        turnos_cliente = [t for t in self.turnos.values() if t.dni == dni and t.estado == "activo"]

        if not turnos_cliente:
            return "Ese cliente no tiene turnos activos."

                                                            # Si el cliente tiene solo un turno, lo cancela de una
        if len(turnos_cliente) == 1:
            turnos_cliente[0].estado = "cancelado"
            ManejadorCSV.guardar_turnos("data/turnos.csv", self.turnos)
            return "Turno cancelado."

                                                            # Si tiene más de uno, mostramos lista
        print("\nTurnos activos del cliente:")
        for i, t in enumerate(turnos_cliente, start=1):
            print(f"{i}) {t.fecha_hora} - {t.servicio}")

        eleccion = input("Elegí cuál cancelar: ")

        if not eleccion.isdigit():
            return "Opción inválida."

        eleccion = int(eleccion)

        if eleccion < 1 or eleccion > len(turnos_cliente):
            return "Opción inválida."

        turno_elegido = turnos_cliente[eleccion - 1]
        turno_elegido.estado = "cancelado"

        ManejadorCSV.guardar_turnos("data/turnos.csv", self.turnos)

        return "Turno cancelado."
