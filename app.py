from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="bgfxs8zjfhryjvdjvfn7-mysql.services.clever-cloud.com",
    user="uxynm85rauhe3m0g",
    password="SEpLfM7642MAPjmODuH9",
    database="bgfxs8zjfhryjvdjvfn7"
)

cursor = conexion.cursor()

app = Flask(__name__)

# Página principal
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Menú de clientes
@app.route('/clientes')
def clientes():
    query = "SELECT * FROM Cliente"
    cursor.execute(query)
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=clientes)


# Agregar un Cliente
@app.route('/alta_cliente', methods=['POST'])
def alta_cliente(): #Obtengo los datos del Formulario
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    contacto = request.form['contacto']
    
    #Lo agrego a la Base de Datos
    query = "INSERT INTO Cliente (DNI, Nombre, Apellido, Direccion, Contacto) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (dni, nombre, apellido, direccion, contacto))
    conexion.commit()
    return redirect(url_for('clientes'))

# Función para obtener los datos de un cliente
def obtener_cliente(dni):
    query = "SELECT * FROM Cliente WHERE DNI = %s"
    cursor.execute(query, (dni,))
    cliente = cursor.fetchone()
    return cliente
# Función para modificar un cliente
def modificar_cliente(dni_actual, nuevo_dni, nombre, apellido, direccion, contacto):
    query = """
        UPDATE Cliente 
        SET DNI = %s, Nombre = %s, Apellido = %s, Direccion = %s, Contacto = %s
        WHERE DNI = %s
    """
    cursor.execute(query, (nuevo_dni, nombre, apellido, direccion, contacto, dni_actual))
    conexion.commit()
    print("Cliente modificado con éxito")

# Ruta para mostrar el formulario de edición de cliente
@app.route('/editar_cliente/<dni>', methods=['GET', 'POST'])
def editar_cliente_route(dni):
    cliente = obtener_cliente(dni)
    
    if request.method == 'POST':
        # Obtener los datos modificados del formulario
        nuevo_dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        contacto = request.form['contacto']
        
        # Llamar a la función para actualizar el cliente
        modificar_cliente(dni, nuevo_dni, nombre, apellido, direccion, contacto)
        
        return redirect(url_for('clientes'))
    
    return render_template('editar_cliente.html', cliente=cliente)

# Función para eliminar un cliente
def eliminar_cliente(id_cliente):
    query = "DELETE FROM Cliente WHERE ID_Cliente = %s"
    cursor.execute(query, (id_cliente,))
    conexion.commit()

# Ruta para eliminar un cliente
@app.route('/eliminar_cliente/<id_cliente>', methods=['POST'])
def eliminar_cliente_route(id_cliente):
    eliminar_cliente(id_cliente)
    return redirect(url_for('clientes'))


# Menú de productos
@app.route('/productos')
def productos():
    query = "SELECT * FROM Producto"
    cursor.execute(query)
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

# Agregar un Producto
@app.route('/alta_producto', methods=['POST'])
def alta_producto(): #Obtengo los datos del Formulario
    talle = request.form['talle']
    marca = request.form['marca']
    precio = request.form['precio']
    
    #Lo agrego a la Base de Datos
    query = "INSERT INTO Producto (Talle, Marca, Precio) VALUES (%s, %s, %s)"
    cursor.execute(query, (talle, marca, precio))
    conexion.commit()
    return redirect(url_for('productos'))

# Función para obtener los datos de un producto
def obtener_producto(id_producto):
    query = "SELECT * FROM Producto WHERE ID_Producto = %s"
    cursor.execute(query, (id_producto,))
    producto = cursor.fetchone()
    return producto

# Función para modificar un producto
def modificar_producto(id_producto, talle, marca, precio):
    query = """
        UPDATE Producto 
        SET Talle = %s, Marca = %s, Precio = %s
        WHERE ID_Producto = %s
    """
    cursor.execute(query, (talle, marca, precio, id_producto))
    conexion.commit()
    print("Producto modificado con éxito")

# Ruta para mostrar el formulario de edición de producto
@app.route('/editar_producto/<id_producto>', methods=['GET', 'POST'])
def editar_producto_route(id_producto):
    producto = obtener_producto(id_producto)
    
    if request.method == 'POST':
        # Obtener los datos modificados del formulario
        talle = request.form['talle']
        marca = request.form['marca']
        precio = request.form['precio']
        
        # Llamar a la función para actualizar el producto
        modificar_producto(id_producto, talle, marca, precio)
        
        return redirect(url_for('productos'))
    
    return render_template('editar_producto.html', producto=producto)




