from flask import Flask, render_template

app = Flask(__name__)

#codigo a completar
nombre = "MundoBotin"

@app.route('/')
def index():
   return render_template('index.html', nombre=nombre)


if __name__ == '__main__':
   app.run(debug=True)