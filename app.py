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
        contacto = request.form.get('contacto', '').strip()

        if not producto or not calidad or not cantidad or not precio or not contacto:
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
            "precio": precio,
            "contacto": contacto
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
