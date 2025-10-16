# ui/app.py
import base64, json, time, requests
import streamlit as st

import os
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="GameMatch+ • Recs de videojuegos", page_icon="🎮", layout="wide")

# -------- Session --------
for k, v in {
    "token": None, "user_id": None, "email": None, "nombre": None,
    "games_cache": {}
}.items():
    st.session_state.setdefault(k, v)

# -------- REST helpers --------
def api_get(path, params=None, auth=True):
    url = f"{BACKEND_URL}{path}"
    headers = {"Accept": "application/json"}
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return {} if not r.text else r.json()

def api_post(path, data=None, auth=True, as_form=False):
    url = f"{BACKEND_URL}{path}"
    headers = {"Content-Type": "application/x-www-form-urlencoded" if as_form else "application/json"}
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    r = requests.post(url, headers=headers, data=(data if as_form else json.dumps(data or {})), timeout=30)
    r.raise_for_status()
    return {} if not r.text else r.json()

def decode_jwt_payload(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {}
        pad = "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + pad).decode("utf-8"))
        return payload
    except Exception:
        return {}


def guard_logged():
    if not st.session_state.token or not st.session_state.user_id:
        st.warning("Inicia sesión para continuar.")
        st.stop()

def refresh_games_cache():
    try:
        games = api_get("/games")
        st.session_state.games_cache = {g["id"]: g for g in (games or [])}
    except requests.HTTPError:
        st.session_state.games_cache = {}

def get_game(gid: int):
    g = st.session_state.games_cache.get(gid)
    if g is None:
        refresh_games_cache()
        g = st.session_state.games_cache.get(gid, {"id": gid, "titulo": f"Juego #{gid}"})
    return g

# -------- CSS global --------
st.markdown("""
<style>
.gm-hero {background: linear-gradient(135deg, #7C4DFF33 0%, #00E5FF22 100%);
  border: 1px solid #ffffff0f; border-radius: 20px; padding: 22px 24px; margin-bottom: 14px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.25);}
.gm-chip {display:inline-block; padding:4px 10px; margin:2px 6px 2px 0; border-radius:999px;
  background:#26263a; border:1px solid #ffffff14; font-size:12px; color:#cfd2ff;}
.gm-card {border-radius:16px; border:1px solid #ffffff12; background: #141422; padding:16px; margin-bottom:12px;}
.gm-card:hover {border-color:#7C4DFFaa; transform: translateY(-1px); transition: all .2s ease;}
.gm-title {font-weight:700; font-size:16px;}
.gm-subtle {color:#9aa3b2; font-size:12px;}
button[kind="secondary"] {border-radius:12px !important;}
.css-1n76uvr, .stSelectbox, .stTextInput {margin-bottom: 0.5rem !important;}
</style>
""", unsafe_allow_html=True)

# -------- Sidebar --------
st.sidebar.title("GameMatch+ 🎮")
st.sidebar.caption("FastAPI + MySQL + Streamlit")

page = st.sidebar.radio("Navegación", ["Inicio", "Registro / Login", "Catálogo", "Recomendaciones", "Feedback", "Métricas", "Admin"], index=0)
st.sidebar.markdown("---")
if st.session_state.token:
    st.sidebar.success(f"Sesión: {st.session_state.email or 'usuario'} (id={st.session_state.user_id})")
    if st.sidebar.button("Cerrar sesión"):
        for k in ["token","user_id","email","nombre"]: st.session_state[k] = None
        st.rerun()
else:
    st.sidebar.info("No autenticado")

# -------- Header --------
def header(title:str, subtitle:str=""):
    with st.container():
        st.markdown(f"""
        <div class="gm-hero">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:16px;">
            <div>
              <div style="font-size:22px;font-weight:800;">{title}</div>
              <div class="gm-subtle">{subtitle}</div>
            </div>
            <div>
              <span class="gm-chip">Backend</span> <span class="gm-subtle">{BACKEND_URL}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# -------- Páginas --------
if page == "Inicio":
    header("GameMatch+", "Recomendaciones + agente ε-greedy con feedback en tiempo real")
    col1, col2, col3 = st.columns([1.6,1,1])
    with col1:
        st.write("**Qué puedes hacer aquí**")
        st.markdown("- Registro/Login con JWT\n- Cargar catálogo\n- Recomendaciones por contenido + **agente inteligente**\n- Feedback 👍/👎/⭐ que **ajusta ε**\n- Métricas por usuario")
    with col2:
        try:
            health = api_get("/health", auth=False); st.metric("Backend", health.get("status","ok"))
        except Exception: st.error("Backend no disponible")
    with col3:
        st.info("Consejo: usa *Admin → Seed* para poblar juegos rápido.")

elif page == "Registro / Login":
    header("Registro / Login")
    t1, t2 = st.tabs(["Registrarme", "Iniciar sesión"])

    with t1:
        with st.form("register_form"):
            c1, c2 = st.columns(2)
            with c1:
                nombre = st.text_input("Nombre", value="Gus")
                rol = st.selectbox("Rol", ["jugador","admin"], index=0)
            with c2:
                email = st.text_input("Email", value="gus@example.com")
                password = st.text_input("Password", type="password", value="123456")
            if st.form_submit_button("Crear cuenta ✨"):
                try:
                    res = api_post("/auth/register", {"nombre": nombre, "email": email, "password": password, "rol": rol}, auth=False)
                    st.success(f"Usuario creado: id={res['id']} • {res['email']}")
                    st.toast("Cuenta creada", icon="✅")
                except requests.HTTPError as e:
                    st.error(e.response.text if e.response is not None else str(e))

    with t2:
       with st.form("login_form"):
        c1, c2 = st.columns(2)
        with c1: email_l = st.text_input("Email", value="gus@example.com")
        with c2: password_l = st.text_input("Password", type="password", value="123456")
        if st.form_submit_button("Entrar 🚀"):
            try:
                res = api_post("/auth/login", data={"username": email_l, "password": password_l}, auth=False, as_form=True)
                st.session_state.token = res["access_token"]
                st.session_state.email = email_l
                
                # Decodificar JWT para obtener user_id
                payload = decode_jwt_payload(st.session_state.token)
                st.session_state.user_id = int(payload.get("sub", 1))  # ← AQUÍ EL CAMBIO
                
                st.success(f"Sesión OK • user_id={st.session_state.user_id}")
                st.toast("Sesión iniciada", icon="✅")
                time.sleep(0.5)
                st.rerun()
            except requests.HTTPError as e:
                st.error(e.response.text if e.response is not None else str(e))

elif page == "Catálogo":
    guard_logged(); header("Catálogo", "Crea y explora tu colección")
    refresh_games_cache()

    colf1, colf2, colf3 = st.columns([1.2,1,1])
    with colf1: q = st.text_input("Buscar por título")
    with colf2:
        all_genres = sorted({g for x in st.session_state.games_cache.values() for g in (x.get("generos","") or "").split(";") if g})
        sel_gen = st.multiselect("Géneros", options=all_genres)
    with colf3: st.write("")

    cA, cB = st.columns([2,1])
    with cA:
        if not st.session_state.games_cache:
            st.info("No hay juegos. Usa **Admin → Seed** para cargar ejemplos.")
        else:
            filtered = list(st.session_state.games_cache.values())
            if q: filtered = [g for g in filtered if q.lower() in (g.get("titulo","").lower())]
            if sel_gen: filtered = [g for g in filtered if any(sg in (g.get("generos","")) for sg in sel_gen)]

            for g in filtered:
                st.markdown('<div class="gm-card">', unsafe_allow_html=True)
                top = st.columns([7,3])
                with top[0]:
                    st.markdown(f'<div class="gm-title">{g["titulo"]}</div>', unsafe_allow_html=True)
                    gens = g.get("generos","").split(";") if g.get("generos") else []
                    if gens: st.markdown("".join([f'<span class="gm-chip">{x}</span>' for x in gens]), unsafe_allow_html=True)
                    st.caption(f'Plataforma: {g.get("plataforma","PC")} • ID: {g["id"]}')
                with top[1]:
                    st.markdown('<div class="gm-subtle">Acciones</div>', unsafe_allow_html=True)
                    if st.button("👍 Like", key=f"like_cat_{g['id']}", use_container_width=True):
                        try:
                            api_post(f"/users/{st.session_state.user_id}/feedback", {"juego_id": g["id"], "liked": True, "rating": 5})
                            st.toast("¡Gracias por el like!", icon="👍")
                        except requests.HTTPError as e:
                            st.error(e.response.text if e.response is not None else str(e))
                st.markdown('</div>', unsafe_allow_html=True)

    with cB:
        st.subheader("Crear juego")
        with st.form("create_game_form"):
            titulo = st.text_input("Título")
            generos = st.text_input("Géneros (separados por ;)")
            tags = st.text_input("Tags (separados por ;)")
            plataforma = st.text_input("Plataforma", value="PC")
            if st.form_submit_button("Crear 🎮"):
                try:
                    new_g = api_post("/games", {"titulo": titulo, "generos": generos, "tags": tags, "plataforma": plataforma})
                    st.success(f"Creado: [{new_g['id']}] {new_g['titulo']}"); st.toast("Juego creado", icon="✅")
                    time.sleep(0.4); refresh_games_cache(); st.rerun()
                except requests.HTTPError as e:
                    st.error(e.response.text if e.response is not None else str(e))

elif page == "Recomendaciones":
    guard_logged(); header("Recomendaciones", "Mezcla de explotación + exploración (ε-greedy)")

    # ε actual
    eps = None
    try:
        state = api_get(f"/agent/{st.session_state.user_id}/state")
        eps = state.get("epsilon", None)
    except Exception:
        pass
    m1, m2 = st.columns([1,1])
    with m1:
        if eps is not None: st.metric("ε actual (agente)", f"{eps:.4f}")
        else: st.caption("Consejo: envía feedback para que el agente empiece a aprender.")
    with m2:
        use_agent = st.toggle("Usar agente inteligente (ε-greedy)", value=True)

    top = st.slider("¿Cuántas recomendaciones quieres?", 1, 20, 6)
    alpha = st.slider("Peso del contenido (α)", 0.0, 1.0, 0.70, 0.05, help="α=1 solo contenido; α=0 solo horas Steam")

    refresh_games_cache()

    with st.spinner("Calculando recomendaciones…"):
        try:
            if use_agent:
                recs = api_get(
                    f"/agent/{st.session_state.user_id}/recommendations",
                    params={"limit": top, "agent_mode": True, "alpha": alpha}
                )
                items = [{"game": get_game(r["id"]), "score": r.get("score", 0)} for r in recs]
            else:
                recs = api_get(
                    f"/users/{st.session_state.user_id}/recommendations",
                    params={"top": top, "alpha": alpha}
                )
                items = [{
                    "game": {"id": r["id"], "titulo": r["titulo"], "generos": r.get("generos",""),
                             "tags": r.get("tags",""), "plataforma": r.get("plataforma","PC")},
                    "score": r.get("probabilidad", 0)
                } for r in recs]
        except requests.HTTPError as e:
            st.error(e.response.text if e.response is not None else str(e))
            items = []

    if not items:
        st.info("Aún no hay suficientes señales. Ve a **Feedback** o da likes en el catálogo.")
    else:
        for i in range(0, len(items), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i+j >= len(items): break
                it = items[i+j]; g = it["game"]; score = it["score"]
                with col:
                    st.markdown('<div class="gm-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="gm-title">{g.get("titulo","Juego")}</div>', unsafe_allow_html=True)
                    st.caption(f'ID: {g.get("id")} • Score: {score:.3f}')
                    if g.get("generos"):
                        st.markdown("".join([f'<span class="gm-chip">{x}</span>' for x in g["generos"].split(";") if x]), unsafe_allow_html=True)
                    if g.get("tags"):
                        st.markdown("".join([f'<span class="gm-chip" style="background:#20302a">{x}</span>' for x in g["tags"].split(";") if x]), unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([1,1,2.2])
                    with c1:
                        if st.button("👍", key=f"like_rec_{g['id']}"):
                            try:
                                res = api_post(f"/agent/{st.session_state.user_id}/feedback", {"game_id": g["id"], "like": True, "rating": 5})
                                if "epsilon" in res: st.toast(f"¡Gracias! ε → {res['epsilon']:.4f}", icon="✅"); st.rerun()
                            except requests.HTTPError as e:
                                st.error(e.response.text if e.response is not None else str(e))
                    with c2:
                        if st.button("👎", key=f"dislike_rec_{g['id']}"):
                            try:
                                res = api_post(f"/agent/{st.session_state.user_id}/feedback", {"game_id": g["id"], "like": False, "rating": 1})
                                if "epsilon" in res: st.toast(f"Anotado. ε → {res['epsilon']:.4f}", icon="⚙️"); st.rerun()
                            except requests.HTTPError as e:
                                st.error(e.response.text if e.response is not None else str(e))
                    with c3: st.caption("Dale feedback para afinar el agente.")
                    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Feedback":
    guard_logged(); header("Feedback", "Registra tus gustos; el agente aprende")
    refresh_games_cache()
    if not st.session_state.games_cache:
        st.info("No hay juegos. Ve a **Admin → Seed**.")
    else:
        options = {f"[{g['id']}] {g['titulo']}": g["id"] for g in st.session_state.games_cache.values()}
        choice = st.selectbox("Juego", list(options.keys()))
        juego_id = options[choice]
        liked = st.toggle("Me gusta 👍", value=True)
        rating = st.slider("Rating", 1, 5, 5)
        if st.button("Enviar feedback ✉️"):
            try:
                res = api_post(f"/agent/{st.session_state.user_id}/feedback", {"game_id": juego_id, "like": liked, "rating": rating})
                if "epsilon" in res: st.success(f"¡Gracias! ε ahora = {res['epsilon']:.4f}"); st.toast("Feedback registrado", icon="✅")
            except requests.HTTPError as e:
                st.error(e.response.text if e.response is not None else str(e))

elif page == "Métricas":
    guard_logged(); header("Tus métricas", "Resumen de tu actividad")
    try:
        m = api_get(f"/users/{st.session_state.user_id}/metrics")
        c1, c2, c3 = st.columns(3)
        c1.metric("Interacciones", m.get("total", 0))
        c2.metric("Likes", m.get("likes", 0))
        c3.metric("Clicks", m.get("clicks", 0))
        st.caption("Detalle bruto"); st.json(m)
    except requests.HTTPError as e:
        st.error(e.response.text if e.response is not None else str(e))

elif page == "Admin":
    header("Admin / Demo", "Herramientas para pruebas")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Seed inicial (CSV)")
        st.write("Carga desde `data/games.csv` del backend.")
        if st.button("Ejecutar seed 📥"):
            try:
                res = api_post("/seed", {}, auth=False)
                st.success(f"Insertados: {res.get('added', 0)}")
                st.toast("Seed ejecutado", icon="✅")
                refresh_games_cache()
            except requests.HTTPError as e:
                st.error(e.response.text if e.response is not None else str(e))
    with c2:
        st.subheader("Estado del backend")
        try:
            health = api_get("/health", auth=False)
            st.success(health)
        except requests.HTTPError as e:
            st.error(e.response.text if e.response is not None else str(e))

    st.markdown("---")

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("RAWG: Sembrar catálogo")
        q = st.text_input("Buscar en RAWG", value="Zelda", key="rawg_query")
        ps = st.slider("Cantidad", 1, 30, 12, key="rawg_ps")
        if st.button("Sembrar desde RAWG", key="rawg_btn"):
            try:
                res = api_get("/integrations/rawg/seed",
                              params={"query": q, "page_size": ps},
                              auth=False)
                st.success(res)
                st.toast("RAWG seed OK", icon="✅")
                refresh_games_cache()
            except requests.HTTPError as e:
                st.error(e.response.text if e.response is not None else str(e))

    with c4:
        st.subheader("Steam: Sincronizar horas jugadas")
        steamid = st.text_input("steamid64 (público)", key="steamid")
        if st.button("Sync Steam para mi usuario", key="steam_btn"):
            if not st.session_state.user_id:
                st.warning("Inicia sesión primero")
            else:
                try:
                    res = api_get("/integrations/steam/sync",
                                  params={"user_id": st.session_state.user_id,
                                          "steamid": steamid},
                                  auth=False)
                    st.success(res)
                    st.toast("Steam sync OK", icon="🎮")
                except requests.HTTPError as e:
                    st.error(e.response.text if e.response is not None else str(e))
