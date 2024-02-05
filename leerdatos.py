import sqlite3 #Importa la libreria para manejar la base

def leer_datos(): #Define la funcion leer_datos
  conn = sqlite3.connect("pv_results.db") #Establecer conexion con la base
  cursor = conn.cursor() #Permitir realizar consultas a la base

  # Obtener y mostrar los datos
  rows = cursor.fetchall()
  for row in rows:
    print(row)  # Aquí puedes ajustar la forma en que se muestran los datos

  # Cerrar la conexión a la base de datos
  conn.close()

if __name__ == '__main__':
    leer_datos()