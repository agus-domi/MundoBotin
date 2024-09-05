from flask import Flask, render_template, request, redirect, url_for
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

# Listar clientes
def listar_clientes():
    query = "SELECT * FROM Cliente"
    cursor.execute(query)
    clientes = cursor.fetchall()
    return clientes

# Función para agregar un cliente
def alta_cliente(dni, nombre, apellido, direccion, contacto):
    query = "INSERT INTO Cliente (DNI, Nombre, Apellido, Direccion, Contacto) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (dni, nombre, apellido, direccion, contacto))
    conexion.commit()
    print("Cliente agregado con éxito")

# Ruta para manejar el formulario de alta de clientes
@app.route('/alta_cliente', methods=['POST'])
def alta_cliente_route():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    contacto = request.form['contacto']
    
    alta_cliente(dni, nombre, apellido, direccion, contacto)
    
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
def eliminar_cliente(dni):
    query = "DELETE FROM Cliente WHERE DNI = %s"
    cursor.execute(query, (dni,))
    conexion.commit()
    print("Cliente eliminado con éxito")

# Ruta para eliminar un cliente
@app.route('/eliminar_cliente/<dni>', methods=['POST'])
def eliminar_cliente_route(dni):
    eliminar_cliente(dni)
    return redirect(url_for('clientes'))

# Menú de clientes
@app.route('/clientes')
def clientes():
    clientes = listar_clientes()
    return render_template('clientes.html', clientes=clientes)



# Listar productos
def listar_productos():
    query = "SELECT * FROM Producto"
    cursor.execute(query)
    productos = cursor.fetchall()
    return productos

# Función para agregar un producto
def alta_producto(talle, marca, precio):
    query = "INSERT INTO Producto (Talle, Marca, Precio) VALUES (%s, %s, %s)"
    cursor.execute(query, (talle, marca, precio))
    conexion.commit()
    print("Producto agregado con éxito")

# Ruta para manejar el formulario de alta de productos
@app.route('/alta_producto', methods=['POST'])
def alta_producto_route():
    talle = request.form['talle']
    marca = request.form['marca']
    precio = request.form['precio']
    
    alta_producto(talle, marca, precio)
    
    return redirect(url_for('productos'))

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


# Menú de productos
@app.route('/productos')
def productos():
    productos = listar_productos()
    return render_template('productos.html', productos=productos)





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

    # Obtener clientes
    clientes = listar_clientes()

    # Obtener nombre y apellido del cliente seleccionado
    cliente_info = None
    if selected_cliente:
        cursor.execute("SELECT Nombre, Apellido FROM Cliente WHERE ID_Cliente = %s", (selected_cliente,))
        cliente_info = cursor.fetchone()

        # Obtener pedidos del cliente seleccionado
        query = """
        SELECT p.Fecha, pr.Marca AS producto, pr.Precio AS precio
        FROM Pedido p
        JOIN Tiene t ON p.ID_Pedido = t.ID_Pedido
        JOIN Producto pr ON t.ID_Producto = pr.ID_Producto
        WHERE p.ID_Cliente = %s
        """
        cursor.execute(query, (selected_cliente,))
        pedidos = cursor.fetchall()

        # Calcular el total
        total = sum(pedido[2] for pedido in pedidos)
    else:
        pedidos = []
        total = 0

    return render_template('pedidos.html', pedidos=pedidos, clientes=clientes, total=total, selected_cliente=selected_cliente, cliente_info=cliente_info)

if __name__ == '__main__':
    app.run(debug=True)
