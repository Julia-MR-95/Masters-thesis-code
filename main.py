from flask import Flask, render_template, request, redirect, url_for, session
from pyexpat import features

import db
import csv
import models
import random
from datetime import datetime

from models import Participante, Respuestas

'''Inicializamos Flask'''
app = Flask(__name__) # objeto/variable global = servidor web
# hace q el propio framework active un servidor web en el ordenador sin q hagamos nada
#running 127.0.0.1:50000 == localhost:5000 --> localhost == not online
app.secret_key = "clave_super_secreta"
#necesario para que funcione session más adelante

'''Cargamos el CSV una única vez'''
items = models.obtener_materiales()

# backend - python ->> ruta: /
    # no puede haber nada entre @app.route y def home()
    # index.html es la ruta raiz de 'home'
# frontend - html/css/js --> index.html y main.css (dentro de templates, static)
@app.route('/') # / = pagina de inicio, marca las rutas (un fichero html/pag web diferente)
def home(): #definimos su comportamiento a seguir
    print("Comprobación de que estoy en la función 'home'.")
    lenguas=models.obtener_lenguas() #creo variable c/Clase desde modelo y funcion
    return render_template("index.html", lenguas=lenguas) #otra variable mismo nombre del template

# (!!!) lo primero q hay q comprobar es q tenemos acceso a la información
#las funciones desencadenadas por una ruta tienen que retornar algo obligatoriamente
@app.route('/crear-participante', methods=["POST"]) #indicar cómo acepta la información
def crear():
    try:
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        edad = request.form["edad"]
        nivel_estudios = request.form["nivel_estudios"]
        lengua_materna = request.form["lengua_materna"]
        otras_lenguas = ';'.join(request.form.getlist("otras_lenguas"))
        # ';'.join transforma mi lista a una sola cadena cuyos elementos están separados por espacios
        # luego hacemos split con el ; para separar los idiomas

        print("=" * 50)
        print(f"Nombre {nombre}")
        print(f"Apellidos: {apellidos}")
        print(f"Edad: {edad}")
        print(f"Nivel de estudios: {nivel_estudios}")
        print(f"Lengua materna: '{lengua_materna}'")
        print(f"Otras lenguas: '{otras_lenguas}'")
        print("=" * 50)

        participante = Participante(nombre=nombre, apellidos=apellidos,
                                    edad=edad, nivel_estudios=nivel_estudios,
                                    lengua_materna=lengua_materna, otras_lenguas=otras_lenguas)
        db.session.add(participante)
        db.session.flush()  # Flush para obtener el ID
        session["participante"] = participante.id
        db.session.commit()  # Commit después de guardar el ID en session

        return redirect(url_for('presentacion_instrucciones')) #redirecciona a la función de instrucciones

    except Exception as e:
        db.session.rollback()  #Revertir si hay error
        print(f"Error al crear participante: {e}")
        return "Error al guardar el participante", 500


'''Primera página de instrucciones'''
@app.route('/presentacion')
def presentacion_instrucciones():
    return render_template("presentacion.html")

'''Segunda página de instrucciones.
Hay que cargar la randomización entre las instrucciones y el experimento, por ello se sitúa aquí'''
@app.route('/instrucciones')
def instrucciones():
    indices = list(range(len(items))) #creamos lista de índices de todos los items
    random.shuffle(indices) #se randomizan
    print(f"Id participante: '{session["participante"]}'")
    print(f"Indices: '{indices}'")
    print(f"Items: '{items}'" )
    participante = session["participante"]
    session["orden_items"] = indices #se guarda la lista en la sesión del participante
    return render_template("instrucciones.html")


'''Experimento'''
@app.route("/experimento/<int:i>") #los <> indican q recibe un parametro de tipo int que se guarda en la variable i
# /0 item 1, /5 item 4... int:i de principio a fin
def experimento(i):
    # Recuperamos la lista de índices aleatorios
    orden = session.get("orden_items")

    # Si por alguna razón no existe, volvemos a instrucciones
    if orden is None:
        return redirect(url_for("instrucciones"))

    # Si ya hemos mostrado todos los ítems, vamos a fin
    if i >= len(orden):
        return redirect("/fin")

    # Calculamos el índice real del ítem a mostrar
    indice_real = orden[i]
    print(f"Indice real: '{indice_real}'")
    print(f"Item Seleccionado: '{items[indice_real]}'")
    item_actual = items[indice_real]
    progress = int(((i + 1) / len(orden)) * 100)    #barra de progreso: cuántos items lleva (i) + 1 / longitud orden

    opciones = [f"{item_actual.opt_a},{item_actual.sign_a}", f"{item_actual.opt_b},{item_actual.sign_b}",
                f"{item_actual.opt_c},{item_actual.sign_c}", f"{item_actual.opt_d},{item_actual.sign_d}"]
    #para renderizar queremos pasar la opción y su significado asociado,
    #pasamos un array de 4 valores= opción + significado separado por coma
    #estamos pasando toda la info, para que solo se muestre la opt, vamos al html
    random.shuffle(opciones)

    # Pasamos ese ítem a la plantilla
    return render_template(
        "experimento.html",
        item=item_actual,
        opciones=opciones,
        index=i,
        progress=progress #barra de progreso
    )

'''Ruta que recibe las respuestas del experimento, se guardan en BBDD/CSV y pasa al siguiente item'''
@app.route("/respuesta", methods=["POST"])
def respuesta():
    try:
        id_item = request.form["id_item"]
        id_participante = session["participante"]
        sign_esp = request.form["sign_esp"]
        respuesta_usuario = request.form["respuesta"] #recibe la respuesta + significado, hay que hacer .split()
        respuesta_usuario_array = respuesta_usuario.split(",")  #separamos
        #columna ok si sign_esp == sign_resp
        ok = 0 #variable base (no coincide, ya es = 0)
        if sign_esp == respuesta_usuario_array[1]:
            ok = 1

        '''Creamos la clase Respuestas a partir de los datos recogidos para la BBDD'''
        nueva_respuesta = Respuestas(id_item=id_item, id_participante=id_participante,
                                     sign_esp=sign_esp,
                                     opt_resp=respuesta_usuario_array[0],
                                     sign_resp=respuesta_usuario_array[1],
                                     ok=ok)
        db.session.add(nueva_respuesta)
        db.session.commit()

        siguiente = int(request.form["index"]) + 1
        return redirect(url_for("experimento", i=siguiente))

    except Exception as e:
        db.session.rollback()  # Revertir si hay error
        print(f"Error al guardar respuesta: {e}")
        return "Error al guardar la respuesta", 500

@app.route("/fin")
def fin():
    return render_template("fin.html")


if __name__ == '__main__':
    db.Base.metadata.create_all(bind=db.engine) #creamos modelo de datos
    app.run(debug=True) # hace q al reiniciar el servidor/modifiquemos codigo,
                        # el servidor de F se reinicie solo