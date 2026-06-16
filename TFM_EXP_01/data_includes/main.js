PennController.ResetPrefix(null)
,
DebugOff() // Uncomment this line only when you are 100% done designing your experiment
// Start with welcome screen, then present test trials in a random order,and show the final screen after sending the results
Sequence( "participants", "welcome" , "welcome2", randomize("experiment"), "send", "final")
,
Header( /* void */ )
,
// Welcome screen and logging user's ID
newTrial("participants",
    defaultText.center().print()
    ,
    newText("participants", "Antes de empezar, ¿nos cuentas un poco sobre ti?")
    ,
    newText("Nombre completo.")
    ,
    newTextInput("Name", "")
        .log()
        .lines(0)
        .center()
        .print()
    ,
    newText("Edad.")
    ,
    newTextInput("Age", "")
        .log()
        .lines(0)
        .center()
        .print()
    ,
    newText("Nivel de estudios.")
    ,
    newTextInput("Studies", "")
        .log()
        .lines(0)
        .center()
        .print()
    ,
    newText("Lengua materna.")
    ,
    newTextInput("Language", "")
        .log()
        .lines(0)
        .center()
        .print()
    ,
    newText("Otras lenguas que sepas hablar (si no sabes más, escribe 'no').")
    ,
    newTextInput("Other", "")
        .log()
        .lines(0)
        .center()
        .print()
    ,
    newText("De acuerdo con lo dispuesto en el artículo 5 de la Ley Orgánica 15/1999, de 13 de diciembre, de Protección de Datos de Carácter Personal, le informamos que sus datos pasan a formar parte del proyecto de trabajo de fin de máster, que tiene como finalidad la realización de un diseño experimental para la asignatura “Trabajo fin de máster”. Le comunicamos que puede ejercitar los derechos de acceso, rectificación, cancelación y oposición de sus datos remitiendo un escrito a jmunoz062@ikasle.ehu.es. Puede consultar el Reglamento de la UPV/EHU para la Protección de Datos de carácter Personal en las direcciones de Internet www.ehu.es/babestu.")
        .cssContainer({"font-size": "100%"}) // con esto podéis aumentar el tamaño de letra
        .center()
        .print()
    ,
    newButton("send","Enviar.")
        .print()
        .wait()
)
,
newTrial("welcome", 
    // We will print all Text elements, horizontally centered
    defaultText.center()
        .print()
        .cssContainer({"font-size": "100%"})
    ,
    newText("¡Hola!")
    ,
    newText("Para realizar este experimento, sitúate en una habitación tranquila donde puedas escuchar los audios que van a reproducirse. Recomendamos el uso de auriculares, así como una buena conexión a internet.")
    ,
    newText("Ajusta también el brillo de la pantalla a un nivel cómodo, y ponte las gafas o lentillas si usas.")
    ,
    newText("Dale al botón para continuar.")
    ,
    newButton("send","Continuar.")
        .print()
        .wait()
) 
,
 newTrial("welcome2",
     defaultText.center()
     .print()
     .cssContainer({"font-size": "100%"})
    ,
    newText("Te explicamos qué tienes que hacer. ")
        .center()
        .print()
    ,
    newText("En este experimento vas a escuchar una voz artificial, y tendrás cuatro (4) posibles respuestas. Cada opción presenta un significado, y has de elegir el que más se ajuste al audio según tu opinión.")
        .center()
        .print()
    ,
    newText("Puedes escuchar el audio dos (2) veces, y elegir la respuesta con el ratón o pulsando la pantalla si estás en un aparato móvil.")
        .center()
        .print()
    ,
    newText("Recuerda, <b>no lo pienses mucho</b> y elige la respuesta que te parezca relaciona mejor el audio y el significado.")
        .center()
        .print()
    ,
    newText("Es posible que repitas alguna respuesta, ¡así que no te preocupes!")
        .center()
        .print()
    ,
    newText("¿Empezamos? Dale al botón.")
    ,
    newButton("send","¡Vamos!")
        .print()
        .wait()
)
,
Template( "thesis_materials_table.csv" , 
    row => newTrial("experiment",
    newAudio("audio", row.AUDIO_MATERIAL)
        .play()
        .print()
        .log()
,
    newSelector("choice")
        .frame("dotted 2px purple")
        .log()
,
    defaultText
        .size(200,100)
        .selector("choice")
,
    newCanvas(75,200)
        .add( 150 , 75 , newText("a", row.CORRECT))
        .add( 400 , 75 , newText("b", row.INCORRECT01))
        .add( 150 , 200, newText("c", row.INCORRECT02))
        .add( 375 , 200 , newText("d", row.INCORRECT03))
        .print()
        .log()
,
    getSelector("choice")
        .add( getText("a") , getText("b") , getText("c") , getText("d") )
        .enable()
        .shuffle()
        .once()
        .wait()
        .log()
,
    newTimer(500)
        .start()
        .wait()
    )
	.log( "relation" , row.RELATION )
	.log( "ID item"	, row.ID )
	.log( "Expected", row.EXPECTED )
)
,
SendResults("send")
,
newTrial( "final",
    newText("Se acabó el experimento, ¡gracias por participar!")
        .print()
    ,
    newButton()
        .wait()
)