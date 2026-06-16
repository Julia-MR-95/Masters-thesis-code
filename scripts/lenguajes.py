import sqlite3

# Conexión a SQLite
conn = sqlite3.connect("../database/datos.db")
cursor = conn.cursor()

# Crear tabla (por si no existe)
cursor.execute("""
CREATE TABLE IF NOT EXISTS lenguas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT
)
""")

with open("../resources/Languages.tab", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        # Saltar líneas vacías o cabecera
        if not line or line.startswith("LangID") or line.startswith("------"):
            continue

        # Dividir en máximo 4 partes
        partes = line.split(maxsplit=3)

        if len(partes) == 4:
            nombre = partes[3]
            cursor.execute(
                "INSERT INTO lenguas (nombre) VALUES (?)",
                (nombre,)
            )

conn.commit()
conn.close()

