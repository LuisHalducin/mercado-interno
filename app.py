import os
from dotenv import load_dotenv
import sys

load_dotenv()

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  
    print("Conexión a MongoDB exitosa")
except Exception as e:
    print("Error al conectar a MongoDB:", e)
    sys.exit("No se pudo conectar a la base de datos. Abortando la aplicación.")

db = client['mi_base_de_datos'] 


ventas_collection = db['ventas']
compras_collection = db['compras']
usuarios_collection = db['usuarios']
articulos_collection = db['articulos']


from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import threading
from datetime import timedelta
from bson import ObjectId
from flask_wtf import CSRFProtect
from datetime import datetime
import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(days=7) 


@app.before_request
def requerir_login():
    session.permanent = True  
    rutas_libres = ['iniciar', 'static', 'registro', 'crear_articulo']  
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
    # Traer todos los artículos ordenados del más reciente al más antiguo
    articulos = list(articulos_collection.find().sort("fecha", -1))
    if articulos:
        articulo_principal = articulos[0]
        articulos_anteriores = articulos[1:]
    else:
        articulo_principal = None
        articulos_anteriores = []

    return render_template('blog.html', 
                           articulo_principal=articulo_principal, 
                           articulos_anteriores=articulos_anteriores)

@app.route('/blog/<articulo_id>')
def ver_articulo(articulo_id):
    articulo = articulos_collection.find_one({"_id": ObjectId(articulo_id)})
    if not articulo:
        flash("Artículo no encontrado.")
        return redirect(url_for('blog'))

    return render_template('ver_articulo.html', articulo=articulo)


def es_admin():
    if 'usuario' not in session:
        return False
    usuario = usuarios_collection.find_one({"nombre": session['usuario']})
    return usuario and usuario.get('rol') == 'admin'

@app.context_processor
def utility_processor():
    return dict(es_admin=es_admin)


@app.route('/blog/crear', methods=['GET', 'POST'])
def crear_articulo():
    if not es_admin():
        flash("No tienes permiso para esta acción.")
        return redirect(url_for('blog'))

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        contenido = request.form.get('contenido', '').strip()
        imagen = request.files.get('imagen')  # 📸 obtener imagen
        print("Imagen recibida:", imagen)

        if not titulo or not contenido:
            flash("Todos los campos son obligatorios.")
            return render_template('crear_articulo.html')
        
        url_imagen = None
        public_id_imagen = None

        if imagen and imagen.filename != '':
            try:
                print("Subiendo imagen a Cloudinary...")
                resultado = cloudinary.uploader.upload(imagen)
                print("Resultado de Cloudinary:", resultado)
                url_imagen = resultado.get("secure_url")
                public_id_imagen = resultado.get("public_id")
            except Exception as e:
                flash("Error al subir imagen: " + str(e))
                return render_template('crear_articulo.html')

        nuevo_articulo = {
            "titulo": titulo,
            "contenido": contenido,
            "autor": session['usuario'],
            "fecha": datetime.utcnow(),
            "imagen": url_imagen,
            "imagen_public_id": public_id_imagen
        }
        articulos_collection.insert_one(nuevo_articulo)
        flash("Artículo creado con éxito.")
        return redirect(url_for('blog'))

    return render_template('crear_articulo.html')

@app.route('/blog/eliminar/<articulo_id>', methods=['POST'])
def eliminar_articulo(articulo_id):
    if not es_admin():
        flash("No tienes permiso para esta acción.")
        return redirect(url_for('blog'))

    articulo = articulos_collection.find_one({"_id": ObjectId(articulo_id)})

    if articulo:
        public_id = articulo.get("imagen_public_id")
        if public_id:
            try:
                cloudinary.uploader.destroy(public_id)
                print(f"Imagen con public_id {public_id} eliminada de Cloudinary.")
            except Exception as e:
                flash(f"Error al eliminar la imagen en Cloudinary: {e}")

        articulos_collection.delete_one({"_id": ObjectId(articulo_id)})
        flash("Artículo eliminado con éxito.")
    else:
        flash("Artículo no encontrado.")

    return redirect(url_for('blog'))


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
