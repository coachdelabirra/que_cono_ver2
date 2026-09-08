# -*- coding: utf-8 -*-
"""
🍿 Que coño ver? 🍺  #YconCervezaEsMejor  — V5
App Streamlit, SQLite local, sin APIs de pago.
Ejecutar: streamlit run app.py
"""
import os
import urllib.parse
import streamlit as st

import db

# ---------------------------------------------------------------
# CONFIG BASE
# ---------------------------------------------------------------
st.set_page_config(
    page_title="🍿 Que coño ver? 🍺",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
LOGO_PATH = os.path.join(ASSETS, "logo.png")
COACH_PATH = os.path.join(ASSETS, "coach_birra.jpg")
RB_LOGO_PATH = os.path.join(ASSETS, "rockandbirra_logo.jpg")

BIRRA_EMOJI = "🍺"
CAFE_EMOJI = "☕"
ROCK_AND_BIRRA_URL = "https://rockandbirra.com/"


def escala_birras(n) -> str:
    if n is None:
        return "⏳ Por ver"
    if n <= 0:
        return f"{CAFE_EMOJI} (0 birras — un café)"
    return BIRRA_EMOJI * n + f"  ({n}/6)"


# ---------------------------------------------------------------
# CSS ESTILO NES (retro 8-bit)
# ---------------------------------------------------------------
NES_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"]  {
    font-family: 'Press Start 2P', monospace !important;
}

.stApp {
    background: repeating-linear-gradient(
        45deg, #0c0c14, #0c0c14 10px, #11112050 10px, #11112050 20px
    ), #0c0c14;
    color: #f4f4f4;
}

.nes-title {
    background: #1a1a2e;
    border: 6px solid #ff3c96;
    box-shadow: 0 0 0 4px #0c0c14, 0 0 0 8px #56e2ff, 6px 6px 0px #000;
    padding: 18px;
    text-align: center;
    margin-bottom: 18px;
}
.nes-title h1 {
    font-size: 22px;
    color: #ffd640;
    text-shadow: 3px 3px 0 #000;
    margin: 0;
    line-height: 1.6;
}
.nes-title p {
    color: #56e2ff;
    font-size: 11px;
    margin-top: 8px;
}

.nes-box {
    background: #16213e;
    border: 4px solid #ffd640;
    box-shadow: 4px 4px 0px #000;
    padding: 14px;
    margin-bottom: 14px;
}
.nes-box h3 {
    color: #56e2ff;
    font-size: 13px;
    border-bottom: 2px dashed #ff3c96;
    padding-bottom: 6px;
}

.rank-card {
    background: #0f3460;
    border: 3px solid #ffd640;
    box-shadow: 3px 3px 0px #000;
    padding: 10px 14px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}
