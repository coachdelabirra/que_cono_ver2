# -*- coding: utf-8 -*-
"""
db.py — Capa de datos con SQLite para 'Que coño ver?' V5
Sin servicios externos. 100% local / gratis. Un solo archivo .db en /data.

Incluye:
- Usuarios con LOGIN + PIN de 4 dígitos (hash con salt, sin librerías externas)
- Títulos con estado 'por_ver' (watchlist, sin calificar) o 'vista' (con birras)
- Amigos con solicitud / aceptar (para "seguir" gustos de amigos)
- Comentarios en perfiles
- Recomendaciones enviar / aceptar / rechazar
- Listas de seguimiento compartidas (varios miembros, mismos títulos)
- Alertas ("notificaciones") cuando un amigo termina de ver algo
"""
import sqlite3
import os
import hashlib
import secrets
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "quecono.db")
POSTERS_DIR = os.path.join(os.path.dirname(__file__), "data", "posters")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(POSTERS_DIR, exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pin_hash TEXT NOT NULL,
            pin_salt TEXT NOT NULL,
            bio TEXT DEFAULT '',
            creado TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS titulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('pelicula','serie')),
            titulo TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'vista' CHECK(estado IN ('vista','por_ver')),
            birras INTEGER CHECK (birras IS NULL OR birras BETWEEN 0 AND 6),
            poster TEXT,
            nota TEXT,
            fecha TEXT NOT NULL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS amistades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            de_usuario_id INTEGER NOT NULL,
            para_usuario_id INTEGER NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendiente' CHECK(estado IN ('pendiente','aceptada')),
            fecha TEXT NOT NULL,
            UNIQUE(de_usuario_id, para_usuario_id),
            FOREIGN KEY(de_usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY(para_usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            perfil_usuario_id INTEGER NOT NULL,
            autor_username TEXT NOT NULL,
            texto TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(perfil_usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS recomendaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            de_usuario_id INTEGER NOT NULL,
            para_usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('pelicula','serie')),
            titulo TEXT NOT NULL,
            mensaje TEXT,
            estado TEXT NOT NULL DEFAULT 'pendiente' CHECK(estado IN ('pendiente','aceptada','rechazada')),
            fecha TEXT NOT NULL,
            FOREIGN KEY(de_usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY(para_usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS listas_compartidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            creador_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(creador_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS lista_miembros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lista_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            UNIQUE(lista_id, usuario_id),
            FOREIGN KEY(lista_id) REFERENCES listas_compartidas(id) ON DELETE CASCADE,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS lista_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lista_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('pelicula','serie')),
            titulo TEXT NOT NULL,
            agregado_por TEXT NOT NULL,
            hecha INTEGER NOT NULL DEFAULT 0,
            fecha TEXT NOT NULL,
            FOREIGN KEY(lista_id) REFERENCES listas_compartidas(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            para_usuario_id INTEGER NOT NULL,
            mensaje TEXT NOT NULL,
            leida INTEGER NOT NULL DEFAULT 0,
            fecha TEXT NOT NULL,
            FOREIGN KEY(para_usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


# ---------- Login: usuario + PIN de 4 dígitos ----------

def _hash_pin(pin: str, salt: str) -> str:
    return hashlib.sha256((salt + pin).encode("utf-8")).hexdigest()


def username_exists(username: str) -> bool:
    conn = get_conn()
    row = conn.execute("SELECT id FROM usuarios WHERE username = ?", (username.strip(),)).fetchone()
    conn.close()
    return row is not None


def crear_usuario(username: str, pin: str) -> int:
    """Crea un usuario nuevo con su PIN de 4 digitos. Lanza ValueError si ya existe."""
    username = username.strip()
    if username_exists(username):
        raise ValueError("Ese usuario ya existe.")
    salt = secrets.token_hex(8)
    pin_hash = _hash_pin(pin, salt)
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO usuarios (username, pin_hash, pin_salt, bio, creado) VALUES (?, ?, ?, '', ?)",
        (username, pin_hash, salt, datetime.now().isoformat()),
    )
    conn.commit()
    uid = c.lastrowid
    conn.close()
    return uid


def verificar_login(username: str, pin: str):
    """Devuelve el id de usuario si el PIN es correcto, o None si falla."""
    conn = get_conn()
    row = conn.execute(
        "SELECT id, pin_hash, pin_salt FROM usuarios WHERE username = ?", (username.strip(),)
    ).fetchone()
    conn.close()
    if not row:
        return None
    if _hash_pin(pin, row["pin_salt"]) == row["pin_hash"]:
        return row["id"]
    return None


def get_user_by_username(username: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM usuarios WHERE username = ?", (username.strip(),)).fetchone()
    conn.close()
    return row


def set_bio(usuario_id, bio):
    conn = get_conn()
    conn.execute("UPDATE usuarios SET bio = ? WHERE id = ?", (bio, usuario_id))
    conn.commit()
    conn.close()


def list_usernames(excluir_id=None):
    conn = get_conn()
    if excluir_id:
        rows = conn.execute(
            "SELECT username FROM usuarios WHERE id != ? ORDER BY username", (excluir_id,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT username FROM usuarios ORDER BY username").fetchall()
    conn.close()
    return [r["username"] for r in rows]


# ---------- Titulos (peliculas / series) ----------

def add_titulo(usuario_id, tipo, titulo, estado="vista", birras=None, poster=None, nota=""):
    conn = get_conn()
    conn.execute(
        """INSERT INTO titulos (usuario_id, tipo, titulo, estado, birras, poster, nota, fecha)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (usuario_id, tipo, titulo.strip(), estado, birras, poster, nota, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    if estado == "vista":
        _notificar_amigos_titulo_visto(usuario_id, titulo)


def update_titulo(titulo_id, titulo=None, birras=None, poster=None, nota=None, estado=None):
    conn = get_conn()
    c = conn.cursor()
    estado_anterior = None
    row = None
    if estado is not None:
        row = c.execute("SELECT estado, usuario_id, titulo FROM titulos WHERE id = ?", (titulo_id,)).fetchone()
        if row:
            estado_anterior = row["estado"]

    fields, values = [], []
    if titulo is not None:
        fields.append("titulo = ?"); values.append(titulo.strip())
    if birras is not None:
        fields.append("birras = ?"); values.append(birras)
    if poster is not None:
        fields.append("poster = ?"); values.append(poster)
    if nota is not None:
        fields.append("nota = ?"); values.append(nota)
    if estado is not None:
        fields.append("estado = ?"); values.append(estado)
    if not fields:
        conn.close()
        return
    values.append(titulo_id)
    c.execute(f"UPDATE titulos SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()

    if estado == "vista" and estado_anterior == "por_ver" and row:
        _notificar_amigos_titulo_visto(row["usuario_id"], titulo or row["titulo"])
    conn.close()


def delete_titulo(titulo_id):
    conn = get_conn()
    conn.execute("DELETE FROM titulos WHERE id = ?", (titulo_id,))
    conn.commit()
    conn.close()


def get_ranking(usuario_id, tipo=None, estado="vista"):
    """Ranking automatico: SQLite ordena de mayor a menor birras (6 -> 0)."""
    conn = get_conn()
    query = "SELECT * FROM titulos WHERE usuario_id = ? AND estado = ?"
    params = [usuario_id, estado]
    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)
    query += " ORDER BY birras DESC, fecha DESC" if estado == "vista" else " ORDER BY fecha DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def get_titulo(titulo_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM titulos WHERE id = ?", (titulo_id,)).fetchone()
    conn.close()
    return row


# ---------- Amigos: solicitud / aceptar ----------

def enviar_solicitud_amistad(de_usuario_id, para_username):
    para = get_user_by_username(para_username)
    if not para:
        return False, "Ese usuario no existe."
    if para["id"] == de_usuario_id:
        return False, "No puedes agregarte a ti mismo."
    conn = get_conn()
    ya = conn.execute(
        "SELECT * FROM amistades WHERE de_usuario_id=? AND para_usuario_id=?",
        (de_usuario_id, para["id"]),
    ).fetchone()
    if ya:
        conn.close()
        return False, "Ya le enviaste una solicitud (o ya son amigos)."
    conn.execute(
        "INSERT INTO amistades (de_usuario_id, para_usuario_id, estado, fecha) VALUES (?, ?, 'pendiente', ?)",
        (de_usuario_id, para["id"], datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return True, f"Solicitud enviada a {para_username}."


def solicitudes_pendientes(usuario_id):
    """Solicitudes que ME enviaron y aun no acepto."""
    conn = get_conn()
    rows = conn.execute(
        """SELECT a.id, u.username, a.fecha FROM amistades a
           JOIN usuarios u ON u.id = a.de_usuario_id
           WHERE a.para_usuario_id = ? AND a.estado = 'pendiente'
           ORDER BY a.fecha DESC""",
        (usuario_id,),
    ).fetchall()
    conn.close()
    return rows


def aceptar_solicitud(solicitud_id):
    conn = get_conn()
    conn.execute("UPDATE amistades SET estado='aceptada' WHERE id = ?", (solicitud_id,))
    conn.commit()
    conn.close()


def rechazar_solicitud(solicitud_id):
    conn = get_conn()
    conn.execute("DELETE FROM amistades WHERE id = ?", (solicitud_id,))
    conn.commit()
    conn.close()


def list_friends(usuario_id):
    """Amigos con amistad aceptada en cualquiera de los dos sentidos."""
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT u.username FROM amistades a
        JOIN usuarios u ON u.id = a.para_usuario_id
        WHERE a.de_usuario_id = ? AND a.estado = 'aceptada'
        UNION
        SELECT u.username FROM amistades a
        JOIN usuarios u ON u.id = a.de_usuario_id
        WHERE a.para_usuario_id = ? AND a.estado = 'aceptada'
        ORDER BY username
        """,
        (usuario_id, usuario_id),
    ).fetchall()
    conn.close()
    return [r["username"] for r in rows]


def remove_friend(usuario_id, amigo_username):
    amigo = get_user_by_username(amigo_username)
    if not amigo:
        return
    conn = get_conn()
    conn.execute(
        """DELETE FROM amistades WHERE
           (de_usuario_id=? AND para_usuario_id=?) OR (de_usuario_id=? AND para_usuario_id=?)""",
        (usuario_id, amigo["id"], amigo["id"], usuario_id),
    )
    conn.commit()
    conn.close()


def compatibilidad(usuario_id, amigo_username):
    amigo = get_user_by_username(amigo_username)
    if not amigo:
        return None, []
    conn = get_conn()
    mios = conn.execute(
        "SELECT titulo, birras FROM titulos WHERE usuario_id=? AND estado='vista'", (usuario_id,)
    ).fetchall()
    suyos = conn.execute(
        "SELECT titulo, birras FROM titulos WHERE usuario_id=? AND estado='vista'", (amigo["id"],)
    ).fetchall()
    conn.close()

    mios_dict = {r["titulo"].lower(): r["birras"] for r in mios}
    suyos_dict = {r["titulo"].lower(): r["birras"] for r in suyos}
    if not mios_dict or not suyos_dict:
        return 0, []

    comunes = set(mios_dict) & set(suyos_dict)
    coincidencias, puntos = [], 0
    for t in comunes:
        dif = abs(mios_dict[t] - suyos_dict[t])
        puntos += max(0, 6 - dif)
        coincidencias.append((t, mios_dict[t], suyos_dict[t]))

    universo = len(set(mios_dict) | set(suyos_dict))
    max_puntos = universo * 6 if universo else 1
    porcentaje = round((puntos / max_puntos) * 100) if universo else 0
    return porcentaje, coincidencias


def actividad_amigos(usuario_id, limite=15):
    """Ultimos titulos marcados como 'vista' por mis amigos (para 'ver que estan mirando')."""
    amigos = list_friends(usuario_id)
    if not amigos:
        return []
    conn = get_conn()
    placeholders = ",".join("?" for _ in amigos)
    rows = conn.execute(
        f"""SELECT u.username, t.tipo, t.titulo, t.birras, t.fecha
            FROM titulos t JOIN usuarios u ON u.id = t.usuario_id
            WHERE u.username IN ({placeholders}) AND t.estado = 'vista'
            ORDER BY t.fecha DESC LIMIT ?""",
        (*amigos, limite),
    ).fetchall()
    conn.close()
    return rows


# ---------- Comentarios en perfil ----------

def add_comentario(perfil_username, autor_username, texto):
    perfil = get_user_by_username(perfil_username)
    if not perfil:
        return
    conn = get_conn()
    conn.execute(
        "INSERT INTO comentarios (perfil_usuario_id, autor_username, texto, fecha) VALUES (?, ?, ?, ?)",
        (perfil["id"], autor_username, texto.strip(), datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_comentarios(usuario_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM comentarios WHERE perfil_usuario_id = ? ORDER BY fecha DESC", (usuario_id,)
    ).fetchall()
    conn.close()
    return rows


# ---------- Recomendaciones ----------

def enviar_recomendacion(de_usuario_id, para_username, tipo, titulo, mensaje=""):
    para = get_user_by_username(para_username)
    if not para:
        return False, "Ese usuario no existe."
    conn = get_conn()
    conn.execute(
        """INSERT INTO recomendaciones (de_usuario_id, para_usuario_id, tipo, titulo, mensaje, estado, fecha)
           VALUES (?, ?, ?, ?, ?, 'pendiente', ?)""",
        (de_usuario_id, para["id"], tipo, titulo.strip(), mensaje, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return True, f"Recomendación enviada a {para_username}."


def recomendaciones_recibidas(usuario_id, estado="pendiente"):
    conn = get_conn()
    rows = conn.execute(
        """SELECT r.*, u.username AS de_username FROM recomendaciones r
           JOIN usuarios u ON u.id = r.de_usuario_id
           WHERE r.para_usuario_id = ? AND r.estado = ?
           ORDER BY r.fecha DESC""",
        (usuario_id, estado),
    ).fetchall()
    conn.close()
    return rows


def responder_recomendacion(rec_id, aceptar: bool):
    conn = get_conn()
    rec = conn.execute("SELECT * FROM recomendaciones WHERE id = ?", (rec_id,)).fetchone()
    if not rec:
        conn.close()
        return
    nuevo_estado = "aceptada" if aceptar else "rechazada"
    conn.execute("UPDATE recomendaciones SET estado = ? WHERE id = ?", (nuevo_estado, rec_id))
    conn.commit()
    conn.close()
    if aceptar:
        add_titulo(rec["para_usuario_id"], rec["tipo"], rec["titulo"], estado="por_ver")


# ---------- Listas de seguimiento compartidas ----------

def crear_lista_compartida(nombre, creador_id, miembros_usernames):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO listas_compartidas (nombre, creador_id, fecha) VALUES (?, ?, ?)",
        (nombre.strip(), creador_id, datetime.now().isoformat()),
    )
    lista_id = c.lastrowid
    c.execute("INSERT OR IGNORE INTO lista_miembros (lista_id, usuario_id) VALUES (?, ?)", (lista_id, creador_id))
    for uname in miembros_usernames:
        u = get_user_by_username(uname)
        if u:
            c.execute(
                "INSERT OR IGNORE INTO lista_miembros (lista_id, usuario_id) VALUES (?, ?)",
                (lista_id, u["id"]),
            )
    conn.commit()
    conn.close()
    return lista_id


def mis_listas_compartidas(usuario_id):
    conn = get_conn()
    rows = conn.execute(
        """SELECT l.* FROM listas_compartidas l
           JOIN lista_miembros m ON m.lista_id = l.id
           WHERE m.usuario_id = ? ORDER BY l.fecha DESC""",
        (usuario_id,),
    ).fetchall()
    conn.close()
    return rows


def miembros_lista(lista_id):
    conn = get_conn()
    rows = conn.execute(
        """SELECT u.username FROM lista_miembros m
           JOIN usuarios u ON u.id = m.usuario_id WHERE m.lista_id = ?""",
        (lista_id,),
    ).fetchall()
    conn.close()
    return [r["username"] for r in rows]


def add_item_lista(lista_id, tipo, titulo, agregado_por):
    conn = get_conn()
    conn.execute(
        """INSERT INTO lista_items (lista_id, tipo, titulo, agregado_por, hecha, fecha)
           VALUES (?, ?, ?, ?, 0, ?)""",
        (lista_id, tipo, titulo.strip(), agregado_por, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def items_lista(lista_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM lista_items WHERE lista_id = ? ORDER BY hecha ASC, fecha DESC", (lista_id,)
    ).fetchall()
    conn.close()
    return rows


def marcar_item_lista(item_id, hecha: bool):
    conn = get_conn()
    conn.execute("UPDATE lista_items SET hecha = ? WHERE id = ?", (1 if hecha else 0, item_id))
    conn.commit()
    conn.close()


def delete_item_lista(item_id):
    conn = get_conn()
    conn.execute("DELETE FROM lista_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# ---------- Alertas / notificaciones ----------

def _notificar_amigos_titulo_visto(usuario_id, titulo):
    conn = get_conn()
    yo = conn.execute("SELECT username FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    conn.close()
    if not yo:
        return
    amigos = list_friends(usuario_id)
    if not amigos:
        return
    conn = get_conn()
    c = conn.cursor()
    for a in amigos:
        u = c.execute("SELECT id FROM usuarios WHERE username = ?", (a,)).fetchone()
        if u:
            c.execute(
                "INSERT INTO alertas (para_usuario_id, mensaje, leida, fecha) VALUES (?, ?, 0, ?)",
                (u["id"], f"🍿 {yo['username']} terminó de ver '{titulo}'", datetime.now().isoformat()),
            )
    conn.commit()
    conn.close()


def get_alertas(usuario_id, solo_no_leidas=False):
    conn = get_conn()
    if solo_no_leidas:
        rows = conn.execute(
            "SELECT * FROM alertas WHERE para_usuario_id=? AND leida=0 ORDER BY fecha DESC",
            (usuario_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM alertas WHERE para_usuario_id=? ORDER BY fecha DESC LIMIT 30",
            (usuario_id,),
        ).fetchall()
    conn.close()
    return rows


def marcar_alertas_leidas(usuario_id):
    conn = get_conn()
    conn.execute("UPDATE alertas SET leida = 1 WHERE para_usuario_id = ?", (usuario_id,))
    conn.commit()
    conn.close()
