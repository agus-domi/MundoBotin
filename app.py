from flask import *

app = Flask(__name__)

#página principal
@app.route('/')
def index():
  return render_template('index.html')

#menu clientes
@app.route('/clientes')
def clientes():
  return render_template('clientes.html')

#menu productos
@app.route('/productos')
def productos():
  return render_template('productos.html')

#menu pedidos
@app.route('/pedidos')
def pedidos():
  return render_template('pedidos.html')

if __name__ == '__main__':
  app.run(debug=True)