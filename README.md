# 🛠️ FERREMAS Online

**FERREMAS Online** es una plataforma web desarrollada para la empresa **FERREMAS**. El sistema incluye una interfaz web, una base de datos y múltiples APIs que interactúan directamente con dicha base.

---

## 🚀 Tecnologías utilizadas

- **Frontend y Backend principal**: Django
- **Base de datos**: Oracle SQL
- **APIs REST**: FastAPI y Spring Boot

---

## ⚙️ Instalación y ejecución

## Instalación
1. Descargar repositorio:
```bash
git clone https://github.com/DanGamer23/Integracion25.git
```

2. Entrar a la carpeta del proyecto:
```bash
cd Integracion25
```

3. Crear ambiente virtual de python:
```bash
python -m venv venv
```

4. Activar ambiente virtual:
```bash
source venv/Scripts/activate
```

5. Instalar dependencias para python en el ambiente virtual:
```bash
pip install -r requirements.txt
```

6. Levantar API:
```bash
uvicorn API1.main:app --reload
```