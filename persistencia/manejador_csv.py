import csv
from datetime import datetime
from modelos.cliente import Cliente
from modelos.turno import Turno


class ManejadorCSV:

    # -----------------------------------------
    # GUARDAR CLIENTES
    # -----------------------------------------
    @staticmethod
    def guardar_clientes(ruta, dicc_clientes):
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            columnas = ["dni", "nombre", "telefono", "email"]
            writer = csv.DictWriter(f, fieldnames=columnas)
            writer.writeheader()

            for cli in dicc_clientes.values():
                writer.writerow(cli.a_dict())

    # -----------------------------------------
    # GUARDAR TURNOS
    # -----------------------------------------
    @staticmethod
    def guardar_turnos(ruta, dicc_turnos):
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            columnas = ["turno_id", "dni", "fecha_hora", "duracion", "servicio", "estado"]
            writer = csv.DictWriter(f, fieldnames=columnas)
            writer.writeheader()

            for tur in dicc_turnos.values():
                writer.writerow(tur.a_dict())

    # -----------------------------------------
    # CARGAR CLIENTES
    # -----------------------------------------
    @staticmethod
    def cargar_clientes(ruta):
        clientes = {}
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    cli = Cliente(
                        fila["dni"],
                        fila["nombre"],
                        fila["telefono"],
                        fila["email"]
                    )
                    clientes[fila["dni"]] = cli
        except FileNotFoundError:
            pass

        return clientes

    # -----------------------------------------
    # CARGAR TURNOS
    # -----------------------------------------
    @staticmethod
    def cargar_turnos(ruta):
        turnos = {}
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    tur = Turno(
                        fila["turno_id"],
                        fila["dni"],
                        datetime.fromisoformat(fila["fecha_hora"]),
                        int(fila["duracion"]),
                        fila["servicio"],
                        fila["estado"]
                    )
                    turnos[fila["turno_id"]] = tur
        except FileNotFoundError:
            pass

        return turnos
