\# Configuración inicial del proyecto



\## 1. Crear estructura de carpetas

\- Ejecutar como Administrador (si es necesario) `setup\_project.bat`

\- Se generarán todas las carpetas y archivos vacíos.



\## 2. Inicializar repositorio Git y ramas

\- Crear un repositorio vacío en GitHub (sin README, sin .gitignore).

\- En tu computadora, dentro de la carpeta del proyecto:

&#x20; ```bash

&#x20; git init

&#x20; git remote add origin https://github.com/tuusuario/auditoria-codigo.git

&#x20; git add .

&#x20; git commit -m "chore: estructura inicial del proyecto"

&#x20; git push -u origin main

