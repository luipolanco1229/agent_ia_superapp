import json
from datetime import date
import streamlit as st
from agent_1 import interpretar_mensaje
from agent_2 import planificar_mensaje
from agent_3 import ejecutar_tareas

st.set_page_config(page_title="Agentes de Viaje", page_icon="🧭", layout="centered")
st.title("🧭 Super App de Viajes")

with st.form("trip_form"):
    origen = st.text_input("Origen", placeholder="Bogotá")
    destino = st.text_input("Destino", placeholder="Barcelona")
    presupuesto = st.number_input("Presupuesto (USD)", min_value=0.0, step=50.0, value=800.0, format="%.2f")
    fecha_salida = st.date_input("Fecha de salida", value=date.today())
    fecha_regreso = st.date_input("Fecha de regreso", value=date.today())
    intereses = st.text_area("Intereses", placeholder="museos, gastronomía, naturaleza")
    submitted = st.form_submit_button("Enviar")

def build_payload(origen, destino, presupuesto, fecha_salida, fecha_regreso, intereses) -> str:
    """JSON inicial para el Agente 1."""
    return json.dumps({
        "origen": origen,
        "destino": destino,
        "presupuesto_usd": float(presupuesto),
        "fecha_salida": str(fecha_salida),
        "fecha_regreso": str(fecha_regreso),
        "intereses": [i.strip() for i in intereses.split(",") if i.strip()]
    }, ensure_ascii=False)


def get_content(resp) -> str:
    """Extrae texto del cliente de Ollama sin romper si cambia el formato."""
    try:
        return resp["message"]["content"]
    except Exception as e:
        return f"(Respuesta del agente no válida o agente sin configurar: {e})"

def call_agents(payload_str: str):
    with st.spinner("Procesando solicitud..."):
        # Agente 1 — Interpretador
        a1 = interpretar_mensaje(payload_str)
        resp1 = get_content(a1)
        st.subheader("🧠 Agente 1 — Interpretador (JSON)")
        st.code(resp1, language="json")

        # Agente 2 — Planificador (recibe salida del A1)
        a2 = planificar_mensaje(resp1)
        resp2 = get_content(a2)
        st.subheader("🗂️ Agente 2 — Plan (JSON)")
        st.code(resp2, language="json")

        # Agente 3 — Enlaces (recibe salida del A2)
        a3 = ejecutar_tareas(resp2)
        resp3 = get_content(a3)
        st.subheader("🔗 Agente 3 — Enlaces (JSON)")
        st.code(resp3, language="json")

    st.markdown("---")
    st.header("✅ Resumen Final")

    try:
        final_data = json.loads(resp3)
    except Exception:
        st.error("El Agente 3 no devolvió un JSON válido.")
        st.text(resp3)
        return

    st.success(f"Plan de viaje para **{final_data.get('destino', 'Destino desconocido')}**")

    if isinstance(final_data.get("tareas"), list) and final_data["tareas"]:
        st.subheader("🗂️ Planificación")
        for t in final_data["tareas"]:
            if not isinstance(t, dict):
                continue
            item = t.get("item", "")
            desc = t.get("descripcion", "")
            est = t.get("estimado_usd", "-")
            st.markdown(f"- **{item}** — {desc} (USD {est})")

    enlaces = []

    if isinstance(final_data.get("enlaces_compra"), list):
        enlaces.extend(final_data["enlaces_compra"])

    if isinstance(final_data.get("tareas"), list):
        for t in final_data["tareas"]:
            if isinstance(t, dict) and isinstance(t.get("enlaces_compra"), list):
                enlaces.extend(t["enlaces_compra"])

    vistos = set()
    enlaces_unicos = []
    for e in enlaces:
        if not isinstance(e, dict):
            continue
        url = (e.get("url") or "").strip()
        if url and url not in vistos:
            vistos.add(url)
            enlaces_unicos.append(e)

    st.subheader("🛒 Enlaces de compra / reserva")
    if not enlaces_unicos:
        st.info("Este plan no incluyó enlaces de compra. Ajusta el prompt del Agente 3 o vuelve a intentar.")
    else:
        for e in enlaces_unicos:
            item = e.get("item", "")
            cat  = e.get("categoria", "")
            vend = e.get("vendor_sugerido", "Vendor")
            url  = (e.get("url") or "").strip()
            mot  = e.get("motivo", "")
            if url.startswith("http"):
                st.markdown(f"- **{item}** ({cat}) — [{vend}]({url})  \n  _{mot}_")
            else:
                st.markdown(
                    f"- **{item}** ({cat}) — {vend}  \n"
                    f"  _{mot}_  \n"
                    f"  `URL inválida: {url}`"
                )

if submitted:
    if not destino.strip():
        st.warning("Por favor escribe un destino.")
    elif fecha_regreso < fecha_salida:
        st.warning("La fecha de regreso no puede ser anterior a la fecha de salida.")
    else:
        payload_str = build_payload(origen, destino, presupuesto, fecha_salida, fecha_regreso, intereses)
        call_agents(payload_str)
