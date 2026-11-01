# Tu Tienda de Ropa (Flask)

Tienda online con catálogo, carrito en sesión, checkout y pedidos guardados en SQLite.

## Funcionalidades
- Catálogo de productos desde la base de datos (con stock)
- Carrito: agregar, actualizar cantidad, quitar (se guarda en la sesión)
- Checkout con validación y descuento de stock en una transacción
- Pedidos e ítems guardados con el precio al momento de la compra
- Protección CSRF en todos los formularios POST

## Instalación
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
flask --app app run --debug
```
La base `tienda.db` se crea sola con los 8 productos de ejemplo la primera vez.

## Estructura
- `app.py`: rutas, base de datos y lógica del carrito
- `templates/`: vistas Jinja2 (`base.html` comparte header y footer)
- `static/`: CSS, imágenes y JS (los de tu repo original)

## Próximos pasos
- [ ] Registro y login de clientes
- [ ] Panel de administración (productos y pedidos)
- [ ] Pago con Mercado Pago (modo prueba)
