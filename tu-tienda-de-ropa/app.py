"""Tu Tienda de Ropa - versión Flask con carrito en sesión y pedidos en SQLite."""
import os
import secrets
import sqlite3
from datetime import datetime

from flask import (Flask, abort, flash, g, redirect, render_template,
                   request, send_from_directory, session, url_for)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "tienda.db"))

app = Flask(__name__)
# En producción definí SECRET_KEY como variable de entorno (ver .env.example)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-cambiar-en-produccion")

PRODUCTOS_INICIALES = [
    ("Campera", 1000, "Abrigo.jpg", 10),
    ("Buzo", 100, "Buzo.jpg", 10),
    ("Camisa", 50, "Camisa.jpg", 10),
    ("Conjunto Hombre", 2000, "ConjunHombre.jpg", 10),
    ("Conjunto", 100, "Conjunto.jpg", 10),
    ("Jeans", 1500, "Jean.jpg", 10),
    ("Remera", 15, "Remera.jpg", 10),
    ("Zapatilla", 1200, "Zapatilla.jpg", 10),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL CHECK (precio >= 0),
    imagen TEXT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT NOT NULL,
    total REAL NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente'
);
CREATE TABLE IF NOT EXISTS pedido_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
    producto_id INTEGER NOT NULL REFERENCES productos(id),
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL NOT NULL
);
"""


# ---------- Base de datos ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    if db.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO productos (nombre, precio, imagen, stock) VALUES (?, ?, ?, ?)",
            PRODUCTOS_INICIALES,
        )
    db.commit()


@app.cli.command("init-db")
def init_db_command():
    """Crea las tablas y carga los productos de ejemplo: flask init-db"""
    init_db()
    print("Base de datos lista.")


# ---------- CSRF simple (formularios POST) ----------
def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def verificar_csrf():
    if request.method == "POST":
        token = session.get("csrf")
        if not token or not secrets.compare_digest(token, request.form.get("csrf", "")):
            abort(400, "Token CSRF inválido")


# ---------- Carrito (guardado en la sesión: {id_producto: cantidad}) ----------
def get_carrito():
    return session.get("carrito", {})


def detalle_carrito():
    """Devuelve (items, total) leyendo precios actuales de la base."""
    carrito = get_carrito()
    if not carrito:
        return [], 0.0
    db = get_db()
    ids = [int(i) for i in carrito]
    marcas = ",".join("?" * len(ids))
    filas = db.execute(f"SELECT * FROM productos WHERE id IN ({marcas})", ids).fetchall()
    items, total = [], 0.0
    for fila in filas:
        cantidad = carrito[str(fila["id"])]
        subtotal = fila["precio"] * cantidad
        total += subtotal
        items.append({"producto": fila, "cantidad": cantidad, "subtotal": subtotal})
    return items, total


@app.context_processor
def inyectar_cantidad_carrito():
    return {"cantidad_carrito": sum(get_carrito().values())}


@app.template_filter("peso")
def formato_peso(valor):
    return "$" + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------- Rutas ----------
@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/productos")
def productos():
    lista = get_db().execute("SELECT * FROM productos ORDER BY id").fetchall()
    return render_template("productos.html", productos=lista)


@app.route("/carrito")
def ver_carrito():
    items, total = detalle_carrito()
    return render_template("carrito.html", items=items, total=total)


@app.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
def agregar_al_carrito(producto_id):
    producto = get_db().execute(
        "SELECT * FROM productos WHERE id = ?", (producto_id,)).fetchone()
    if producto is None:
        abort(404)
    carrito = get_carrito()
    clave = str(producto_id)
    nueva = carrito.get(clave, 0) + 1
    if nueva > producto["stock"]:
        flash(f"No hay más stock de {producto['nombre']}.", "error")
    else:
        carrito[clave] = nueva
        session["carrito"] = carrito
        flash(f"{producto['nombre']} agregado al carrito.", "ok")
    return redirect(request.referrer or url_for("productos"))


@app.route("/carrito/actualizar/<int:producto_id>", methods=["POST"])
def actualizar_carrito(producto_id):
    carrito = get_carrito()
    clave = str(producto_id)
    if clave in carrito:
        try:
            cantidad = int(request.form.get("cantidad", 1))
        except ValueError:
            cantidad = 1
        producto = get_db().execute(
            "SELECT stock FROM productos WHERE id = ?", (producto_id,)).fetchone()
        if producto is None or cantidad <= 0:
            carrito.pop(clave)
        else:
            carrito[clave] = min(cantidad, producto["stock"])
        session["carrito"] = carrito
    return redirect(url_for("ver_carrito"))


@app.route("/carrito/quitar/<int:producto_id>", methods=["POST"])
def quitar_del_carrito(producto_id):
    carrito = get_carrito()
    carrito.pop(str(producto_id), None)
    session["carrito"] = carrito
    return redirect(url_for("ver_carrito"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = detalle_carrito()
    if not items:
        flash("Tu carrito está vacío.", "error")
        return redirect(url_for("productos"))

    if request.method == "POST":
        datos = {c: request.form.get(c, "").strip()
                 for c in ("nombre", "email", "telefono", "direccion")}
        errores = []
        if len(datos["nombre"]) < 3:
            errores.append("Ingresá tu nombre completo.")
        if "@" not in datos["email"] or "." not in datos["email"]:
            errores.append("Ingresá un email válido.")
        if len(datos["direccion"]) < 5:
            errores.append("Ingresá una dirección de entrega.")
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("checkout.html", items=items, total=total, datos=datos)

        db = get_db()
        try:
            db.execute("BEGIN")
            # Revalidar stock dentro de la transacción
            for it in items:
                p = db.execute("SELECT stock FROM productos WHERE id = ?",
                               (it["producto"]["id"],)).fetchone()
                if p["stock"] < it["cantidad"]:
                    raise ValueError(f"Sin stock suficiente de {it['producto']['nombre']}.")
            cur = db.execute(
                "INSERT INTO pedidos (fecha, nombre, email, telefono, direccion, total) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now().isoformat(timespec="seconds"), datos["nombre"],
                 datos["email"], datos["telefono"], datos["direccion"], total))
            pedido_id = cur.lastrowid
            for it in items:
                db.execute(
                    "INSERT INTO pedido_items (pedido_id, producto_id, nombre, cantidad, precio_unitario) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (pedido_id, it["producto"]["id"], it["producto"]["nombre"],
                     it["cantidad"], it["producto"]["precio"]))
                db.execute("UPDATE productos SET stock = stock - ? WHERE id = ?",
                           (it["cantidad"], it["producto"]["id"]))
            db.commit()
        except ValueError as exc:
            db.rollback()
            flash(str(exc), "error")
            return redirect(url_for("ver_carrito"))
        except Exception:
            db.rollback()
            raise
        session.pop("carrito", None)
        return redirect(url_for("pedido_ok", pedido_id=pedido_id))

    return render_template("checkout.html", items=items, total=total, datos={})


@app.route("/pedido/<int:pedido_id>")
def pedido_ok(pedido_id):
    db = get_db()
    pedido = db.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()
    if pedido is None:
        abort(404)
    items = db.execute("SELECT * FROM pedido_items WHERE pedido_id = ?", (pedido_id,)).fetchall()
    return render_template("pedido_ok.html", pedido=pedido, items=items)


# Páginas estáticas que ya tenías (Contacto, Locales, Cambios) en la carpeta template/
@app.route("/template/<path:archivo>")
def pagina_estatica(archivo):
    if archivo.lower() == "productos.html":
        return redirect(url_for("productos"))
    return send_from_directory(os.path.join(BASE_DIR, "template"), archivo)


@app.route("/index.html")
def inicio_html():
    return redirect(url_for("inicio"))


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
