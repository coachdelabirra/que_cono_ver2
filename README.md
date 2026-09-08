# 🍿 Que coño ver? 🍺 — #YconCervezaEsMejor (V5)

App web hecha en **Python + Streamlit**, con base de datos **SQLite** local (sin APIs
de pago ni servicios externos obligatorios). Permite crear listas de películas/series,
calificarlas con una escala de "birras" (6🍺 = la mejor, 0☕ = la peor), llevar una
lista de "por ver", ranking automático, compartir por WhatsApp, seguir amigos,
comparar gustos, recibir/enviar recomendaciones, listas de seguimiento compartidas
y notificaciones cuando un amigo termina algo. Interfaz retro tipo cartucho de
**Nintendo NES** (fuente pixel "Press Start 2P", colores 8-bit, menú lateral
"⬇️ MENU ⬇️"), con login propio de **usuario + PIN de 4 dígitos**.

## 📦 Contenido del proyecto

```
que-cono-ver/
├── app.py                    # App principal de Streamlit (toda la interfaz)
├── db.py                     # Capa de datos SQLite (usuarios, títulos, amigos,
│                              #   comentarios, recomendaciones, listas, alertas)
├── make_logo.py               # Script que generó el logo pixel-art (no hace falta re-ejecutarlo)
├── requirements.txt           # Dependencias (streamlit, pillow)
├── .gitignore
├── assets/
│   ├── logo.png                 # Logo retro NES de "Que coño ver?"
│   ├── coach_birra.jpg          # Mascota "Coach de la birra" (pantalla de login)
│   └── rockandbirra_logo.jpg    # Logo oficial de Rock and Birra (marca del sponsor)
└── data/
    ├── quecono.db             # Se crea solo al ejecutar la app (no se sube a GitHub)
    └── posters/                # Portadas subidas por los usuarios (no se sube a GitHub)
```

## 🕹️ Funciones incluidas

### Cuentas y calificación
- 🔐 **Login propio**: cada usuario crea su cuenta con nombre de usuario y un
  **PIN de 4 dígitos** (se guarda con hash + salt, nunca en texto plano).
- 🎬 Añadir películas y 📺 series, marcándolas como **✅ ya vista** (con
  calificación) o **⏳ por ver** (watchlist, sin calificar todavía).
- 🍺 Escala de birras: 6🍺 la mejor → 0☕ ("un café") la peor.
- 🏆 Ranking automático (SQLite ordena de mayor a menor birras al vuelo).
- ✏️ Editar, 🗑️ eliminar, y mover un título de "por ver" a "vista" cuando lo
  terminas (calificándolo en ese momento).
- 📺 Portada opcional: subir una imagen desde el teléfono/computador.

### Social
- 👥 **Seguir amigos**: se envía una solicitud y el otro usuario la acepta o
  rechaza (como una red social real).
- 👀 **Actividad de amigos**: en el Ranking se ve qué están mirando tus amigos
  en tiempo real (se actualiza cada vez que recargas/navegas la app).
- ❤️ **Compatibilidad de gustos**: compara títulos en común y calcula un
  porcentaje según qué tan parecidas son sus calificaciones.
- 💬 **Comentarios en perfiles**: puedes dejar comentarios en el perfil de tus
  amigos y ellos en el tuyo.
- 🎁 **Recomendaciones**: envía un título a un amigo con un mensaje; él puede
  aceptarla (se agrega automáticamente a su lista "por ver") o rechazarla.
- 📋 **Listas de seguimiento compartidas**: crea una lista con nombre (ej.
  "Maratón de terror"), invita amigos, y todos pueden añadir títulos y
  marcarlos como vistos.
- 🔔 **Notificaciones**: cuando un amigo termina de ver algo (marca un título
  como "vista"), a todos sus amigos les llega una alerta en la campana 🔔.

### Compartir y marca
- 📊 Perfil con estadísticas, bio personalizable y botón de compartir.
- 📲 Compartir el ranking (con medallas y emojis de birra) directo a WhatsApp
  usando un enlace `wa.me` — se abre WhatsApp con el mensaje ya escrito.
- 🌐 Botón "Rock And Birra" con el logo oficial → enlaza a https://rockandbirra.com/
- Menú lateral estilo NES con la etiqueta "⬇️ Menu⬇️", y la mascota "Coach de la
  birra" en la pantalla de bienvenida.

