from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import database.Elbase as base
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey' #algo mucho muy importante para que funcione flash

def no_cache(response): #Borra la cache para no guardar las sesiones
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html'), 405

@app.route('/', methods= ['GET','POST']) #El get para mostrar el formulario y el post para procesarlo ._.
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        # nombre = base.get_user_property('NombreUser', email)
        print(hashlib.sha256(password.encode()).hexdigest() , base.get_user_property('Password', email))
        #OBVIAMENTE CAMBIAR LOGICA
        if hashlib.sha256(password.encode()).hexdigest() == base.get_user_property('Password', email):
            session['user'] = email  
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.')
    return render_template("login.html")
# --------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
# --------------------------------------------------
@app.route('/Recuperar-contraseña')
def forgot_password():
    return render_template("forgotPassword.html")
# --------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    response = make_response(render_template("dashboard.html", email=session['user']))
    return no_cache(response)
    
@app.route("/Nuevo-alumno")
def new_student():
    return render_template("new-student.html")
    

@app.route('/submit', methods=['POST'])
def formulario():
    data = request.form
    print(data)
    return "Datos recibidos", 200

@app.route("/curso")
def curso():
    return render_template("cursos.html")
    
if __name__ == '__main__':
    app.run(debug=True)
