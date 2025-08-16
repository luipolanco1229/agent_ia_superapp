# agent_3.py
import ollama

def ejecutar_tareas(input: str):
    """
    Agente 3 (Ejecución simulada):
    - ENTRADA: JSON (como string) generado por el Agente 2 con:
        {
          "origen": "<string>",
          "destino": "<string>",
          "rango_fechas": {"salida":"<YYYY-MM-DD>","regreso":"<YYYY-MM-DD>"},
          "presupuesto_usd": <number>,
          "intereses": ["<string>"],
          "tareas": [
            {
              "item": "<nombre corto>",
              "categoria": "vuelo|hospedaje|transporte|actividad|seguro|otros",
              "descripcion": "<qué y por qué>",
              "estimado_usd": <number>,
              "palabras_clave": ["<tokens de búsqueda>"]
            }
          ]
        }

    - SALIDA: ÚNICO JSON (como texto) con EXACTAMENTE:
        {
          "destino": "<string>",
          "costo_total_estimado_usd": <number>,
          "tareas": [
            { "item": "<nombre>", "descripcion": "<detalle>", "estimado_usd": <number> }
          ],
          "enlaces_compra": [
            { "item": "<nombre>", "categoria": "<categoria>", "vendor_sugerido": "<string>", "url": "<url>", "motivo": "<texto breve>" }
          ]
        }

    Notas:
    - Los enlaces de compra NO van dentro de cada tarea; solo en el array raíz "enlaces_compra".
    - Puedes usar origen/rango_fechas/intereses para construir URLs, pero NO los incluyas en la salida final.
    """
    return ollama.chat(
        model="llama3:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres el Agente 3 (Ejecución simulada). Recibirás el JSON del Agente 2 con el plan.\n"
                    "Tu trabajo es devolver SOLO un JSON con EXACTAMENTE esta estructura:\n"
                    "{\n"
                    '  "destino": "<string>",\n'
                    '  "costo_total_estimado_usd": <number>,\n'
                    '  "tareas": [\n'
                    '    { "item": "<nombre>", "descripcion": "<detalle>", "estimado_usd": <number> }\n'
                    '  ],\n'
                    '  "enlaces_compra": [\n'
                    '    { "item": "<nombre>", "categoria": "<categoria>", "vendor_sugerido": "<string>", "url": "<url>", "motivo": "<texto breve>" }\n'
                    "  ]\n"
                    "}\n\n"
                    "REGLAS DE VALIDACIÓN Y CONSISTENCIA:\n"
                    "- NO incluyas 'enlaces_compra' dentro de los objetos de 'tareas'. TODOS los enlaces van SOLO en el array raíz 'enlaces_compra'.\n"
                    "- Cada objeto en 'enlaces_compra' debe mapearse a un 'item' existente en 'tareas' y referir su 'categoria'.\n"
                    "- Si alguna tarea no tiene 'estimado_usd', coloca un estimado razonable (entero) y úsalo en el total.\n"
                    "- Calcula 'costo_total_estimado_usd' como la suma EXACTA de los 'estimado_usd' de todas las tareas (redondea a entero si hace falta).\n"
                    "- NO inventes precios en tiempo real ni disponibilidad; son estimados.\n"
                    "- NUNCA incluyas texto fuera del JSON final.\n\n"
                    "ENTRADA Y CAMPOS DISPONIBLES (para construir enlaces):\n"
                    "- El JSON de entrada tiene: origen, destino, rango_fechas (salida, regreso), presupuesto_usd, intereses[], tareas[].\n"
                    "- Puedes usar origen/destino/fechas/intereses/palabras_clave para armar URLs; PERO esos campos NO deben aparecer en la salida final.\n\n"
                    "CONSTRUCCIÓN DE URLs (sin placeholders; usa valores reales del plan):\n"
                    "- Reemplaza espacios por '+'. Simplifica diacríticos (ej.: 'São Paulo' -> 'Sao+Paulo').\n"
                    "- Usa 'destino' y 'rango_fechas' (salida/regreso). Si existe 'origen', úsalo en vuelos; si no, usa 'Bogota'.\n"
                    "- Para ACTIVIDADES, incorpora términos de 'intereses' y/o 'palabras_clave' en la query cuando corresponda.\n\n"
                    "TEMPLATES SUGERIDOS (elige según categoria):\n"
                    "* Vuelos (si desconoces IATA): Google Search con origen, destino y fecha de salida:\n"
                    "  https://www.google.com/search?q=vuelos+<ORIGEN>+a+<DESTINO>+<YYYY-MM-DD>\n"
                    "* Hospedaje: Booking con destino y fechas:\n"
                    "  https://www.booking.com/searchresults.html?ss=<DESTINO>&checkin=<YYYY-MM-DD>&checkout=<YYYY-MM-DD>\n"
                    "* ACTIVIDADES (mínimo 2 enlaces por cada actividad):\n"
                    "  - GetYourGuide con destino, fechas e intereses:\n"
                    "    https://www.getyourguide.com/s/?q=<DESTINO>+<INTERES>&from=<YYYY-MM-DD>&to=<YYYY-MM-DD>\n"
                    "  - TripAdvisor (búsqueda general por destino/interés):\n"
                    "    https://www.tripadvisor.com/Search?q=<DESTINO>+<INTERES>\n"
                    "  (Si hay varios intereses, elige los más relevantes para cada actividad y genera ENLACES SEPARADOS.)\n"
                    "* Transporte local: Google Search:\n"
                    "  https://www.google.com/search?q=transporte+publico+<DESTINO>\n"
                    "* Seguro de viaje: Google Search:\n"
                    "  https://www.google.com/search?q=seguro+de+viaje+<DESTINO>\n\n"
                    "VENDORS SUGERIDOS POR CATEGORIA:\n"
                    "- vuelo -> 'Google' (o 'Skyscanner')\n"
                    "- hospedaje -> 'Booking'\n"
                    "- actividad -> 'GetYourGuide', 'TripAdvisor'\n"
                    "- transporte -> 'Google'\n"
                    "- seguro -> 'Google'\n\n"
                    "SALIDA ESTRICTA:\n"
                    "- Devuelve SOLO el JSON final. Nada de comentarios ni explicaciones fuera del JSON.\n"
                    "- 'enlaces_compra' debe contener, para cada actividad del plan, al menos dos objetos (uno para GetYourGuide y otro para TripAdvisor), con URLs utilizables.\n"
                )
            },
            {"role": "user", "content": input}
        ]
    )