.rank-card .titulo-txt { font-size: 12px; color: #f4f4f4; }
.rank-card .birras-txt { font-size: 14px; color: #ffd640; }
.rank-pos {
    display:inline-block;
    background:#ff3c96;
    color:#0c0c14;
    padding: 2px 8px;
    margin-right: 8px;
    font-size: 11px;
}

.notif-card {
    background: #2b1b3d;
    border: 3px solid #56e2ff;
    box-shadow: 3px 3px 0px #000;
    padding: 8px 12px;
    margin-bottom: 8px;
    font-size: 11px;
}

.comment-card {
    background: #0f3460;
    border-left: 4px solid #ff3c96;
    padding: 8px 12px;
    margin-bottom: 8px;
    font-size: 11px;
}

div.stButton > button, .stDownloadButton>button, .stLinkButton>a {
    font-family: 'Press Start 2P', monospace !important;
    background: #ff3c96 !important;
    color: #0c0c14 !important;
    border: 3px solid #0c0c14 !important;
    box-shadow: 3px 3px 0px #000 !important;
    font-size: 10px !important;
    border-radius: 0px !important;
}
div.stButton > button:hover { background: #56e2ff !important; }

section[data-testid="stSidebar"] {
    background: #1a1a2e;
    border-right: 6px solid #ff3c96;
}
.menu-flag {
    text-align:center;
    background:#ffd640;
    color:#0c0c14;
    padding:6px;
    font-size:12px;
    margin-bottom:10px;
    border: 3px solid #0c0c14;
}

hr { border-top: 3px dashed #56e2ff; }

input, textarea, select {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 11px !important;
}

.badge-pendiente {
    background:#ff3c96; color:#0c0c14; padding:2px 6px; font-size:10px;
}
</style>
"""
st.markdown(NES_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------
# LOGIN: usuario + PIN de 4 dígitos (registro / ingreso)
# ---------------------------------------------------------------
if "username" not in st.session_state:
    st.session_state.username = None
    st.session_state.user_id = None

if not st.session_state.username:
    st.markdown(
        """
        <div class="nes-title">
            <h1>🍿 QUE COÑO VER? 🍺</h1>
            <p>#YconCervezaEsMejor — PRESS START</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        if os.path.exists(COACH_PATH):
            st.image(COACH_PATH, caption="Tu coach de la birra 🍺", use_container_width=True)

        tab_entrar, tab_registro = st.tabs(["▶️ Entrar", "🆕 Crear cuenta"])

        with tab_entrar:
            st.markdown('<div class="nes-box"><h3>👤 LOGIN</h3></div>', unsafe_allow_html=True)
            u = st.text_input("Usuario", key="login_user")
            p = st.text_input("PIN (4 dígitos)", key="login_pin", type="password", max_chars=4)
            if st.button("▶️ INSERT COIN (Entrar)"):
                if not u.strip() or not p.strip():
                    st.warning("Completa usuario y PIN.")
                elif not (p.isdigit() and len(p) == 4):
                    st.warning("El PIN debe tener exactamente 4 dígitos.")
                else:
                    uid = db.verificar_login(u, p)
                    if uid:
                        st.session_state.username = u.strip()
                        st.session_state.user_id = uid
                        st.rerun()
                    else:
                        st.error("Usuario o PIN incorrectos.")

        with tab_registro:
            st.markdown('<div class="nes-box"><h3>🆕 CREAR CUENTA</h3></div>', unsafe_allow_html=True)
            nu = st.text_input("Elige un nombre de usuario", key="reg_user")
            np1 = st.text_input("Crea un PIN de 4 dígitos", key="reg_pin1", type="password", max_chars=4)
            np2 = st.text_input("Repite el PIN", key="reg_pin2", type="password", max_chars=4)
            if st.button("🎮 CREAR MI CUENTA"):
                if not nu.strip():
                    st.warning("Escribe un nombre de usuario.")
                elif not (np1.isdigit() and len(np1) == 4):
                    st.warning("El PIN debe ser de 4 dígitos numéricos.")
                elif np1 != np2:
                    st.warning("Los PIN no coinciden.")
                elif db.username_exists(nu):
                    st.error("Ese usuario ya existe. Ve a la pestaña 'Entrar'.")
                else:
                    uid = db.crear_usuario(nu, np1)
                    st.session_state.username = nu.strip()
                    st.session_state.user_id = uid
                    st.success("¡Cuenta creada! Entrando...")
                    st.rerun()
    st.stop()

user_id = st.session_state.user_id
username = st.session_state.username

# ---------------------------------------------------------------
# SIDEBAR / MENU
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="menu-flag">⬇️ MENU ⬇️</div>', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    st.markdown(f"**👤 {username}**")

    alertas_no_leidas = db.get_alertas(user_id, solo_no_leidas=True)
    badge = f" ({len(alertas_no_leidas)})" if alertas_no_leidas else ""

    pagina = st.radio(
        "Ir a:",
        [
            "🏆 Ranking",
            "🎬 Películas",
            "📺 Series",
            "📝 Por ver",
            "➕ Añadir",
            "👥 Amigos",
            "🎁 Recomendaciones",
            "📋 Listas compartidas",
            f"🔔 Notificaciones{badge}",
            "📊 Perfil",
            "📲 Compartir",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    if os.path.exists(RB_LOGO_PATH):
        st.image(RB_LOGO_PATH, use_container_width=True)
    st.link_button("🌐 Rock And Birra", ROCK_AND_BIRRA_URL, use_container_width=True)
    if st.button("🚪 Salir", use_container_width=True):
        st.session_state.username = None
        st.session_state.user_id = None
        st.rerun()

# ---------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------
st.markdown(
    """
    <div class="nes-title">
        <h1>🍿 QUE COÑO VER? 🍺</h1>
        <p>#YconCervezaEsMejor</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def render_ranking(rows, permitir_editar=True, es_watchlist=False):
    if not rows:
        st.info("Aún no hay títulos aquí.")
        return
    for pos, r in enumerate(rows, start=1):
        cols = st.columns([1, 4, 2, 2, 1, 1])
        with cols[0]:
            if not es_watchlist:
                st.markdown(f'<span class="rank-pos">#{pos}</span>', unsafe_allow_html=True)
        with cols[1]:
            icono = "🎬" if r["tipo"] == "pelicula" else "📺"
            st.markdown(f'<span class="titulo-txt">{icono} {r["titulo"]}</span>', unsafe_allow_html=True)
            if r["poster"] and os.path.exists(r["poster"]):
                st.image(r["poster"], width=90)
        with cols[2]:
            st.markdown(f'<span class="birras-txt">{escala_birras(r["birras"])}</span>', unsafe_allow_html=True)
        with cols[3]:
            if r["nota"]:
                st.caption(r["nota"])
        if permitir_editar:
            with cols[4]:
                if st.button("✏️", key=f"edit_{r['id']}"):
                    st.session_state[f"editing_{r['id']}"] = True
            with cols[5]:
                if st.button("🗑️", key=f"del_{r['id']}"):
                    db.delete_titulo(r["id"])
                    st.rerun()

        if st.session_state.get(f"editing_{r['id']}"):
            with st.form(key=f"form_edit_{r['id']}"):
                st.markdown("**✏️ Editar título**")
                nuevo_titulo = st.text_input("Título", value=r["titulo"])
                if es_watchlist:
                    ya_vista = st.checkbox("✅ Ya la vi (mover a mi ranking)")
                    nuevas_birras = st.slider("Calificación (6🍺 mejor → 0☕ peor)", 0, 6, 3) if ya_vista else None
                else:
                    nuevas_birras = st.slider(
                        "Calificación (6🍺 la mejor → 0☕ la peor)", 0, 6, r["birras"] or 3
                    )
                    ya_vista = False
                nueva_nota = st.text_area("Nota (opcional)", value=r["nota"] or "")
                guardar = st.form_submit_button("💾 Guardar cambios")
                cancelar = st.form_submit_button("❌ Cancelar")
                if guardar:
                    if es_watchlist and ya_vista:
                        db.update_titulo(r["id"], titulo=nuevo_titulo, birras=nuevas_birras, nota=nueva_nota, estado="vista")
                    else:
                        db.update_titulo(r["id"], titulo=nuevo_titulo, birras=nuevas_birras, nota=nueva_nota)
                    st.session_state[f"editing_{r['id']}"] = False
                    st.rerun()
                if cancelar:
                    st.session_state[f"editing_{r['id']}"] = False
                    st.rerun()


# ---------------------------------------------------------------
# PAGINAS
# ---------------------------------------------------------------
if pagina == "🏆 Ranking":
    st.markdown('<div class="nes-box"><h3>🏆 RANKING GENERAL (mayor a menor birras)</h3></div>', unsafe_allow_html=True)
    render_ranking(db.get_ranking(user_id))

    st.markdown('<div class="nes-box"><h3>👀 QUÉ ESTÁN MIRANDO TUS AMIGOS</h3></div>', unsafe_allow_html=True)
    actividad = db.actividad_amigos(user_id)
    if not actividad:
        st.info("Agrega amigos en '👥 Amigos' para ver su actividad aquí.")
    else:
        for a in actividad:
            icono = "🎬" if a["tipo"] == "pelicula" else "📺"
            st.markdown(
                f'<div class="rank-card"><span class="titulo-txt">{icono} <b>{a["username"]}</b> vio "{a["titulo"]}"</span>'
                f'<span class="birras-txt">{escala_birras(a["birras"])}</span></div>',
                unsafe_allow_html=True,
            )

elif pagina == "🎬 Películas":
    st.markdown('<div class="nes-box"><h3>🎬 MIS PELÍCULAS</h3></div>', unsafe_allow_html=True)
    render_ranking(db.get_ranking(user_id, tipo="pelicula"))

elif pagina == "📺 Series":
    st.markdown('<div class="nes-box"><h3>📺 MIS SERIES</h3></div>', unsafe_allow_html=True)
    render_ranking(db.get_ranking(user_id, tipo="serie"))

elif pagina == "📝 Por ver":
    st.markdown('<div class="nes-box"><h3>📝 MI LISTA POR VER (sin calificar todavía)</h3></div>', unsafe_allow_html=True)
    render_ranking(db.get_ranking(user_id, estado="por_ver"), es_watchlist=True)

elif pagina == "➕ Añadir":
    st.markdown('<div class="nes-box"><h3>➕ AÑADIR PELÍCULA O SERIE</h3></div>', unsafe_allow_html=True)
    with st.form("form_add", clear_on_submit=True):
        tipo = st.radio(
            "Tipo:", ["pelicula", "serie"],
            format_func=lambda x: "🎬 Película" if x == "pelicula" else "📺 Serie",
            horizontal=True,
        )
        estado = st.radio(
            "¿Ya la viste?",
            ["vista", "por_ver"],
            format_func=lambda x: "✅ Ya la vi (calificar ahora)" if x == "vista" else "⏳ La quiero ver (watchlist)",
            horizontal=True,
        )
        titulo = st.text_input("Título")
        birras = None
        if estado == "vista":
            birras = st.slider(
                "🍺 La Mejor: six pack de cerveza — califica de 6🍺 (mejor) a 0☕ (peor)", 0, 6, 3
            )
        nota = st.text_area("Nota / comentario (opcional)")
        poster_file = st.file_uploader(
            "📺 Portada opcional (imagen desde tu teléfono/computador)",
            type=["png", "jpg", "jpeg", "webp"],
        )
        enviar = st.form_submit_button("💾 Guardar en mi lista")
        if enviar:
            if not titulo.strip():
                st.warning("Escribe un título.")
            else:
                poster_path = None
                if poster_file is not None:
                    safe_name = f"{user_id}_{titulo.strip().replace(' ', '_')}_{poster_file.name}"
                    poster_path = os.path.join(db.POSTERS_DIR, safe_name)
                    with open(poster_path, "wb") as f:
                        f.write(poster_file.getbuffer())
                db.add_titulo(user_id, tipo, titulo, estado=estado, birras=birras, poster=poster_path, nota=nota)
                msg = escala_birras(birras) if estado == "vista" else "⏳ agregada a tu watchlist"
                st.success(f"'{titulo}' guardado — {msg} 🎉")

elif pagina == "👥 Amigos":
    st.markdown('<div class="nes-box"><h3>👥 SEGUIR AMIGOS</h3></div>', unsafe_allow_html=True)

    with st.form("form_add_friend", clear_on_submit=True):
        st.caption("Tu amigo debe tener una cuenta creada en esta app. Le llegará una solicitud para aceptar.")
        amigo = st.text_input("Nombre de usuario de tu amigo/a")
        add_f = st.form_submit_button("➕ Enviar solicitud de amistad")
        if add_f and amigo.strip():
            ok, msg = db.enviar_solicitud_amistad(user_id, amigo)
            (st.success if ok else st.warning)(msg)

    solicitudes = db.solicitudes_pendientes(user_id)
    if solicitudes:
        st.markdown('<div class="nes-box"><h3>📥 SOLICITUDES RECIBIDAS</h3></div>', unsafe_allow_html=True)
        for s in solicitudes:
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.markdown(f'<span class="titulo-txt">👤 {s["username"]}</span>', unsafe_allow_html=True)
            if c2.button("✅ Aceptar", key=f"acc_{s['id']}"):
                db.aceptar_solicitud(s["id"])
                st.rerun()
            if c3.button("❌ Rechazar", key=f"rej_{s['id']}"):
                db.rechazar_solicitud(s["id"])
                st.rerun()

    st.markdown('<div class="nes-box"><h3>🧑‍🤝‍🧑 MIS AMIGOS</h3></div>', unsafe_allow_html=True)
    amigos = db.list_friends(user_id)
    if not amigos:
        st.info("Aún no tienes amigos agregados.")
    for a in amigos:
        st.markdown(f'<div class="rank-card"><span class="titulo-txt">👤 {a}</span></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button(f"❤️ Ver compatibilidad con {a}", key=f"compat_{a}"):
                st.session_state["ver_compat"] = a
        with c2:
            if st.button(f"🗑️ Eliminar a {a}", key=f"rm_{a}"):
                db.remove_friend(user_id, a)
                st.rerun()

    if st.session_state.get("ver_compat"):
        a = st.session_state["ver_compat"]
        pct, coincidencias = db.compatibilidad(user_id, a)
        if pct is None:
            st.warning(f"{a} todavía no tiene una cuenta en esta app.")
        else:
            st.markdown(
                f'<div class="nes-box"><h3>❤️ COMPATIBILIDAD CON {a.upper()}: {pct}%</h3></div>',
                unsafe_allow_html=True,
            )
            if coincidencias:
                for t, mi_birra, su_birra in coincidencias:
                    st.markdown(
                        f'<div class="rank-card">'
                        f'<span class="titulo-txt">{t}</span>'
                        f'<span class="birras-txt">Tú: {mi_birra}🍺 · {a}: {su_birra}🍺</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("Todavía no tienen títulos en común calificados.")

elif pagina == "🎁 Recomendaciones":
    st.markdown('<div class="nes-box"><h3>🎁 ENVIAR RECOMENDACIÓN</h3></div>', unsafe_allow_html=True)
    amigos = db.list_friends(user_id)
    if not amigos:
        st.info("Agrega amigos primero en '👥 Amigos' para poder recomendarles algo.")
    else:
        with st.form("form_recomendar", clear_on_submit=True):
            destino = st.selectbox("¿A quién se lo recomiendas?", amigos)
            tipo_r = st.radio("Tipo:", ["pelicula", "serie"], format_func=lambda x: "🎬 Película" if x == "pelicula" else "📺 Serie", horizontal=True)
            titulo_r = st.text_input("Título a recomendar")
            mensaje_r = st.text_area("Mensaje (opcional)", placeholder="¡Tienes que verla, está buenísima!")
            enviar_r = st.form_submit_button("📤 Enviar recomendación")
            if enviar_r and titulo_r.strip():
                ok, msg = db.enviar_recomendacion(user_id, destino, tipo_r, titulo_r, mensaje_r)
                (st.success if ok else st.warning)(msg)

    st.markdown('<div class="nes-box"><h3>📥 RECOMENDACIONES RECIBIDAS</h3></div>', unsafe_allow_html=True)
    recibidas = db.recomendaciones_recibidas(user_id, estado="pendiente")
    if not recibidas:
        st.info("No tienes recomendaciones pendientes.")
    for r in recibidas:
        icono = "🎬" if r["tipo"] == "pelicula" else "📺"
        st.markdown(
            f'<div class="rank-card"><span class="titulo-txt">{icono} <b>{r["de_username"]}</b> te recomienda: {r["titulo"]}'
            + (f"<br><i>{r['mensaje']}</i>" if r["mensaje"] else "") + '</span></div>',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        if c1.button("✅ Aceptar (va a Por ver)", key=f"acc_rec_{r['id']}"):
            db.responder_recomendacion(r["id"], aceptar=True)
            st.rerun()
        if c2.button("❌ Rechazar", key=f"rej_rec_{r['id']}"):
            db.responder_recomendacion(r["id"], aceptar=False)
            st.rerun()

elif pagina == "📋 Listas compartidas":
    st.markdown('<div class="nes-box"><h3>📋 CREAR LISTA DE SEGUIMIENTO COMPARTIDA</h3></div>', unsafe_allow_html=True)
    amigos = db.list_friends(user_id)
    with st.form("form_crear_lista", clear_on_submit=True):
        nombre_lista = st.text_input("Nombre de la lista (ej: 'Maratón de terror con la banda')")
        miembros = st.multiselect("¿Con quién la compartes?", amigos) if amigos else []
        crear = st.form_submit_button("➕ Crear lista")
        if crear and nombre_lista.strip():
            db.crear_lista_compartida(nombre_lista, user_id, miembros)
            st.success("¡Lista creada!")
            st.rerun()

    st.markdown('<div class="nes-box"><h3>📋 MIS LISTAS COMPARTIDAS</h3></div>', unsafe_allow_html=True)
    listas = db.mis_listas_compartidas(user_id)
    if not listas:
        st.info("Aún no tienes listas compartidas.")
    for lst in listas:
        miembros_l = db.miembros_lista(lst["id"])
        st.markdown(
            f'<div class="nes-box"><h3>🎞️ {lst["nombre"]}</h3>'
            f'<p style="font-size:10px;color:#ffd640;">👥 {", ".join(miembros_l)}</p></div>',
            unsafe_allow_html=True,
        )
        with st.form(f"form_item_{lst['id']}", clear_on_submit=True):
            c1, c2 = st.columns([3, 1])
            titulo_item = c1.text_input("Añadir título a esta lista", key=f"titulo_item_{lst['id']}")
            tipo_item = c2.selectbox("Tipo", ["pelicula", "serie"], key=f"tipo_item_{lst['id']}", format_func=lambda x: "🎬" if x == "pelicula" else "📺")
            add_item = st.form_submit_button("➕ Añadir a la lista")
            if add_item and titulo_item.strip():
                db.add_item_lista(lst["id"], tipo_item, titulo_item, username)
                st.rerun()

        items = db.items_lista(lst["id"])
        for it in items:
            icono = "🎬" if it["tipo"] == "pelicula" else "📺"
            estado_txt = "✅ Vista" if it["hecha"] else "⏳ Pendiente"
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.markdown(
                f'<span class="titulo-txt">{icono} {it["titulo"]} <i>(añadida por {it["agregado_por"]})</i> — {estado_txt}</span>',
                unsafe_allow_html=True,
            )
            if not it["hecha"]:
                if c2.button("✅ Marcar vista", key=f"done_{it['id']}"):
                    db.marcar_item_lista(it["id"], True)
                    st.rerun()
            if c3.button("🗑️", key=f"delitem_{it['id']}"):
                db.delete_item_lista(it["id"])
                st.rerun()

elif pagina.startswith("🔔 Notificaciones"):
    st.markdown('<div class="nes-box"><h3>🔔 NOTIFICACIONES</h3></div>', unsafe_allow_html=True)
    st.caption(
        "Se actualizan cada vez que entras o navegas por la app (no hay 'push' en tiempo real "
        "sin servicios externos de pago, pero verás lo último apenas recargues esta página)."
    )
    if st.button("🔄 Actualizar y marcar como leídas"):
        db.marcar_alertas_leidas(user_id)
        st.rerun()
    alertas = db.get_alertas(user_id)
    if not alertas:
        st.info("No tienes notificaciones todavía. Cuando un amigo termine de ver algo, aparecerá aquí.")
    for al in alertas:
        marca = "🆕 " if not al["leida"] else ""
        st.markdown(f'<div class="notif-card">{marca}{al["mensaje"]}</div>', unsafe_allow_html=True)

elif pagina == "📊 Perfil":
    st.markdown('<div class="nes-box"><h3>📊 MI PERFIL</h3></div>', unsafe_allow_html=True)
    user_row = db.get_user_by_username(username)
    rows = db.get_ranking(user_id)
    total = len(rows)
    pelis = len([r for r in rows if r["tipo"] == "pelicula"])
    series = len([r for r in rows if r["tipo"] == "serie"])
    top = rows[0] if rows else None

    with st.form("form_bio"):
        bio = st.text_area("Mi bio / frase de cabecera", value=user_row["bio"] or "", placeholder="Ej: Fan del terror y las birras artesanales 🍺")
        if st.form_submit_button("💾 Guardar bio"):
            db.set_bio(user_id, bio)
            st.success("Bio actualizada.")
            st.rerun()

    c1, c2, c3 = st.columns(3)
    c1.metric("🎬 Películas", pelis)
    c2.metric("📺 Series", series)
    c3.metric("📚 Total", total)

    if top:
        st.markdown(
            f'<div class="rank-card"><span class="titulo-txt">🏆 Favorita: {top["titulo"]}</span>'
            f'<span class="birras-txt">{escala_birras(top["birras"])}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="nes-box"><h3>💬 COMENTARIOS EN MI PERFIL</h3></div>', unsafe_allow_html=True)
    comentarios = db.get_comentarios(user_id)
    if not comentarios:
        st.info("Aún no tienes comentarios. ¡Pide a tus amigos que visiten tu perfil!")
    for cmt in comentarios:
        st.markdown(f'<div class="comment-card"><b>{cmt["autor_username"]}:</b> {cmt["texto"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="nes-box"><h3>✍️ COMENTAR EN EL PERFIL DE UN AMIGO</h3></div>', unsafe_allow_html=True)
    amigos = db.list_friends(user_id)
    if amigos:
        with st.form("form_comentar_amigo", clear_on_submit=True):
            perfil_destino = st.selectbox("Perfil de:", amigos)
            texto_comentario = st.text_area("Tu comentario")
            if st.form_submit_button("💬 Publicar comentario") and texto_comentario.strip():
                db.add_comentario(perfil_destino, username, texto_comentario)
                st.success(f"Comentario publicado en el perfil de {perfil_destino}.")
    else:
        st.caption("Agrega amigos para poder comentar en sus perfiles.")

    st.markdown("#### 🔗 Compartir mi perfil")
    perfil_txt = (
        f"🍿 Perfil de {username} en 'Que coño ver? 🍺'\n"
        f"#YconCervezaEsMejor\n\n"
        f"🎬 Películas calificadas: {pelis}\n"
        f"📺 Series calificadas: {series}\n"
    )
    if top:
        perfil_txt += f"🏆 Favorita: {top['titulo']} — {escala_birras(top['birras'])}\n"
    st.text_area("Vista previa:", perfil_txt, height=140)
    wa_link = "https://wa.me/?text=" + urllib.parse.quote(perfil_txt)
    st.link_button("📲 Compartir perfil por WhatsApp", wa_link, use_container_width=True)

elif pagina == "📲 Compartir":
    st.markdown('<div class="nes-box"><h3>📲 COMPARTIR RANKING</h3></div>', unsafe_allow_html=True)
    rows = db.get_ranking(user_id)
    if not rows:
        st.info("Añade títulos primero para poder compartir tu ranking.")
    else:
        cantidad = st.slider("¿Cuántos títulos incluir en el ranking a compartir?", 1, min(len(rows), 20), min(5, len(rows)))
        lineas = [f"🍿 RANKING DE {username.upper()} 🍺", "#YconCervezaEsMejor", ""]
        medallas = ["🥇", "🥈", "🥉"]
        for i, r in enumerate(rows[:cantidad]):
            icono = "🎬" if r["tipo"] == "pelicula" else "📺"
            medalla = medallas[i] if i < 3 else f"{i+1}."
            birras_txt = (BIRRA_EMOJI * r["birras"]) if r["birras"] and r["birras"] > 0 else CAFE_EMOJI
            lineas.append(f"{medalla} {icono} {r['titulo']} — {birras_txt}")
        lineas.append("")
        lineas.append(f"🌐 {ROCK_AND_BIRRA_URL}")
        texto_compartir = "\n".join(lineas)

        st.text_area("Vista previa del mensaje:", texto_compartir, height=220)
        wa_link = "https://wa.me/?text=" + urllib.parse.quote(texto_compartir)
        st.link_button("📲 Enviar ranking por WhatsApp", wa_link, use_container_width=True)
        st.caption("Se abrirá WhatsApp con el mensaje listo — solo elige el contacto o grupo.")

st.markdown("---")
st.caption("🍿 Que coño ver? 🍺 #YconCervezaEsMejor — V5 · Python + Streamlit + SQLite, sin servicios externos.")
