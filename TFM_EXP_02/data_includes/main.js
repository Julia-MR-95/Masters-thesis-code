PennController.ResetPrefix(null)
,
//DebugOff() // Uncomment this line only when you are 100% done designing your experiment
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
    newButton("send", "Continuar")
        .center()
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
    newText("Para realizar este experimento, sitúate en una habitación tranquila donde puedas escuchar los audios que van a reproducirse.")
    ,
    newText("Recomendamos el uso de auriculares, así como una buena conexión a internet.")
    ,
    newText("Ajusta también el brillo de la pantalla a un nivel cómodo, y ponte las gafas o lentillas si usas.")
    ,
    newText("Dale al botón para continuar.")
    ,
    newButton("send", "Continuar.")
        .center()
        .print()
        .wait()
)
,
 newTrial("welcome2",
     defaultText.center()
     .print()
     .cssContainer({"font-size": "100%"})
    ,
    newText("Te explicamos qué tienes que hacer.")
        .center()
        .print()
    ,
    newText("En este experimento vas a escuchar una palabra y tendrás dos (2) significados entre los que elegir.")
        .center()
        .print()
    ,
    newText("Puedes escuchar el audio dos (2) veces, y elegir la respuesta con el ratón o pulsando la pantalla.")
        .center()
        .print()
    ,
    newText("Recuerda, <b>no lo pienses mucho</b> y elige la respuesta que te parezca relaciona mejor el sonido y el significado.")
        .center()
        .print()
    ,
    newText("Las opciones se repiten, ¡así que no te preocupes!")
        .center()
        .print()
    ,
    newText("¿Empezamos? Dale al botón.")
    ,
    newButton("send","¡Vamos!")
        .print()
        .center()
        .wait()
)
,
Template( "thesis_materials02_table.csv" , row => 
    newTrial("experiment",
        newAudio("audio", row.AUDIO_MATERIAL)
            .play()
            .center()
            .print()
            .log()
,
    newCanvas("side-by-side", 450, 200)
        .add(100, 0, newText("a", row.CORRECT))
        .add(200, 0, newText("b", row.INCORRECT))
        .center()
        .print()
,
    newSelector("choice")
        .add( getText("a") , getText("b"))
        .log()
        .center()
        .once()
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