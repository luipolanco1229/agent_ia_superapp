import ollama 

def planificar_mensaje(input):
    return ollama.chat(
        model='llama3:8b',
        messages=[
            {
                'role': 'system',
                'content': (
                    "Eres el Agente 2 (Planificador). Recibes el JSON del Agente 1. "
                    "Devuelve SOLO un JSON con EXACTAMENTE esta estructura:\n"
                    "{\n"
                    '  "origen": "<string>",\n'
                    '  "destino": "<string>",\n'
                    '  "rango_fechas": {"salida":"<YYYY-MM-DD>","regreso":"<YYYY-MM-DD>"},\n'
                    '  "presupuesto_usd": <number>,\n'
                    '  "intereses": ["<string>"],\n'
                    '  "tareas": [\n'
                    '    {\n'
                    '      "item": "<nombre corto>",\n'
                    '      "categoria": "vuelo|hospedaje|transporte|actividad|seguro|otros",\n'
                    '      "descripcion": "<qué y por qué>",\n'
                    '      "estimado_usd": <number>,\n'
                    '      "palabras_clave": ["<tokens de búsqueda>"]\n'
                    '    }\n'
                    '  ]\n'
                    "}\n"
                    "Reglas:\n"
                    "- Usa los intereses para proponer actividades personalizadas (ej: si interesa gastronomía → tours de comida).\n"
                    "- Ajusta el plan al presupuesto.\n"
                    "- Incluye al menos vuelo, hospedaje, 3 actividades, transporte y seguro si el presupuesto lo permite.\n"
                    "- No incluyas texto fuera del JSON."
                )
            },
            {'role': 'user', 'content': input}
        ]
    )