> **Nota sobre "tiempo real"**: sin servicios externos de pago (websockets,
> push notifications) no es posible un empuje instantáneo al celular. Lo que
> sí hace la app: cada vez que abres o navegas la app, consulta la base de
> datos al instante y te muestra la actividad y notificaciones más recientes
> — que es como funcionan la mayoría de apps sociales "gratis para uso
> personal" hechas con Streamlit.

> **Nota sobre compartir "como imagen"**: WhatsApp no permite que una web
> envíe una imagen automáticamente sin que el usuario la elija a mano. Por eso
> se genera un **texto con emojis ya formateado** (ranking o perfil) y se abre
> WhatsApp listo para enviar — es el método 100% gratuito (la API oficial de
> WhatsApp Business requiere cuenta de empresa y no es gratuita).

## ▶️ Probarlo en tu computador (opcional, antes de subirlo)

```bash
cd que-cono-ver
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá en `http://localhost:8501`. Crea tu cuenta con usuario + PIN de 4
dígitos en la pestaña "🆕 Crear cuenta", y pide a tus amigos que hagan lo mismo
para poder seguirse entre ustedes.

---

## 🚀 PASOS EXACTOS: Subir a GitHub

1. Crea una cuenta en https://github.com si no tienes una.
2. Entra a https://github.com/new y crea un repositorio nuevo, por ejemplo:
   `que-cono-ver` (puede ser público o privado).
3. **No** marques "Add a README" (ya tienes uno en este ZIP).
4. En tu computador, dentro de la carpeta `que-cono-ver`, ejecuta:

```bash
git init
git add .
git commit -m "Version 5: login PIN, amigos, recomendaciones, listas compartidas"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/que-cono-ver.git
git push -u origin main
```

Reemplaza `TU_USUARIO` por tu usuario real de GitHub. Si te pide credenciales,
usa un **Personal Access Token** (GitHub ya no acepta contraseña normal por Git):
Settings → Developer settings → Personal access tokens → Generate new token.

---

## ☁️ PASOS EXACTOS: Publicar gratis en Streamlit Community Cloud

Streamlit Community Cloud es gratuito para proyectos personales y es la forma
más rápida de tener tu app en la nube sin servidores propios.

1. Ve a https://share.streamlit.io/ e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"New app"**.
3. Selecciona:
   - **Repository**: `TU_USUARIO/que-cono-ver`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Haz clic en **"Deploy"**. En 1-2 minutos tendrás una URL pública tipo:
   `https://que-cono-ver-tuusuario.streamlit.app`
5. Comparte esa URL con tus amigos — ya pueden usarla desde el navegador de su
   celular (se puede "Agregar a pantalla de inicio" en Android/iPhone para que
   se sienta como una app). Cada quien crea su propia cuenta con usuario + PIN.

### ⚠️ Importante sobre SQLite en la nube

Streamlit Community Cloud reinicia el contenedor de vez en cuando (por
inactividad o actualizaciones), y en ese reinicio **se borra el archivo SQLite**
porque el disco no es permanente. Para **uso personal o con un grupo pequeño de
amigos** esto suele ser aceptable (los datos duran mientras la app esté
"despierta", que puede ser semanas). Si quieres que los datos, cuentas y PIN
**nunca se pierdan**, sigue la sección de Supabase abajo.

---

## 🗄️ OPCIONAL: Hacer los datos permanentes con Supabase (gratis)

Supabase ofrece una base de datos Postgres gratuita en la nube. Esto es
**opcional** — la app funciona sin esto, pero si quieres que las cuentas y el
ranking de tus amigos nunca se borren al reiniciar el servidor, sigue estos pasos:

1. Crea una cuenta gratis en https://supabase.com/ y un nuevo proyecto.
2. En el panel de Supabase, ve a **SQL Editor** y ejecuta (misma estructura
   que usa `db.py`, adaptada a Postgres):

