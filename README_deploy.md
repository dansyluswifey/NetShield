Despliegue rápido de NetShield

Opciones recomendadas:
- Render (fácil, conecta con GitHub)
- Railway
- PythonAnywhere (si prefieres interfaz web)

Pasos rápidos (usando GitHub + Render):

1) Inicializa repo local y sube a GitHub (si no lo has hecho):

```bash
git init
git add .
git commit -m "Prepare app for deployment"
# crea el repo en GitHub y luego:
git remote add origin https://github.com/tu_usuario/tu_repo.git
git branch -M main
git push -u origin main
```

2) En Render:
- Crea una cuenta en https://render.com
- Nuevo "Web Service" → Conecta tu cuenta GitHub → Selecciona el repo
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Selecciona la rama `main` y despliega.

3) Variables de entorno:
- Agrega `SECRET_KEY`, credenciales de la base de datos, y configuración de correo.
- En Render las config se llaman Environment → Nuevo Secret.

4) Alternativa rápida con PythonAnywhere (subir archivos por web o scp):
- Crea una cuenta y sube el código
- Configura un Web App (Flask), apunta al `app.py` y al virtualenv

Notas:
- Si usas base de datos MySQL, configura el acceso desde el host y actualiza `database.py` para usar esas credenciales.
- Para SSL y dominio personalizado, sigue la documentación del proveedor (Render ofrece Let's Encrypt integrado).
