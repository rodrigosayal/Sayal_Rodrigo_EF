from datetime import datetime
from gestor_turnos import GestorTurnos


def main():

    gestor = GestorTurnos()

    while True:
        print("\n==============================")
        print("   SISTEMA DE TURNOS")
        print("       PELUQUERÍA GUNS AND ROSES")
        print("==============================")
        print("1) Registrar cliente")
        print("2) Pedir turno")
        print("3) Listado de  clientes")
        print("4) Listado de turnos")
        print("5) Cancelar turno (por DNI)")
        print("6) Salir")
        print("==============================")

        opcion = input("Elegí una opción: ")

        
        # 1) REGISTRAR CLIENTE
        
        if opcion == "1":

            dni = input("DNI del cliente: ")
            nombre = input("Nombre completo: ")
            telefono = input("Teléfono: ")
            email = input("Email (opcional): ")

            mensaje = gestor.registrar_cliente(dni, nombre, telefono, email)
            print("\n" + mensaje + "\n")

        
        # 2) PEDIR TURNO
        
        elif opcion == "2":

            dni = input("DNI del cliente: ")

            if dni not in gestor.clientes:
                print("\nEse DNI no está registrado.\n")
                continue

            dia = input("Día del turno (DD/MM/AAAA): ")
            hora = input("Hora del turno (HH:MM): ")

            if "/" not in dia or ":" not in hora:
                print("\nFormato incorrecto.\n")
                continue

            partes = dia.split("/")
            fecha_formato = f"{partes[2]}-{partes[1]}-{partes[0]} {hora}"

            try:
                fecha = datetime.fromisoformat(fecha_formato.replace(" ", "T"))
            except:
                print("\nFecha inválida.\n")
                continue

            duracion = input("Duración (sugerencia 60 minutos maximo): ")

            if not duracion.isdigit():
                print("\nLa duración debe ser un número.\n")
                continue

            duracion = int(duracion)

            servicio = input("Servicio (corte, color, etc.): ")

            resultado = gestor.pedir_turno(dni, fecha, duracion, servicio)

            if isinstance(resultado, str):
                print("\n" + resultado + "\n")
            else:
                print(f"\nTurno creado. ID interno: {resultado.turno_id}\n")

        
        # 3) LISTAR CLIENTES
        
        elif opcion == "3":

            lista = gestor.listar_clientes()

            if not lista:
                print("\nNo hay clientes cargados.\n")
            else:
                print("\n=== CLIENTES REGISTRADOS ===")
                for cli in lista:
                    print(f"DNI: {cli.dni} | Nombre: {cli.nombre} | Tel: {cli.telefono}")

        
        # 4) LISTAR TURNOS
        
        elif opcion == "4":

            lista = gestor.listar_turnos()

            if not lista:
                print("\nNo hay turnos cargados.\n")
            else:
                print("\n=== TURNOS CARGADOS ===")
                for t in lista:
                    estado = "(cancelado)" if t.estado != "activo" else ""
                    print(f"ID: {t.turno_id} | DNI: {t.dni} | Fecha: {t.fecha_hora} | {t.servicio} {estado}")

        
        # 5) CANCELAR TURNO (USANDO DNI)
        
        elif opcion == "5":

            dni = input("DNI del cliente: ")
            mensaje = gestor.cancelar_turno(dni)
            print("\n" + mensaje + "\n")

        
        # 6) SALIR
        
        elif opcion == "6":
            print("\nSaliendo del sistema...\n")
            break

        else:
            print("\nOpción inválida.\n")


if __name__ == "__main__":
    main()
