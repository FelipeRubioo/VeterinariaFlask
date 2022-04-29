

from flask import Flask, render_template,request


app = Flask(__name__)

@app.route("/", methods= ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('Signin.html')
    

@app.route('/templates/Inicio.html', methods = ['POST'])
def Inicio():
    if request.method == 'POST':
        return render_template("Inicio.html", correo = request.form['correo'])

if __name__ == "__main__":
    app.run(debug=True)

   