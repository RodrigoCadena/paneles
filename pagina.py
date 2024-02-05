from flask import Flask, request, render_template, render_template_string # Importar Flask para crear la aplicación web,  y request para manejar solicitudes HTTP y render_template_string para renderizar plantillas
import os
import sqlite3

app = Flask(__name__) # Crear una aplicación de Flask

# Función para conectarse a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('pv_results.db')
    conn.row_factory = sqlite3.Row # Para poder acceder a las columnas por nombre en lugar de índice
    return conn

# Ruta para la página de inicio
@app.route('/') # Decorador para indicar la ruta de la página
def index():
    """
    Página para calcular la potencia máxima de los paneles dadas una temperatura y una irradiancia.
    """
    return render_template_string('''
        <img src='https://media.istockphoto.com/id/1473638950/es/foto/t%C3%A9cnicos-que-llevan-m%C3%B3dulo-solar-fotovoltaico-mientras-instalan-el-sistema-de-paneles-solares.webp?b=1&s=612x612&w=0&k=20&c=uFpr23Bz5hVWYIoNKkCRod6NwJEhqg9Wcaxy7U7SBQI='/>
        <form action="/buscar" method="post">
            <h1>Escriba un valor de irradiancia entre 500 y 1000 en centenas</h1>
                <label for="valor1">Valor:</label>
                <input type="text" name="valor1" id="valor1" required>
            <h2>Escriba un valor de temperatura entre 278 y 309 grados Kelvin</h2>
                <label for="valor2">Valor:</label>
                <input type="text" name="valor2" id="valor2" required>
            <button type="submit">Buscar</button>
        </form>
    ''')

# Ruta para realizar la búsqueda
@app.route('/buscar', methods=['POST'])
def buscar():
   
    valor1 = request.form['valor1']
    valor2 = request.form['valor2']
    conn = get_db_connection()
    registro = None
    
    registro = conn.execute('SELECT * FROM max_power_results WHERE radiation = ? and temperature = ?',(valor1,valor2)).fetchone()
    conn.close()
    
    if registro:
      
        return render_template_string('''
            <img src='https://media.istockphoto.com/id/1473638950/es/foto/t%C3%A9cnicos-que-llevan-m%C3%B3dulo-solar-fotovoltaico-mientras-instalan-el-sistema-de-paneles-solares.webp?b=1&s=612x612&w=0&k=20&c=uFpr23Bz5hVWYIoNKkCRod6NwJEhqg9Wcaxy7U7SBQI='/>
            <p>Irradiancia: {{ registro['radiation'] }}</p>
            <p>Temperatura: {{ registro['temperature'] }}</p>
            <p>Potencia Máxima: {{ registro['max_power'] }}</p>
            <a href="/">Volver</a>
        ''', registro=registro)
    else:
        return 'Registre un valor de irradiancia y temperatura apropiados. <a href="/">Volver</a>'

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)