```sql
create table usuarios (
  id bigint generated always as identity primary key,
  username text unique not null,
  pin_hash text not null,
  pin_salt text not null,
  bio text default '',
  creado timestamptz default now()
);

create table titulos (
  id bigint generated always as identity primary key,
  usuario_id bigint references usuarios(id) on delete cascade,
  tipo text check (tipo in ('pelicula','serie')),
  titulo text not null,
  estado text not null default 'vista' check (estado in ('vista','por_ver')),
  birras int check (birras is null or birras between 0 and 6),
  poster text,
  nota text,
  fecha timestamptz default now()
);

create table amistades (
  id bigint generated always as identity primary key,
  de_usuario_id bigint references usuarios(id) on delete cascade,
  para_usuario_id bigint references usuarios(id) on delete cascade,
  estado text not null default 'pendiente' check (estado in ('pendiente','aceptada')),
  fecha timestamptz default now(),
  unique(de_usuario_id, para_usuario_id)
);

create table comentarios (
  id bigint generated always as identity primary key,
  perfil_usuario_id bigint references usuarios(id) on delete cascade,
  autor_username text not null,
  texto text not null,
  fecha timestamptz default now()
);

create table recomendaciones (
  id bigint generated always as identity primary key,
  de_usuario_id bigint references usuarios(id) on delete cascade,
  para_usuario_id bigint references usuarios(id) on delete cascade,
  tipo text check (tipo in ('pelicula','serie')),
  titulo text not null,
  mensaje text,
  estado text not null default 'pendiente' check (estado in ('pendiente','aceptada','rechazada')),
  fecha timestamptz default now()
);

create table listas_compartidas (
  id bigint generated always as identity primary key,
  nombre text not null,
  creador_id bigint references usuarios(id) on delete cascade,
  fecha timestamptz default now()
);

create table lista_miembros (
  id bigint generated always as identity primary key,
  lista_id bigint references listas_compartidas(id) on delete cascade,
  usuario_id bigint references usuarios(id) on delete cascade,
  unique(lista_id, usuario_id)
);

create table lista_items (
  id bigint generated always as identity primary key,
  lista_id bigint references listas_compartidas(id) on delete cascade,
  tipo text check (tipo in ('pelicula','serie')),
  titulo text not null,
  agregado_por text not null,
  hecha boolean not null default false,
  fecha timestamptz default now()
);

create table alertas (
  id bigint generated always as identity primary key,
  para_usuario_id bigint references usuarios(id) on delete cascade,
  mensaje text not null,
  leida boolean not null default false,
  fecha timestamptz default now()
);
```

3. Ve a **Project Settings → API** y copia la `Project URL` y la `anon public key`.
4. En tu proyecto local (o en Streamlit Cloud → "Settings" → "Secrets" de tu app),
   agrega un archivo `.streamlit/secrets.toml` con:

```toml
SUPABASE_URL = "https://TU-PROYECTO.supabase.co"
SUPABASE_KEY = "tu-anon-key-aqui"
```

5. Instala el cliente: agrega `supabase` a `requirements.txt`.
6. Reemplaza las funciones de `db.py` que usan `sqlite3` por llamadas al cliente
   `supabase-py` (`from supabase import create_client`), usando
   `st.secrets["SUPABASE_URL"]` y `st.secrets["SUPABASE_KEY"]`. La estructura de
   tablas de arriba ya coincide 1 a 1 con las funciones de `db.py`, así que solo
   hay que cambiar el "motor" de guardado, no la lógica de la app.
7. Vuelve a hacer `git push` — Streamlit Cloud redeploya automáticamente.

> Esta sección es opcional a propósito: el modo por defecto de la app es
> SQLite puro, sin depender de ningún servicio externo. Supabase queda
> documentado aquí solo como mejora futura si algún día quieres persistencia
> total entre reinicios del servidor gratuito.

---

## 🧭 Resumen rápido

| Paso | Dónde | Qué hacer |
|---|---|---|
| 1 | GitHub | Crear repo y subir el código (`git push`) |
| 2 | Streamlit Cloud | Conectar el repo y desplegar (`share.streamlit.io`) |
| 3 | (Opcional) Supabase | Crear tablas y guardar credenciales en `secrets.toml` para persistencia total |
| 4 | WhatsApp | Ya integrado: botones "Compartir" abren `wa.me` con el texto listo |
| 5 | Amigos | Cada uno crea su cuenta (usuario + PIN) y se agregan entre sí desde "👥 Amigos" |

¡Salud! 🍺 #YconCervezaEsMejor
