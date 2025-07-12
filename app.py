from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import threading
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  # Necesaria para usar sesiones
app.permanent_session_lifetime = timedelta(days=7)  # o más si deseas


DATA_FILE = 'datos.json'
datos_lock = threading.Lock()
datos_cache = None

def cargar_datos():
    global datos_cache
    if datos_cache is None:
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump({"ventas": [], "compras": []}, f)
        with open(DATA_FILE, 'r') as f:
            datos_cache = json.load(f)
    return datos_cache

def guardar_datos(data):
    global datos_cache
    with datos_lock:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        datos_cache = data

@app.before_request
def requerir_login():
    session.permanent = True  # Mantiene la sesión activa según timedelta
    rutas_libres = ['iniciar', 'static']  # Páginas que no requieren login
    if 'usuario' not in session and request.endpoint not in rutas_libres:
        return redirect(url_for('iniciar'))

@app.route('/')
def principal():
    return render_template('principal.html')

# ---------- INICIO Y CIERRE DE SESIÓN ----------
@app.route('/iniciar', methods=['GET', 'POST'])
def iniciar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            session['usuario'] = nombre
            return redirect(url_for('principal'))
    return render_template('iniciar.html')

@app.route('/cerrar')
def cerrar():
    session.clear()
    return redirect(url_for('iniciar'))

@app.route('/ventas')
def ventas():
    data = cargar_datos()
    return render_template('ventas.html', ventas=data["ventas"])

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

        data = cargar_datos()
        data["ventas"].append(nueva_venta)
        guardar_datos(data)
        return redirect(url_for('ventas'))

    return render_template('venta.html')

@app.route('/eliminar_venta/<int:index>', methods=['POST'])
def eliminar_venta(index):
    if 'usuario' not in session:
        return redirect(url_for('iniciar'))

    data = cargar_datos()
    if 0 <= index < len(data["ventas"]):
        if data["ventas"][index]["vendedor"] == session['usuario']:
            del data["ventas"][index]
            guardar_datos(data)
    return redirect(url_for('ventas'))

# ---------- COMPRAS ----------
@app.route('/compras')
def compras():
    data = cargar_datos()
    return render_template('compras.html', compras=data["compras"])

@app.route('/compra', methods=['GET', 'POST'])
def compra():
    if 'usuario' not in session:
        return redirect(url_for('iniciar'))

    if request.method == 'POST':
        producto = request.form.get('producto', '').strip()
        calidad = request.form.get('calidad', '').strip()
        cantidad = request.form.get('cantidad', '').strip()
        contacto = request.form.get('contacto', '').strip()

        if not producto or not calidad or not cantidad or not contacto:
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
            "cantidad": cantidad,
            "contacto": contacto
        }

        data = cargar_datos()
        data["compras"].append(nueva_compra)
        guardar_datos(data)
        return redirect(url_for('compras'))
    return render_template('compra.html')

@app.route('/eliminar_compra/<int:index>', methods=['POST'])
def eliminar_compra(index):
    if 'usuario' not in session:
        return redirect(url_for('iniciar'))

    data = cargar_datos()
    if 0 <= index < len(data["compras"]):
        if data["compras"][index]["comprador"] == session['usuario']:
            del data["compras"][index]
            guardar_datos(data)
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
