from flask import Flask, render_template,request,redirect,session
from funciones import lee_diccionario_csv
#from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "asdfvfñfes7u2nairfn"
diccionario_usuarios = lee_diccionario_csv('usuarios.csv')

@app.route("/")
def index():
    return render_template("index.html")

#LOGIN entrar a la pagina con el usuario registrado
@app.route("/login/", methods= ["GET","POST"])
def login():
    if request.method == 'GET':
        msg = ''
        return render_template('signin.html',mensaje=msg)

    elif request.method == 'POST':
            usuario = request.form['usuario']
            #print(diccionario_usuarios)
            if usuario in diccionario_usuarios:
                password_db = diccionario_usuarios[usuario]['secreto'] # password guardado
                password_forma = request.form['contrasenia'] #password presentado
                #verificado = sha256_crypt.verify(password_forma,password_db)
                if (password_db == password_forma):
                    session['usuario'] = usuario
                    session['logged_in'] = True
                    if 'ruta' in session:
                        ruta = session['ruta']
                        session['ruta'] = None
                        return redirect(ruta)
                    else:
                        return redirect("/inicio")
                else:
                    msg = f'El password de {usuario} no corresponde'
                    return render_template('signin.html',mensaje=msg)
            else:
                msg = f'usuario {usuario} no existe'
                return render_template('signin.html',mensaje=msg)

#LOGOUT salir de la pagina
@app.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect("/")
    
#Inicio o vista del usuario
@app.route('/inicio', methods = ['GET'])
def Inicio():
    if request.method == 'GET':
        return render_template('inicio.html')

if __name__ == "__main__":
    app.run(debug=True)

   