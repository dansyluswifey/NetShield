import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from database import obtener_conexion

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "netshield_super_secret")

# 📧 CONFIGURACIÓN DEL SERVIDOR DE CORREO
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo_universitario_o_personal@gmail.com' 
app.config['MAIL_PASSWORD'] = 'tus_16_letras_de_google_sin_espacios' 
app.config['MAIL_DEFAULT_SENDER'] = ('NetShield Platform 🛡️', 'tu_correo_universitario_o_personal@gmail.com')

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html', vista_actual='login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al panel.", "error")
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', 
                           username=session.get('username'), 
                           avatar=session.get('avatar'))

@app.route('/modulo1')
def modulo1():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al módulo.", "error")
        return redirect(url_for('login_page'))
    return render_template('modulo1.html', 
                           username=session.get('username'), 
                           avatar=session.get('avatar'))

@app.route('/modulo2')
def modulo2():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al módulo.", "error")
        return redirect(url_for('login_page'))
    return render_template('modulo2.html', 
                           username=session.get('username'), 
                           avatar=session.get('avatar'))

@app.route('/modulo3')
def modulo3():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al módulo.", "error")
        return redirect(url_for('login_page'))
    return render_template('modulo3.html', 
                           username=session.get('username'), 
                           avatar=session.get('avatar'))

@app.route('/modulo4')
def modulo4():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al módulo.", "error")
        return redirect(url_for('login_page'))
    return render_template('modulo4.html', 
                           username=session.get('username'), 
                           avatar=session.get('avatar'))

@app.route('/modulo5')
def modulo5():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al módulo.", "error")
        return redirect(url_for('login_page'))
    return render_template('modulo5.html', 
                           username=session.get('username'), 
                           avatar=session.get('avatar'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for('home'))

@app.route('/update-avatar', methods=['POST'])
def update_avatar():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    payload = request.get_json(silent=True) or {}
    new_avatar = payload.get('avatar')
    if not new_avatar or not new_avatar.startswith('avatar') or not new_avatar.endswith('.png'):
        return jsonify({'error': 'Avatar inválido'}), 400

    conexion = obtener_conexion()
    if not conexion:
        return jsonify({'error': 'Error de conexión'}), 500

    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET avatar = %s WHERE id = %s", (new_avatar, session['user_id']))
        conexion.commit()
        cursor.close()
        conexion.close()
        session['avatar'] = new_avatar
        return jsonify({'success': True, 'avatar': new_avatar})
    except Exception as e:
        print(f"Error actualizando avatar: {e}")
        return jsonify({'error': 'No se pudo guardar el avatar'}), 500

# 🐬 INICIO DE SESIÓN CORREGIDO
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conexion = obtener_conexion()
    if not conexion:
        flash("Error de conexión con el servidor.", "error")
        return redirect(url_for('login_page'))
        
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    
    if usuario and usuario['password'] == password:
        raw_avatar = usuario.get('avatar', '')
        if raw_avatar and not raw_avatar.startswith('avatar'):
            raw_avatar = 'avatar' + raw_avatar
        session['user_id'] = usuario['id']
        session['username'] = usuario['username']
        session['avatar'] = raw_avatar
        return redirect(url_for('dashboard'))
    else:
        flash("Credenciales incorrectas o usuario no registrado.", "error")
        return redirect(url_for('login_page'))

# 📧 REGISTRO BLINDADO (Si falla el mail, avanza para que no se quede cargando)
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    avatar = request.form.get('avatar')

    codigo_verificacion = str(random.randint(100000, 999999))
    
    session['temp_user'] = {
        'username': username,
        'email': email,
        'password': password,
        'avatar': avatar,
        'codigo': codigo_verificacion
    }

    try:
        msg = Message("Tu código de verificación NetShield 🛡️", recipients=[email])
        msg.body = f"¡Hola, {username}!\n\nTu código de seguridad para dar de alta tu cuenta en NetShield es: {codigo_verificacion}"
        mail.send(msg)
        flash("Código enviado. Revisa tu correo.", "success")
    except Exception as e:
        # Pasa en fa si tus credenciales de Gmail no están listas todavía
        print(f"⚠️ Alerta Mail: {str(e)}")
        flash(f"Modo desarrollo activo. Código simulado: {codigo_verificacion}", "success")
        
    return render_template('login.html', vista_actual='verify')

# 💾 VERIFICACIÓN E INSERCIÓN EN MYSQL
@app.route('/verify', methods=['POST'])
def verify():
    codigo_ingresado = request.form.get('code')
    datos_usuario = session.get('temp_user')

    if not datos_usuario:
        flash("La sesión expiró. Inténtalo de nuevo.", "error")
        return redirect(url_for('login_page'))

    if codigo_ingresado == datos_usuario['codigo']:
        conexion = obtener_conexion()
        if not conexion:
            flash("Error de conexión al salvar los datos.", "error")
            return redirect(url_for('login_page'))
            
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO usuarios (username, email, password, avatar) VALUES (%s, %s, %s, %s)"
            valores = (datos_usuario['username'], datos_usuario['email'], datos_usuario['password'], datos_usuario['avatar'])
            cursor.execute(query, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            
            session.pop('temp_user', None)
            flash("¡Cuenta creada! Inicia sesión.", "success")
            return redirect(url_for('login_page'))
        except Exception as e:
            flash("El usuario o email ya existe.", "error")
            return redirect(url_for('login_page'))
    else:
        flash("Código incorrecto.", "error")
        return render_template('login.html', vista_actual='verify')

if __name__ == '__main__':
    app.run(debug=True)