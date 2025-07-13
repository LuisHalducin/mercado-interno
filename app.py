import os
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['mi_base_de_datos']  # Puedes llamarla como quieras

# Ejemplo: colección de ventas
ventas_collection = db['ventas']
compras_collection = db['compras']
usuarios_collection = db['usuarios']

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import threading
from datetime import timedelta
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  # Necesaria para usar sesiones
app.permanent_session_lifetime = timedelta(days=7)  # o más si deseas


@app.before_request
def requerir_login():
    session.permanent = True  # Mantiene la sesión activa según timedelta
    rutas_libres = ['iniciar', 'static']  # Páginas que no requieren login
    if 'usuario' not in session and request.endpoint not in rutas_libres:
        return redirect(url_for('iniciar'))

@app.route('/')
def principal():
    return render_template('principal.html')

@app.route('/iniciar', methods=['GET', 'POST'])
def iniciar():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        contraseña = request.form.get('contraseña', '').strip()

        if not nombre or not contraseña:
            flash("Todos los campos son obligatorios.")
            return render_template('iniciar.html')

        usuario = usuarios_collection.find_one({"nombre": nombre})
        if usuario and check_password_hash(usuario['contraseña'], contraseña):
            session['usuario'] = nombre
            return redirect(url_for('principal'))
        else:
            flash("Nombre o contraseña incorrectos.")
            return render_template('iniciar.html')

    return render_template('iniciar.html')

@app.route('/cerrar')
def cerrar():
    session.clear()
    return redirect(url_for('iniciar'))


# ---------- REGISTRO ----------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        contraseña = request.form.get('contraseña', '').strip()
        contraseña2 = request.form.get('contraseña2', '').strip()

        if not nombre or not contraseña or not contraseña2:
            flash("Todos los campos son obligatorios.")
            return render_template('registro.html')

        if contraseña != contraseña2:
            flash("Las contraseñas no coinciden.")
            return render_template('registro.html')

        # Verifica si ya existe un usuario con ese nombre
        if db.usuarios.find_one({"nombre": nombre}):
            flash("El nombre ya está en uso. Intenta otro.")
            return render_template('registro.html')

        # Encripta la contraseña y guarda el nuevo usuario
        contraseña_hash = generate_password_hash(contraseña)
        db.usuarios.insert_one({
            "nombre": nombre,
            "contraseña": contraseña_hash
        })

        flash("Cuenta creada con éxito. Ahora inicia sesión.")
        return redirect(url_for('iniciar'))

    return render_template('registro.html')


@app.route('/ventas')
def ventas():
    ventas = list(ventas_collection.find())  # obtiene las ventas desde MongoDB
    return render_template('ventas.html', ventas=ventas)

@app.route('/venta', methods=['GET', 'POST'])
def venta():
    if 'usuario' not in session:
        return redirect(url_for('iniciar'))

    if request.method == 'POST':
        producto = request.form.get('producto', '').strip()
        calidad = request.form.get('calidad', '').strip()
        cantidad = request.form.get('cantidad', '').strip()
        precio = request.form.get('precio', '').strip()

        if not producto or not calidad or not cantidad or not precio:
            flash("Todos los campos son obligatorios.")
            return render_template('venta.html')

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            flash("La cantidad y el precio deben ser valores numéricos.")
            return render_template('venta.html')

        nueva_venta = {
            "vendedor": session['usuario'],
            "producto": producto,
            "calidad": calidad,
            "cantidad": cantidad,
            "precio": precio
        }

        ventas_collection.insert_one(nueva_venta)  # guarda en MongoDB
        return redirect(url_for('ventas'))

    return render_template('venta.html')


@app.route('/eliminar_venta/<id>', methods=['POST'])
def eliminar_venta(id):
    if 'usuario' not in session:
        return redirect(url_for('iniciar'))

    venta = ventas_collection.find_one({"_id": ObjectId(id)})
    if venta and venta['vendedor'] == session['usuario']:
        ventas_collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('ventas'))

@app.route('/compras')
def compras():
    compras = list(compras_collection.find())
    return render_template('compras.html', compras=compras)

@app.route('/compra', methods=['GET', 'POST'])
def compra():
    if 'usuario' not in session:
        return redirect(url_for('iniciar'))

    if request.method == 'POST':
        producto = request.form.get('producto', '').strip()
        calidad = request.form.get('calidad', '').strip()
        cantidad = request.form.get('cantidad', '').strip()

        if not producto or not calidad or not cantidad:
            flash("Todos los campos son obligatorios.")
            return render_template('compra.html')

        try:
            cantidad = int(cantidad)
        except ValueError:
            flash("La cantidad debe ser un número entero.")
            return render_template('compra.html')

        nueva_compra = {
            "comprador": session['usuario'],
            "producto": producto,
            "calidad": calidad,
            "cantidad": cantidad
        }

        compras_collection.insert_one(nueva_compra)
        return redirect(url_for('compras'))

    return render_template('compra.html')

@app.route('/eliminar_compra/<compra_id>', methods=['POST'])
def eliminar_compra(compra_id):
    if 'usuario' not in session:
        return redirect(url_for('iniciar'))

    compra = compras_collection.find_one({"_id": ObjectId(compra_id)})
    if compra and compra['comprador'] == session['usuario']:
        compras_collection.delete_one({"_id": ObjectId(compra_id)})

    return redirect(url_for('compras'))


@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/herramientas')
def herramientas():
    return render_template('herramientas.html')

@app.route('/gobierno')
def gobierno():
    return render_template('gobierno.html')

@app.route('/proximamente')
def proximamente():
    return render_template('proximamente.html')

@app.route('/redirigir_discord')
def redirigir_discord():
    url_web = request.args.get('url')
    if not url_web:
        return "URL no proporcionada", 400

    # Convierte el enlace a intento de abrir la app de Discord
    url_app = url_web.replace("https://", "discord://")

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Redirigiendo a Discord...</title>
      <style>
        body {{
          background-color: #1e1e2f;
          color: #f0f0f0;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
          text-align: center;
        }}
        h1 {{
          font-size: 2em;
          margin-bottom: 20px;
          color: #00bcd4;
        }}
        p {{
          font-size: 1.1em;
        }}
        a {{
          color: #00bcd4;
          text-decoration: none;
          margin-top: 10px;
          padding: 10px 20px;
          background-color: #2c3e50;
          border-radius: 8px;
          display: inline-block;
          transition: background 0.3s ease;
        }}
        a:hover {{
          background-color: #34495e;
        }}
      </style>
      <script>
        function openDiscord() {{
          window.location = "{url_app}";
          setTimeout(function() {{
            window.location = "{url_web}";
          }}, 2000);
        }}
        window.onload = openDiscord;
      </script>
    </head>
    <body>
      <h1>Redirigiendo a Discord...</h1>
      <p>Intentando abrir la aplicación. Si no funciona, haz clic abajo:</p>
      <a href="{url_web}">Ir al canal en Discord</a>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
