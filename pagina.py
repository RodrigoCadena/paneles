from flask import Flask, request, render_template_string # Importar Flask para crear la aplicación web,  y request para manejar solicitudes HTTP y render_template_string para renderizar plantillas
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
        <h1>Escriba un valor de irradiancia entre 500 y 1000 en centenas</h1>
        <form action="/buscar" method="post">
            <label for="tipo1">Buscar por:</label>
            <select name="tipo1" id="tipo1">
                <option value="radiation">Número</option> 
            </select>
            <label for="valor1">Valor:</label>
            <input type="text" name="valor1" id="valor1" required>
            <button type="submit">Buscar</button>
        </form>
        <h2>Escriba un valor de temperatura entre 278 y 309 grados Kelvin</h2>
        <form action="/buscar" method="post">
            <label for="tipo2">Buscar por:</label>
            <select name="tipo2" id="tipo2">
                <option value="temperature">Número</option> 
            </select>
            <label for="valor2">Valor:</label>
            <input type="text" name="valor2" id="valor2" required>
            <button type="submit">Buscar</button>
        </form>
    ''')

# Ruta para realizar la búsqueda
@app.route('/buscar', methods=['POST'])
def buscar():
   
    tipo1 = request.form['tipo1']
    valor1 = request.form['valor1']
    tipo2 = request.form['tipo2']
    valor2 = request.form['valor2']
    conn = get_db_connection()
    registro1 = None
    registro2 = None

    if tipo1 == 'radiation' and tipo2 == 'radiation': # Buscar por número
        registro = conn.execute('SELECT * FROM pv_results WHERE radiation = ?', (valor1,)).fetchone()
        registro = conn.execute('SELECT * FROM pv_results WHERE temperature = ?', (valor2,)).fetchone()
    conn.close()
    
    if registro:
      
        return render_template_string('''
            <p>Potencia Máxima: {{ registro['max_power'] }}</p>
            <a href="/">Volver</a>
        ''', registro=registro)
    else:
        return 'Registre un valor de irradiancia y temperatura apropiados. <a href="/">Volver</a>'

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)