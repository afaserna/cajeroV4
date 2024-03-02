import pyodbc

import sys
from tabulate import tabulate
consi = None

def crear_bd():
    conn_str = 'Driver={SQL Server};' \
               'Server=LAPTOP-Q2N4V5J3\SQLEXPRESS;' \
               'Database=master;' \
               'Trusted_Connection=yes;'
    #inicialmente se conectara a master
    # master es una bd de sistema predeterminada en SQL server.
    print("Creando la base de datos...")
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE clientesBco;")
    cursor.close()
    conn.close()
    
    #establece conexion con una bd diferente a master
    return pyodbc.connect(conn_str.replace("master", "clientesBco"), autocommit=True)

def crear_tabla(conn):
    
    print("Creando la tabla Usuario...")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE Usuario (
            cedula_user INT PRIMARY KEY,
            name_user VARCHAR(50),
            email_user VARCHAR(50),
            clave_user INT,
            rep_claveUser INT
        )
    """)
    cursor.close()

def registro(conn):
    ide = int(input("Ingrese su identificación: "))
    usu = input("Ingrese su usuario: ")
    corre = input("Ingrese su correo: ")
    clav = int(input("Ingrese su clave: "))
    rep_clav = int(input("Ingrese su clave nuevamente: "))
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuario (cedula_user, name_user, email_user, clave_user, rep_claveUser) VALUES (? ,?, ?, ?, ?)", (ide, usu, corre, clav, rep_clav))
    cursor.close()

def ingreso_user(conn):
    usuario = input("Ingrese su usuario: ")
    clave = int(input("Ingrese su clave: "))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE name_user = ? AND clave_user = ?", (usuario, clave))
    if cursor.fetchone():
        print("Usuario autenticado correctamente")
       
         # Autenticación correcta
    else:
        print("Usuario o clave incorrectos")
        
          # Autenticación fallida
    
    cursor.close()
    

def menu():
    conn = crear_bd()
    crear_tabla(conn)
   
    while True:
        print("**************************Menu************************************")
        print("Presione 1 para registro:")
        print("Presione 2 para ingresar:")
        print("Presione 3 para consultas y movimientos:")
        print("Presione 4 para salir del menú:")
        print("Presione 5 para destruir la BD ")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registro(conn)
        elif opcion == "2":
            ingreso_user(conn)
        elif opcion == "3":
            print ("Ingreso a consultas y movimientos")
            print ("presione 6 para consultar movimientos")
            print ("presione 7 para consignar")
            print ("presione 8 para retirar")
            
            opcion1= int(input("seleccione una opcion: "))
            
            if (opcion1 == 6):
                crearTabla_consultMov(conn)
                intoConsult_mov(conn)
                mostrar_consultMov (conn)
            elif (opcion1==7):
                consignar(conn)
            elif (opcion1==8):
                retirar(conn)
                
            else: print("Debes ingresar con una clave válida")
            
        elif opcion == "4":
            salir(conn)
            return
        elif opcion == "5":
            DestruirBd(conn)
        else:
            print("Opción inválida")
            
            
def crearTabla_consultMov(conn):
    
         print("Creando la tabla consultas y movimientos...")
         cursor = conn.cursor()
         cursor.execute("""
         CREATE TABLE consult_movimiento (
            Id_conMov INT PRIMARY KEY,
            cedula_user1 int,
            retiro float,
            consignar float,
            consult_mov varchar(100),
            consult_saldo float,
            constraint apodo foreign key (cedula_user1) references Usuario (cedula_user)
             )
         """)
         cursor.close()
         
def mostrar_consultMov (conn):
    cursor = conn.cursor()
    cursor.execute("select *from consult_movimiento")
    for row in cursor:
       print(row)
         
def intoConsult_mov(conn):
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO consult_movimiento (Id_conMov, cedula_user1, retiro, consignar, consult_mov, consult_saldo ) values(?,?,?,?,?,?)", (1, 71379025, 0, 0, 'consulta', 0))
    cursor.close()
          
def consignar(conn):
    cursor = conn.cursor()
    global consi
    consi = int (input("Ingrese valor a consignar"))
    cursor.execute("INSERT INTO consult_movimiento (Id_conMov, cedula_user1, retiro, consignar, consult_mov, consult_saldo ) values(?,?,?,?,?,?)", (2, 71379025, 0, consi, 'consulta', 0))
    print("te han consignado: ", consi)
    
    cursor.close()
    

def retirar(conn):
    global consi
    print("ingrese valor a retirar")
    reti = int (input("solo valores >=10.000: "))
    if reti <= 50000:
        te_quedan = consi - reti 
        print("retiraste: " , reti)
        print("tu nuevo saldo es: ", te_quedan)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO consult_movimiento (Id_conMov, cedula_user1, retiro, consignar, consult_mov, consult_saldo ) values(?,?,?,?,?,?)", (3, 71379025, reti, 0, 'consulta', 0))
        cursor.close()
     

def salir(conn):
    print("Cerrando la aplicación...")
    conn.close()
    
def DestruirBd(conn):
    conexiones_activas = pyodbc.pooling.activeconnections()
   # Cerrar todas las conexiones activas
    for conn in conexiones_activas:
        conn.close()
    print("Todas las conexiones activas han sido cerradas")  # Verifica el resultado
    cursor = conn.cursor()
    cursor.execute("drop database clientesBco;")
    cursor.close()
    

if __name__ == "__main__":
    menu()