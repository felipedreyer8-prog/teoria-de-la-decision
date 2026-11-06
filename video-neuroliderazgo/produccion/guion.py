"""Guion del video 'Neuroliderazgo en el ámbito laboral' (5:00).

Los tiempos de cada escena son los del prompt escalados de 3:00 a 5:00 (x 5/3).
Cada 'cue' es un audio independiente; 'text' es exactamente lo que se dice
(nunca nombres de personajes ni indicaciones visuales).
"""

ESCALA = 5 / 3
ESCENAS = [  # (id, inicio original, fin original) en segundos
    ("E1", 0, 20), ("E2", 20, 50), ("E3", 50, 85),
    ("E4", 85, 130), ("E5", 130, 160), ("E6", 160, 180),
]

VOCES = {
    "narrador": "n0bF9TsFNliKzI7wyJ2H",  # Carlos - Argentinian Narrator
    "jefe": "jbWMqMKDKL7X0v1DXTHH",      # Franco - Confident | Argentina
    "lucia": "p7AwDmKvTdoHTBuueGvP",     # Malena - Conversacional (rioplatense)
}

# tts: texto que se manda a la voz (puede llevar etiquetas de tono entre corchetes
# que no se pronuncian); text: lo que se ve en el subtítulo.
CUES = [
    # ESCENA 1
    dict(id="N1a", esc="E1", voz="narrador", text="Una entrega contiene un error. El jefe debe intervenir."),
    dict(id="N1b", esc="E1", voz="narrador", text="Pero la forma de hacerlo puede influir en la atención, las emociones y las decisiones del equipo."),
    dict(id="N1c", esc="E1", voz="narrador", text="El neuroliderazgo incorpora conocimientos de las neurociencias para comprender estas situaciones y mejorar la conducción de personas."),
    # ESCENA 2
    dict(id="J1", esc="E2", voz="jefe", tts="[annoyed] Lucía, esto está mal otra vez. ¿Cómo no te diste cuenta? Corregilo ya.",
         text="Lucía, esto está mal otra vez. ¿Cómo no te diste cuenta? Corregilo ya."),
    dict(id="L1", esc="E2", voz="lucia", tts="[hesitant] Usé los datos que recibimos ayer. ¿Cambió algo?",
         text="Usé los datos que recibimos ayer. ¿Cambió algo?"),
    dict(id="J2", esc="E2", voz="jefe", tts="[impatient] No tengo tiempo para explicaciones. Hacelo como te digo y, desde ahora, consultame todo.",
         text="No tengo tiempo para explicaciones. Hacelo como te digo y, desde ahora, consultame todo."),
    dict(id="N2a", esc="E2", voz="narrador", text="La conversación se centra en la culpa."),
    dict(id="N2b", esc="E2", voz="narrador", text="Lucía puede concentrarse en proteger su imagen, en lugar de analizar el problema."),
    dict(id="N2c", esc="E2", voz="narrador", text="Además, no sabe qué debe corregir ni con qué criterio."),
    # ESCENA 3
    dict(id="N3a", esc="E3", voz="narrador", tts="El modelo Scarf, propuesto por David Rock, identifica cinco dimensiones que pueden experimentarse como amenaza o recompensa en las interacciones sociales.",
         text="El modelo SCARF, propuesto por David Rock, identifica cinco dimensiones que pueden experimentarse como amenaza o recompensa en las interacciones sociales."),
    dict(id="N3b", esc="E3", voz="narrador", text="El estatus se relaciona con la posición que percibimos frente a los demás."),
    dict(id="N3c", esc="E3", voz="narrador", text="La certidumbre, con saber qué esperar."),
    dict(id="N3d", esc="E3", voz="narrador", text="La autonomía, con nuestro margen de decisión."),
    dict(id="N3e", esc="E3", voz="narrador", text="La relación, con la confianza y la pertenencia."),
    dict(id="N3f", esc="E3", voz="narrador", text="Y la equidad, con percibir un trato justo."),
    dict(id="N3g", esc="E3", voz="narrador", text="En esta situación, la exposición pública, las instrucciones confusas y el control excesivo pueden generar amenazas."),
    # ESCENA 4
    dict(id="J3", esc="E4", voz="jefe", tts="[calm] Lucía, revisemos este dato. No coincide con la última actualización. ¿Qué información recibiste?",
         text="Lucía, revisemos este dato. No coincide con la última actualización. ¿Qué información recibiste?"),
    dict(id="L2", esc="E4", voz="lucia", tts="[calm] La versión de ayer. No sabía que había una nueva.",
         text="La versión de ayer. No sabía que había una nueva."),
    dict(id="J4", esc="E4", voz="jefe", tts="[warm] Entiendo. Necesitamos actualizarlo antes de las cuatro. ¿Cómo proponés resolverlo?",
         text="Entiendo. Necesitamos actualizarlo antes de las cuatro. ¿Cómo proponés resolverlo?"),
    dict(id="L3", esc="E4", voz="lucia", tts="[confident] Puedo verificar la fuente y corregir la presentación. Después la revisamos juntos.",
         text="Puedo verificar la fuente y corregir la presentación. Después la revisamos juntos."),
    dict(id="J5", esc="E4", voz="jefe", tts="[warm] Perfecto. Voy a compartir la actualización con todo el equipo para que trabajemos con el mismo criterio.",
         text="Perfecto. Voy a compartir la actualización con todo el equipo para que trabajemos con el mismo criterio."),
    dict(id="N4a", esc="E4", voz="narrador", text="El error sigue siendo señalado, pero sin descalificar a la persona."),
    dict(id="N4b", esc="E4", voz="narrador", text="Hay un objetivo claro, espacio para proponer soluciones y criterios compartidos."),
    dict(id="N4c", esc="E4", voz="narrador", text="Esto puede favorecer la confianza, la cooperación y el aprendizaje."),
    # ESCENA 5
    dict(id="N5a", esc="E5", voz="narrador", text="Los líderes no deciden únicamente a partir de datos objetivos. También intervienen sus experiencias, percepciones y emociones."),
    dict(id="N5b", esc="E5", voz="narrador", text="La racionalidad limitada y los atajos mentales ayudan a comprender por qué podemos llegar a conclusiones apresuradas."),
    dict(id="N5c", esc="E5", voz="narrador", text="Antes de atribuir un error a la falta de compromiso, conviene revisar la información y escuchar."),
    dict(id="N5d", esc="E5", voz="narrador", text="Regular una emoción no significa esconderla: implica revisar cómo interpretamos una situación antes de reaccionar."),
    # ESCENA 6
    dict(id="N6a", esc="E6", voz="narrador", text="El neuroliderazgo propone comprender mejor a las personas para conducir equipos."),
    dict(id="N6b", esc="E6", voz="narrador", text="No ofrece recetas universales ni explica toda conducta por el cerebro: también importan el contexto y las relaciones laborales."),
    dict(id="N6c", esc="E6", voz="narrador", text="Su aplicación debe respetar la privacidad y la autonomía."),
    dict(id="N6d", esc="E6", voz="narrador", text="Liderar implica alcanzar resultados y generar condiciones para aprender y desarrollarse."),
]

def ventana(esc):
    for e, a, b in ESCENAS:
        if e == esc:
            return a * ESCALA, b * ESCALA
    raise KeyError(esc)

if __name__ == "__main__":
    import re
    total = 0
    for c in CUES:
        t = c.get("tts", c["text"])
        n = len(t)
        total += n
    print("cues:", len(CUES), "caracteres TTS:", total)
    for e, a, b in ESCENAS:
        s, f = ventana(e)
        words = sum(len(c["text"].split()) for c in CUES if c["esc"] == e)
        print(f"{e}: {s:6.1f}–{f:6.1f}s ({f-s:5.1f}s)  palabras {words:3d}  ~habla {words/2.4:5.1f}s")
