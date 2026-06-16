''''''
'''PREGUNTA 1: Con respecto al modelo de datos, la tabla respuestas guarda id_participante e id_item,
pero no hay claves foráneas reales hacia participantes y materiales.
¿Qué problemas puede generar eso y cómo rediseñarías el esquema para asegurar integridad?'''


'''Rediseño tablas'''
class Participante(db.Base):
    __tablename__ = 'participantes'
    #ya existentes

    # Relación 1:N --> un participante tiene muchas respuestas
    respuestas = relationship('Respuestas', back_populates='participante')

class Material(db.Base):
    __tablename__ = 'materiales'
    #ya existentes

    # Relación 1:N --> un material tiene muchas respuestas
    respuestas = relationship('Respuestas', back_populates='material')

class Respuestas(db.Base):
    __tablename__ = 'respuestas'
    id = Column(Integer, primary_key=True)
    #ya existentes

    # FK añadidas de las tablas materiales y participantes
    id_material = Column(Integer, ForeignKey('materiales.id'), nullable=False)
    id_participante = Column(Integer, ForeignKey('participantes.id'), nullable=False)

    # Relaciones inversas
    participante = relationship('Participante', back_populates='respuestas')
    material = relationship('Material', back_populates='respuestas')


''' PREGUNTA 2: Si mañana quisieras añadir más experimentos, limitar repeticiones, 
registrar tiempos de respuesta, exportar resultados y permitir análisis por grupos lingüísticos, 
¿cómo reorganizarías la aplicación y qué cambios harías en el modelo de datos?'''

'''Reorganización de datos para análisis por grupos lingüísticos'''
# modificamos la tabla 'lenguas' (models.py)
class Lengua (db.Base):
    __tablename__= 'lenguas'
    id = Column(Integer, primary_key=True) #identificador unico de cada lengua
    id_participante = Column(Integer, ForeignKey('participantes.id')) #identificador de participantes
    lengua = Column(String(50))
    tipo = Column(String(20)) # "materna" u "otra"

#modificamos la función crear (main.py)
def crear():
    try:
        # lineas nombre a nivel_estudios se mantienen

        lengua_materna = request.form["lengua_materna"]
        otras_lenguas = request.form.getlist("otras_lenguas")

        participante = Participante(
            nombre=nombre,
            apellidos=apellidos,
            edad=edad,
            nivel_estudios=nivel_estudios
        )

        db.session.add(participante)
        db.session.flush()  # necesitamos el ID

        # guardar lengua materna aparte y se añade a la clase
        lm = Lengua(
            participante_id=participante.id,
            lengua=lengua_materna,
            tipo="materna"
        )
        db.session.add(lm)

        # guardamos otras lenguas aparte y se añaden a la clase
        # se genera una línea por cada lengua tipo "otra"
        for lengua in otras_lenguas:
            otra = Lengua(
                participante_id=participante.id,
                lengua=lengua,
                tipo="otra"
            )
            db.session.add(otra)

        session["participante"] = participante.id
        db.session.commit()

        return redirect(url_for('presentacion_instrucciones'))

    except Exception as e:
        db.session.rollback()
        print(f"Error al crear participante: {e}")
        return "Error al guardar el participante", 500

'''Reorganización de HTML para limitar repeticiones y registrar tiempos de respuesta'''
#limitar repeticiones de audio (experimento.html)
<body>
#<!-- AUDIO -->
# añadimos id al audio para poder hacer seguimiento de reproducciones
# la primera reproducción es automática
<audio controls id="audioStimulus" autoplay>
    <source src="{{ url_for('static', filename='audio_files/' ~ item.audio_material) }}">
</audio>

#registro de tiempo de respuesta desde la reproducción automática
<form method="post" action="/respuesta">
    #añadimos input para tiempo de respuesta
    <input type="hidden" name="tiempo_respuesta" id="tiempo_respuesta">
...
</form>

#continuación de la limitación del número de reproducciones antes de cerrar el body
#usamos JavaScript
<script>
document.addEventListener("DOMContentLoaded", function() {

    let audio = document.getElementById("audioStimulus");
    let playCount = 0;
    let maxPlays = 3;

    #tiempo inicio
    let startTime = Date.now();

    #limitar reproducciones
    audio.addEventListener("play", function() {
        playCount++;

        if (!startTime) {
            startTime = Date.now();
        }

        if (playCount >= maxPlays) {
            audio.controls = false; #oculta controles
        }
    });

    #guardamos el tiempo de respuesta (reaction time)
    let botones = document.querySelectorAll("button[name='respuesta']");

    botones.forEach(btn => {
        btn.addEventListener("click", function() {
            let endTime = Date.now();
            let reactionTime = endTime - startTime;

            document.getElementById("tiempo_respuesta").value = reactionTime;
        });
    });
</script>

</body>

'''PREGUNTA 3: Ahora que la IA está tan a la orden del día, 
se te ocurre alguna funcionalidad de tu app en la que podría aplicarse?'''

