from pickle import TRUE
from flask import Flask, render_template,request,redirect,session
from funciones import *
#from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "asdfvfñfes7u2nairfn"
diccionario_usuarios = lee_diccionario_csv('usuarios.csv')
lista_mascotas = crea_lista_mascotas('mascotas.csv')

# Creamos el diccionario del cliente
dcliente = {'Agregar cita':'/citas',
            'Citas anteriores':'/anteriores',
            'Mis mascotas':'/mascotas'
}

# Creamos el diccionario usuario haciendo una copia del diccionario cliente con 2 valores extra
dusuario = dcliente.copy()
dusuario['Receta'] = '/recetas'
dusuario['Procedimiento'] = '/procedimiento'

# Creamos el diccionario admin haciendo una copia del diccionario usuario con 2 valores extra
dadmin = dusuario.copy()
dadmin['Usuarios'] = '/usuarios'
dadmin['Informes'] = '/informes'

# Ruteamos cada uno  de los diccionarios
dmenus = {'cliente':dcliente,
          'usuario':dusuario,
          'admin':dadmin,}

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
                    # if 'ruta' in session:
                    #     ruta = session['ruta']
                    #     session['ruta'] = None
                    #     return redirect(ruta)
                    # else:
                    return redirect(f"/inicio/{usuario}")
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
@app.route('/inicio/<usuario>', methods = ['GET'])
def Inicio(usuario):
    if usuario in diccionario_usuarios and session:
        if request.method == 'GET':
            tipo = diccionario_usuarios[usuario]['tipo']
            menu = dmenus[tipo]
            #print(menu)
            return render_template('inicio.html', menu=menu)
    else:
        return render_template('error-404.html')

#mascotas del cliente
@app.route('/mascotas', methods = ['GET','POST'])
def mascotas():
    if request.method == 'GET':
        return render_template('mascotas.html',mascotas = lista_mascotas, usuario = session['usuario'])
    elif request.method == 'POST':
        #funcion para eliminar mascota
        return render_template('mascotas.html',mascotas = lista_mascotas, usuario = session['usuario'])
        
if __name__ == "__main__":
    app.run(debug=True)

   