# Función para eliminar un producto
def eliminar_producto(id_producto):
    query = "DELETE FROM Producto WHERE ID_Producto = %s"
    cursor.execute(query, (id_producto,))
    conexion.commit()
    print("Producto eliminado con éxito")

# Ruta para eliminar un producto
@app.route('/eliminar_producto/<id_producto>', methods=['POST'])
def eliminar_producto_route(id_producto):
    eliminar_producto(id_producto)
    return redirect(url_for('productos'))




# Listar pedidos
def listar_pedidos():
    query = "SELECT * FROM Pedido"
    cursor.execute(query)
    pedidos = cursor.fetchall()
    return pedidos

# Menú de pedidos
@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    selected_cliente = request.form.get('cliente_id', '')

    # Obtener lista de clientes
    query_clientes = "SELECT * FROM Cliente"
    cursor.execute(query_clientes)
    clientes = cursor.fetchall()

    # Obtener nombre del cliente seleccionado
    cliente_info = None
    if selected_cliente:
        cursor.execute("SELECT Nombre, Apellido FROM Cliente WHERE ID_Cliente = %s", (selected_cliente,))
        cliente_info = cursor.fetchone()

    # Obtener lista de productos
    query_productos = "SELECT * FROM Producto"
    cursor.execute(query_productos)
    productos = cursor.fetchall()

    # Obtener pedidos del cliente
    pedidos = []
    total = 0
    if cliente_info:
        query_pedidos = """
        SELECT p.ID_Pedido, p.Fecha, pr.Marca, pr.Precio
        FROM Pedido p
        JOIN Tiene t ON p.ID_Pedido = t.ID_Pedido
        JOIN Producto pr ON t.ID_Producto = pr.ID_Producto
        WHERE p.ID_Cliente = %s
        """
        cursor.execute(query_pedidos, (selected_cliente,))
        pedidos = cursor.fetchall()
        total = sum(pedido[3] for pedido in pedidos)  # Actualiza el índice a 3 para obtener el precio

    return render_template(
        'pedidos.html', pedidos=pedidos, clientes=clientes, productos=productos,
        total=total, selected_cliente=selected_cliente, cliente_info=cliente_info,
        fecha_actual=datetime.now().strftime('%Y-%m-%d')
    )



@app.route('/agregar_pedido', methods=['POST'])
def agregar_pedido():
    cliente_id = request.form['cliente_id']
    productos_ids = request.form.getlist('producto_id')  # Lista de productos seleccionados
    fecha = datetime.now().strftime('%Y-%m-%d')  # Fecha actual

    # Insertar el pedido en la tabla Pedido
    query_pedido = "INSERT INTO Pedido (Fecha, ID_Cliente, Monto) VALUES (%s, %s, 0)"  # Monto inicialmente en 0
    cursor.execute(query_pedido, (fecha, cliente_id))
    conexion.commit()

    # Obtener el ID del nuevo pedido
    pedido_id = cursor.lastrowid
    total_monto = 0

    # Insertar cada producto seleccionado en la tabla Tiene y calcular el total
    for producto_id in productos_ids:
        query_tiene = "INSERT INTO Tiene (ID_Pedido, ID_Producto) VALUES (%s, %s)"
        cursor.execute(query_tiene, (pedido_id, producto_id))
        
        # Obtener el precio del producto y sumarlo al monto total
        query_precio = "SELECT Precio FROM Producto WHERE ID_Producto = %s"
        cursor.execute(query_precio, (producto_id,))
        precio = cursor.fetchone()[0]
        total_monto += precio

    # Actualizar el monto total en el pedido
    query_actualizar_monto = "UPDATE Pedido SET Monto = %s WHERE ID_Pedido = %s"
    cursor.execute(query_actualizar_monto, (total_monto, pedido_id))
    conexion.commit()

    return redirect(url_for('pedidos'))

# Ruta para eliminar un pedido
@app.route('/eliminar_pedido', methods=['POST'])
def eliminar_pedido():
    pedido_id = request.form.get('ID')
    # Primero, elimina todas las relaciones de productos del pedido en la tabla 'Tiene'
    query_eliminar_tiene = 'DELETE FROM Tiene WHERE ID_Pedido = %s'
    cursor.execute(query_eliminar_tiene, (pedido_id,))
        
    # Luego, elimina el pedido de la tabla 'Pedido'
    query_eliminar_pedido = 'DELETE FROM Pedido WHERE ID_Pedido = %s'
    cursor.execute(query_eliminar_pedido, (pedido_id,))
        
    # Confirma los cambios
    conexion.commit()
    
    # Redirige a la página de pedidos
    return redirect(url_for('pedidos'))


if __name__ == '__main__':
    app.run(debug=True)