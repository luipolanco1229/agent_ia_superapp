import ollama 

def interpretar_mensaje(input):
    return ollama.chat(
        model='llama3:8b',
        messages=[
            {
                'role': 'system',
                'content': (
                    "Eres el Agente 1 (Interpretador). Recibes un JSON como texto con "
                    "origen, destino, presupuesto_usd, fecha_salida, fecha_regreso, intereses[]. "
                    "Devuelve SOLO un JSON con EXACTAMENTE estos campos:\n"
                    "{\n"
                    '  "origen": "<string>",\n'
                    '  "destino": "<string>",\n'
                    '  "presupuesto_usd": <number>,\n'
                    '  "fecha_salida": "<YYYY-MM-DD>",\n'
                    '  "fecha_regreso": "<YYYY-MM-DD>",\n'
                    '  "intereses": ["<string>"],\n'
                    '  "resumen_intencion": "<frase breve>"\n'
                    "}\n"
                    "Reglas:\n"
                    "- Si no hay origen, usa \"Bogotá\".\n"
                    "- Si no hay intereses, deja el array vacío [].\n"
                    "- No incluyas texto fuera del JSON."
                )
            },
            {'role': 'user', 'content': input}
        ]
    )
