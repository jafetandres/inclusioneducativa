import io
from django.contrib import messages
from django.shortcuts import render, redirect
from reportlab.lib.colors import Color, CMYKColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, ListFlowable, ListItem
from django.http import FileResponse
from datetime import datetime
from InclusionEducativa.Apps.automata.forms import TestLenguajeForm
from InclusionEducativa.Apps.automata.models import Canton

PAGE_WIDTH = A4[0]
PAGE_HEIGHT = A4[1]
styles = getSampleStyleSheet()
titulo = "Actividades"


def datosTest(request):
    if request.method == 'POST':
        if calcularEdad(request.POST['fechaNacimiento']) >= 2 and calcularEdad(request.POST['fechaNacimiento']) < 6 and \
                request.POST['discapacidad'] == 'autismo':
            request.session['fechaNacimiento'] = request.POST['fechaNacimiento']
            request.session['canton'] = request.POST['canton']
            request.session['genero'] = request.POST['genero']
            request.session['discapacidad'] = request.POST['discapacidad']
            return redirect('automata:test')
        else:
            messages.error(request, 'Lo sentimos la ficha evaluativa esta diseñada para niños de 2 a 5 años de edad')
    return render(request, 'automata/base.html')


def calcularEdad(fechaNacimiento):
    hoy = datetime.today()
    fechaNacimiento = datetime.strptime(str(fechaNacimiento), '%Y-%m-%d')
    dias = hoy - fechaNacimiento
    edad = dias.days / 365
    return edad


def test(request):
    actividades_alimentacion = []
    actividades_comprension = []
    actividades_expre_com = []
    actividades_fluidez = []
    actividades_voz = []
    # hoy = datetime.today()
    # fechaNacimiento = datetime.strptime(str(request.session.get('fechaNacimiento')), '%Y-%m-%d')
    # dias = hoy - fechaNacimiento
    # edad = dias.days / 365
    edad = calcularEdad(request.session.get('fechaNacimiento'))
    if request.method == 'POST':
        form_testLenguaje = TestLenguajeForm(request.POST)
        if form_testLenguaje.is_valid():
            canton = Canton()
            canton.nombre = request.session.get('canton')
            canton.save()
            testLenguaje = form_testLenguaje.save(commit=False)
            testLenguaje.canton = canton
            testLenguaje.genero = request.session.get('genero')
            testLenguaje.discapacidad = request.session.get('discapacidad')
            testLenguaje.fechaNacimiento = request.session.get('fechaNacimiento')
            testLenguaje.save()
            if request.POST.get('p1', False) == 'no':
                actividades_alimentacion.append(
                    'Servir los alimentos en porciones pequeñas cuando estos no son de agrado para su hijo/a '
                    'para incrementar paulatinamente la cantidad, siendo recomendable anticipar el menú del día '
                    '(sin embargo descartar con un especialista o pediatra si no existe alguna '
                    'condición médica o requerimiento de suplementos alimenticios antes de iniciar '
                    'este programa conductual)')
                actividades_alimentacion.append(
                    'Establecer rutinas de las actividades del día para regular a su hijo/a en el hábito de la '
                    'hora de comer')
                actividades_alimentacion.append(
                    'Implementar indicadores temporales para graduar el tiempo que el niño/a '
                    'debe terminar (reloj, cronómetro)')
                actividades_alimentacion.append(
                    'Presentar agendas/ calendarios visuales (fotos, gráficos, pictogramas) de la secuencia de '
                    'alimentos en el orden en que se servirá los alimentos ej. sopa + ensalada y pollo + '
                    'postre (este último puede ser utilizado como reforzador positivo)')
            if request.POST.get('p2', False) == 'no':
                actividades_alimentacion.append(
                    'Usar la participación parcial de los familiares al momento de utilizar los cubiertos '
                    '(ej. colocarse detrás del niño/a y ayudar con sus manos a utilizar los utensilios '
                    'sosteniendo las  manos de su hijo por la parte dorsal y realizar la actividad como '
                    'si  él/ella lo realizara, posteriormente disminuir este apoyo tocando su codo, hombro '
                    'e indicación verbal paulatinamente)')
                actividades_alimentacion.append(
                    'Enseñar en casa por medio de objetos reales y asociación de gráficos el uso correcto '
                    'de los utensilios para la alimentación (ej. utilizar el objeto real CUCHILLO y gráfico '
                    'SOPA , CARNE y asociar a qué elemento corresponde el utensilio)')
                actividades_alimentacion.append(
                    'Implementar indicadores temporales para graduar el tiempo que el niño/a '
                    'debe terminar (reloj, cronómetro)')
                actividades_alimentacion.append(
                    'Si el niño presenta conductas como lanzar los utensilios o rechazarlos, iniciar '
                    'el proceso por utensilios básicos (cuchara, vaso plato que sean de su agrado o q '
                    'el haya seleccionado en cuanto a colores o formas) y pictogramas de conducta, para '
                    'posteriormente incorporar otras opciones, no forzar el uso hasta que el niño/a tolere '
                    'el manejo de instrumentos básicos de alimentación.')
                actividades_alimentacion.append(
                    'Reforzar en casa con  ejercicios de motricidad fina para fomentar  la habilidad del '
                    'manejo de los utensilios')
                actividades_alimentacion.append(
                    'Motivar el uso de utensilios, por medio de la presentación repetitiva de '
                    'alimentos que requieran el manejo de los mismos.')
                actividades_alimentacion.append(
                    'Incorporar un mantel o individual con velcro con la forma de los utensilios '
                    'para que el niño/a aprenda la colocación correcta de los mismos')
            if request.POST.get('p3', False) == 'no':
                actividades_alimentacion.append(
                    'Presentar los alimentos sólidos en trozos pequeños cuando estos no son de agrado para '
                    'su hijo/a, para incrementar paulatinamente la cantidad (sin embargo descartar con un '
                    'especialista o pediatra si no existe alguna condición médica o requerimiento de suplementos'
                    ' alimenticios antes de iniciar este programa conductual)')
                actividades_alimentacion.append(
                    'Realizar ejercicios maxilares como abrir y cerrar la'
                    ' boca para estimular el proceso de masticación')
            if request.POST.get('p4', False) == 'no':
                actividades_alimentacion.append(
                    'Motivar a su hijo/a mediante tazas de su agrado(dibujos, colores) correspondientes a '
                    'su edad para la incorporación de bebidas no agradables para el niño/a')
                actividades_alimentacion.append(
                    'Cuando los líquidos que queremos incorporar no son de agrado para el niño iniciar con medidas pequeñas '
                    'para incrementar gradualmente con el tiempo ')
                actividades_alimentacion.append(
                    'Motivar al niño al terminar la ingesta por medio de reforzadores (ej. aplausos, '
                    'festejos verbales ¡Muy bien!)')
            if request.POST.get('p5', False) == 'no':
                actividades_alimentacion.append(
                    'Ejercitar los labios para mejorar la ingesta (uso de sorbetes, soplo, apretar los '
                    'labios, simular a enviar besos, etc.)')
                actividades_alimentacion.append(
                    'Si la retención o derrame de alimentos se debe a dificultades conductuales se recomienda '
                    'emplear pictogramas de conducta sobre las normas de alimentación')
                actividades_alimentacion.append(
                    'Descartar con un especialista si no existe alguna condición médica que impide el '
                    'control de los órganos de la boca')
            if request.POST.get('p6', False) == 'no':
                actividades_alimentacion.append(
                    'Presentar los alimentos en porciones pequeñas hasta incorporar la cantidad de los mismo, '
                    'en presentaciones agradables a la vista del niño/a y en utensilios q él o ella haya '
                    'seleccionado  ')
                actividades_alimentacion.append(
                    'Combinar alimentos que son de agrado con los que no lo son para motivar la '
                    'ingesta ej. Fruta que queremos incorporar: Fresa'
                    'Alimento de agrado: Yogurt')
                actividades_alimentacion.append(
                    'Alternar al momento de la comida entre alimentos de agrado y desagrado ej.'
                    'Alimento a incorporar: carne'
                    'Alimento de agrado: espagueti'
                    'Así, se dará un trozo de carne y dos porciones de espagueti después que haya probado '
                    'el alimento no deseado hasta ir incorporando gradualmente el alimento')
            if request.POST.get('p7', False) == 'no':
                actividades_comprension.append(
                    'Utilizar los objetos reales de lo que queremos enseñar, dándole el uso y la función '
                    'correcta siendo modelo para que nuestro hijo/a imite ej. pelota (hacerla rodar )'
                    'Peinilla (peinar un cabello)')
                actividades_comprension.append(
                    'Seleccionar los objetos que queremos enseñar, de preferencia objetos de uso diario y de '
                    'interés para el niño/a ')
                actividades_comprension.append(
                    'Reforzar las actividades con el objeto real y fotografías de la acción para que el niño/a '
                    'los asocie')
                actividades_comprension.append(
                    'Utilizar juguetes que generen la reacción causa-efecto ej. Woki toki, carros con rampas '
                    'de carrera, etc.')
                actividades_comprension.append(
                    'Dar el nombre de los objetos cuando se realiza una acción ej. al momento del lavado de'
                    'dientes dar el nombre al colocar la PASTA DENTAL, tomar el CEPILLO, etc.')
            if request.POST.get('p8', False) == 'no':
                actividades_comprension.append(
                    'Descartar con un especialista si no existe alguna condición médica como problemas '
                    'auditivos antes de iniciar este programa')
                actividades_comprension.append(
                    'Utilizar información clara evitando utilizar un lenguaje confuso o de doble sentido'
                    '(bromas, metáforas, etc.)')
                actividades_comprension.append(
                    'Presentar actividades de  interés para su hijo/a con el fin de establecer bases de  interacción')
                actividades_comprension.append(
                    'Hacer inicialmente todo de la mima forma (rutina), para posteriormente ir cambiando '
                    'o incorporando más actividades')
                actividades_comprension.append(
                    'Utilizar apoyo visual (tarjetas, fotos, etc.) para mejorar la comprensión cuando se da '
                    'una orden a realizar')
            if request.POST.get('p9', False) == 'no':
                actividades_comprension.append(
                    'Eliminar los ruidos externos o distracciones ')
                actividades_comprension.append(
                    'Utilizar un tono de voz normal, suave y relajado, siempre de frente, tocándole ocasionalmente ')
                actividades_comprension.append(
                    'Iniciar con actividades de juego de interacción como cosquillas, burbujas, etc. para mejorar  su atención')
                actividades_comprension.append(
                    'Reforzar ejercicios de contacto visual, sentándose frente al niño y colocando ocasionalmente '
                    'objetos y el material a la altura de los ojos mientras le damos indicaciones del mismo ')
                actividades_comprension.append(
                    'Utilizar indicaciones simples evitando el exceso de información que pueden crear confusión ej. '
                    'Toma la pelota')
            if request.POST.get('p10', False) == 'no':
                actividades_comprension.append(
                    'Preparar juguetes que sean del interés del niño/a para motivar el uso correcto de ellos, si no '
                    'los utiliza correctamente se sugiere se lo tome de las manos y enseñarle cómo usarlos')
                actividades_comprension.append(
                    'Enseñar la participación con la entrega de juguetes, mediante la indicación TOMA-DAME '
                    'entregándole el juguete al niño/a mientras se usa la palabra TOMA y tomarle del brazo '
                    'para que entregue el juguete, festejando como si él/ella lo hubiera entregado')
                actividades_comprension.append(
                    'Hazlo partícipe de actividades cotidianas del hogar de acuerdo a su edad '
                    '(ej. ayudar a colocar la mesa, etc.) ya que incrementará el vocabulario y '
                    'brindará más opciones a la hora de seleccionar sus preferencias y juguetes')
                actividades_comprension.append(
                    'Usar apoyos visuales (objeto/juguete) para que el niño/a seleccione con qué desea jugar ')
                actividades_comprension.append(
                    'Delimitar el espacio establecido para jugar (incorporar un espacio en casa que sea '
                    'sólo para esa actividad)')
            if request.POST.get('p11', False) == 'no':
                actividades_comprension.append(
                    'Brindar la orden de manera clara y concisa con la acción que queremos que realice'
                    ' en pasos de secuencia ej. Queremos que pinte todos los círculos de color amarillo '
                    'del libro, por lo tanto la secuencia sería 1. Toma la pintura amarilla 2. Pinta los '
                    'círculos, 3. Cierra el libro (pueden presentarse la secuencia con apoyo visual o de '
                    'forma verbal mientras realiza paso por paso)')
                actividades_comprension.append(
                    'Enseñar inicialmente a clasificar por similitudes ej. en una caja colocar fichas de '
                    'diferentes colores y en otra colocar envases para ordenar de esta manera podrá '
                    'emparejar cada ficha por su color ')
                actividades_comprension.append(
                    'Presentar objetos que varíen sólo en la noción que queremos enseñar y solicitar '
                    'al niño/a con la palabra que queremos que identifique ej. dos manzanas de la misma '
                    'forma y color que varíen solo en el tamaño, pedir al niño/a “Grande” para que lo '
                    'entregue, si no sabe que hacer ayudarle manipulando su mano para que entregue el'
                    ' objeto y festejar como si él/ella hubiera realizado la actividad')
                actividades_comprension.append(
                    'Utilizar material como plantillas con diferentes temáticas como animales, colores, '
                    'objetos, etc. para que el niño/a encierre y marque las categorías solicitadas')
                actividades_comprension.append(
                    'Iniciar el uso con material concreto (objetos) para posteriormente cambiarlos por '
                    'fotografías, gráficos /pictogramas')
            if request.POST.get('p12', False) == 'no':
                actividades_comprension.append(
                    'Utilizar las fotografías de los personajes del cuento, presentando con 2 – 3'
                    ' acciones para que el niño/a identifique o asocie en cuál participó el personajes  ')
                actividades_comprension.append(
                    'Realizar preguntas claves para que pueda identificar el cuento, iniciar con Qué es, y cuando '
                    'este sea adquirido continuar con Quién es, Qué hace?')
                actividades_comprension.append(
                    'Utilizar cuentos que contengan número limitado de gráficos y personajes, '
                    'no sobrecargados de estímulos')
                actividades_comprension.append(
                    'Utilizar objetos/gráficos que se encontraron y NO en el cuento para que el niño/a '
                    'seleccione cuales estuvieron presentes en la historia  ')
            if request.POST.get('p13', False) == 'no':
                actividades_comprension.append(
                    'Utilizar preguntas claras y cortas con un vocabulario sencillo si el niño/a tienen '
                    'un número limitado de palabras')
                actividades_comprension.append(
                    'Si el caso requiere apoyarse de material visual que acompañe la pregunta')
                actividades_comprension.append(
                    'Realizar preguntas cerradas para que el niño/a no pierda el hilo de la conversación')
            if request.POST.get('p14', False) == 'no':
                actividades_comprension.append(
                    'Estimular el reconocimiento de acciones por medio de la imitación, iniciando con la '
                    'imitación del padre a las acciones o juegos que realiza el niño/a para luego '
                    'motivarlo a que imite el del padre')
                actividades_comprension.append(
                    'Utilizar la palabra de la acción sin ningún otro componente para que lo señale en gráficos '
                    'o fotografías ej. Toca JUGANDO, Toca COMIENDO, etc.  ')
                actividades_comprension.append(
                    'Iniciar la identificación de acciones con verbos que sean de uso común para el'
                    'niño, ej. comer, dormir, etc. ')
            if request.POST.get('p15', False) == 'no':
                actividades_comprension.append(
                    'Utilizar objetos material concreto o fotografías para indicar el objeto o '
                    'persona que queremos que indique ')
                actividades_comprension.append(
                    'No sobre cargar el espacio donde colocaremos los materiales para la identificación de objetos')
                actividades_comprension.append(
                    'Iniciar con la identificación de objetos para posteriormente incorporar personas,'
                    ' acciones y lugares')
                actividades_comprension.append(
                    'Brindar oportunidades para la repetición del vocabulario aprendido')
            if request.POST.get('p16', False) == 'no':
                actividades_comprension.append(
                    'Brindar la orden con palabras clave ej . GUARDA, COME, etc.')
                actividades_comprension.append(
                    'Ayudar mediante la participación parcial de la actividad (usar la mano del'
                    ' padre como apoyo para que el niño/a pueda realizar la actividad como si '
                    'él/ella lo estuviera realizando), festejar el logro')
                actividades_comprension.append(
                    'Seleccionar anticipadamente los comandos que queremos que el niño/a aprenda '
                    'e ir incorporando nuevos y de mayor complejidad')
            if request.POST.get('p17', False) == 'no':
                actividades_comprension.append(
                    'Utilizar la imagen secuenciada (gráficos u objetos) de lo que queremos que el niño/a realice ')
                actividades_comprension.append(
                    'Solicitar la orden por pasos e ir incorporando las acciones mientras realiza '
                    'cada actividad, ej. Ve a tu habitación y trae tu mochila para ir a la escuela'
                    'Los pasos a seguir serían de manera secuenciada 1. Ve a tu habitación, cuando lo '
                    ' cumpla continuar, 2. Toma la mochila 3. Vamos a la escuela')
                actividades_comprension.append(
                    'Acompañar al niño en la orden indicada para recordarle paso a paso lo que tiene que hacer')
            if request.POST.get('p18', False) == 'no':
                actividades_comprension.append(
                    'Utilizar apoyos visuales (gráficos) con historias  para indicar las consecuencias de una acción')
                actividades_comprension.append(
                    'Incorporar actividades para ejercitar situaciones reales por medio de la asociación '
                    'de gráficos ej. Gráficos de un  niño comiendo muchos dulces y de niño con dolor de '
                    'estómago y muy feliz para que el niño lo identifique y clasifique')
            if request.POST.get('p19', False) == 'no':
                actividades_comprension.append(
                    'Iniciar con la anticipación de actividades, indicar al niño lo que sucederá ante '
                    'situaciones que se presenten en el hogar antes de que esta se presente, ya que '
                    'ayudará en el manejo de planificación y reconocimiento de eventos al niño/a')
                actividades_comprension.append(
                    'Reforzar el uso de objetos, vestimenta de acuerdo al clima, acciones, lugares, '
                    'etc., mediante la asociación y emparejamiento de láminas o gráficos para enseñar '
                    'la situación correcta y lógica ')
            if request.POST.get('p20', False) == 'no':
                actividades_expre_com.append(
                    'Prestar atención a las interacciones del niño/a, como tomar al padre de la mano '
                    'y guiarlo hacia el objeto que desea, utilizar tercera persona para indicar '
                    'la necesidad. Ej. “quiere galleta”')
                actividades_expre_com.append(
                    'Identificar el objeto o alimento de mayor preferencia para el niño colocarlo frente '
                    'a él/ella y provocar algún tipo de respuesta. Cuando su hijo/a realice algún gesto '
                    'indicando que lo quiere, entregárselo , darle el nombre y repetir la '
                    'actividad motivando al niño a producir la palabra o gesto ')
                actividades_expre_com.append(
                    'utilizar algún tipo de comunicador (tecnológico, gráfico) de apoyo para '
                    'la comprensión de solicitar necesidades y aumento de vocabulario')
                actividades_expre_com.append(
                    'Colocar el objeto de mayor preferencia para el niño fuera de su alcance '
                    'para que solicite lo que desea')
            if request.POST.get('p21', False) == 'no':
                actividades_expre_com.append(
                    'Dar el nombre de los objetos de interés para el niño de manera repetitiva '
                    'cada vez que esta se presente. ')
                actividades_expre_com.append(
                    'Provocar la respuesta del niño/a en situaciones de agrado para él/ella. Ej. Si '
                    'el niño se encuentra en un columpio mientras se lo balancea decir COLUMPIO, '
                    'cada vez que se realice la actividad, parar y esperar a ver la reacción del '
                    'niño para que produzca el gesto o seña de que quiere seguir balanceándose')
                actividades_expre_com.append(
                    'Enseñarle al niño/a señalar objetos, mediante la participación del adulto '
                    'al tomar su mano y guiar el movimiento')
                actividades_expre_com.append(
                    'Utilizar algún tipo de comunicador (tecnológico, gráfico) como sustitutivo del lenguaje oral')
            if request.POST.get('p22', False) == 'no':
                actividades_expre_com.append(
                    'Aumentar el vocabulario partiendo de objetos y TEMAS de interés para el niño/a')
                actividades_expre_com.append(
                    'Proporcionar el nombre de los objetos aunque ya lo hayamos enseñado antes cuando estos tengan '
                    'diferente color, textura o tamaño para generalizar el vocabulario ej. CARRO ')
                actividades_expre_com.append(
                    'Establecer momentos de comunicación con su hijo/a el cual contenga preguntas, '
                    'manipulación de objetos y sensaciones (olores, sabores) para motivar el uso de  '
                    'nuevo vocabulario')
                actividades_expre_com.append(
                    'Dar el nombre de los objetos cuando se realicen actividades con él/ella. Ej. '
                    'al momento de vestirlo decir el nombre de las prendas que le colocamos en ese momento ')
            if request.POST.get('p23', False) == 'no':
                actividades_expre_com.append(
                    'Iniciar esta enseñanza cuando el niño tenga un considerable manejo de lenguaje comprensivo'
                    ' (comprensión de órdenes simples, identificación de objetos comunes, etc.) ')
                actividades_expre_com.append(
                    'Utilizar un pronombre a la vez para la incorporación de estos al vocabulario, se recomienda '
                    'partir de posesivo MIO y pronombre YO para posterior seguir con los demás elementos')
                actividades_expre_com.append(
                    'Utilizar el apoyo de fotografías personales en los que se encuentre el niño/a solo para utilizar '
                    'la pregunta de referencia “¿Quién es?” y la respuesta a dar será “YO” tomando al niño/a de la mano '
                    'y tocando su pecho para dar la simulación que él/ella lo realiza'
                    'Se puede realizar la actividad de igual manera con el uso de un espejo')
            if request.POST.get('p24', False) == 'no':
                if edad >= 2 and edad < 4:
                    actividades_expre_com.append(
                        'Enseñar el uso de estructuras por medio de lectura  de gráficos o pictogramas que '
                        'contengan los siguientes elementos:'
                        'Sustantivo + verbo + sustantivos (mamá dame agua)')
                if edad >= 4 and edad < 5:
                    actividades_expre_com.append(
                        'Enseñar el uso de estructuras por medio de lectura  de gráficos o pictogramas que '
                        'contengan los siguientes elementos:'
                        'Artículo + verbo + nexo + sustantivo (la niña come una manzana)'
                    )
                if edad >= 5:
                    actividades_expre_com.append(
                        'Enseñar el uso de estructuras por medio de lectura  de gráficos o pictogramas que contengan '
                        'los siguientes elementos:'
                        'Artículo + verbo + nexo + conector + sustantivo (la niña come una manzanza con yogurt)'
                    )
                actividades_expre_com.append(
                    'Realizar preguntas claves para provocar el uso de vocabulario espontáneo Ej. Con el apoyo de la mano del '
                    'padre tocar el pecho del niño/a para que este diga su nombre “JUAN”, se le preguntará qué necesita y la '
                    'respuesta esperada será QUIERE AGUA, etc.')
            if request.POST.get('p25', False) == 'no':
                actividades_expre_com.append(
                    'Motivar la comunicación por medio de actividades y temas que sean de interés para el niño/a')
                actividades_expre_com.append(
                    'Iniciar el proceso por medio de la imitación, adecuando nuestras acciones imitando al niño')
                actividades_expre_com.append(
                    'Establecer juegos motores que motiven al niño a participar, ej. Corre que te alcanzo, escondite, etc. esto motivará '
                    'al niño/a a interactuar con el adulto y mejorar la comunicación  ')
                actividades_expre_com.append(
                    'Establecer tiempos cortos inicialmente de compartir con el niño/a actividades para luego incorporar gradualmente el tiempo')
            if request.POST.get('p26', False) == 'no':
                actividades_expre_com.append(
                    'Motivar la comunicación por medio de actividades y temas que sean de interés para el niño/a')
                actividades_expre_com.append(
                    'Iniciar el proceso por medio de la imitación, adecuando nuestras acciones imitando al niño')
                actividades_expre_com.append(
                    'Establecer juegos motores que motiven al niño a participar, ej. Corre que te alcanzo, escondite, etc. esto motivará '
                    'al niño/a a interactuar con el adulto y mejorar la comunicación  ')
                actividades_expre_com.append(
                    'Establecer tiempos cortos inicialmente de compartir con el niño/a actividades para luego incorporar gradualmente el tiempo')
            if request.POST.get('p27', False) == 'no':
                actividades_expre_com.append(
                    'Motivar la comunicación por medio de actividades y temas que sean de interés para el niño/a')
                actividades_expre_com.append(
                    'Iniciar el proceso por medio de la imitación, adecuando nuestras acciones imitando al niño')
                actividades_expre_com.append(
                    'Establecer juegos motores que motiven al niño a participar, ej. Corre que te alcanzo, escondite, etc. esto motivará '
                    'al niño/a a interactuar con el adulto y mejorar la comunicación  ')
                actividades_expre_com.append(
                    'Establecer tiempos cortos inicialmente de compartir con el niño/a actividades para luego incorporar gradualmente el tiempo')
            if request.POST.get('p28', False) == 'no':
                actividades_expre_com.append(
                    'Utilizar apoyos visuales con diferentes emociones en los que el niño/a pueda seleccionar cómo se siente')
                actividades_expre_com.append(
                    'Utilizar historias sociales en los que se armará una historia del niño/a mientras se le pregunta las actividades,'
                    ' lugares, personas, sensaciones y sentimientos que ocurrieron en ella')
            if request.POST.get('p29', False) == 'no':
                actividades_expre_com.append(
                    'A medida que el niño ha incorporado un considerable vocabulario comprensivo y expresivo  tendrá interés por '
                    'preguntar en base a la imitación ¿Qué es, quién es? Como preguntas que hemos incorporado a lo largo '
                    'del proceso de adquisición de vocabulario')
                actividades_expre_com.append(
                    'Incorporar objetos, situaciones y acciones que no son comunes para el niño/a para generar curiosidad')
            if request.POST.get('p30', False) == 'no':
                actividades_expre_com.append(
                    'Establecer temas que sean de conocimiento previo del niño (qué hizo en la escuela, juguete preferido, etc.)')
                actividades_expre_com.append(
                    'Al identificar que el niño/a pierde el tema en la conversación, ayudarlo generando preguntas que'
                    ' le ayuden a retomar el tema')
                actividades_expre_com.append(
                    'Apoyarse de ayudas visuales como fotografías del tema que queremos incorporar')
            if request.POST.get('p31', False) == 'no':
                actividades_expre_com.append(
                    'Realizar juegos en los que se visualice la toma de turnos ej. Teléfono de vaso e hilo, rondas con globo y '
                    'la persona que tiene el globo tendrá la oportunidad de hablar, etc. ')
                actividades_expre_com.append(
                    'Utilizar indicadores visuales que indique al niño cuándo es el momento de hablar o permanecer '
                    'en silencia (pictogramas de conducta, semáforo, etc.)')
                actividades_expre_com.append(
                    'Enseñar normas sociales  y de comportamiento, mediante historias sociales en el que se incorpore '
                    'normas de conducta en diferentes lugares y personas')
            if request.POST.get('p32', False) == 'no':
                actividades_expre_com.append(
                    'Iniciar este proceso cuando el niño haya adquirido un lenguaje comprensivo y expresivo '
                    'amplio para el manejo de tiempos verbales como pasado y futuro')
                actividades_expre_com.append(
                    'Utilizar historietas, cuentos o láminas en los que se identifique secuencias de actividades para '
                    'generar preguntas de qué hizo, qué hace, qué hará, etc.')
                actividades_expre_com.append(
                    'Reforzar con ejercicios de antes y después (orden de eventos, sembrar plantas, etc.)')
                actividades_expre_com.append(
                    'Anticipar eventos agradables de la semana para indicar que hará en los próximos días e incorporar preguntas '
                    'como ¿qué harás? Seguido de nuestra indicación')
                actividades_expre_com.append(
                    'Utilizar agendas visuales para ayudar al niño/a en la planificación de actividades futuras')
            if request.POST.get('p33', False) == 'no':
                if edad >= 2.5 and edad < 3:
                    actividades_expre_com.append(
                        'Rezalizar ejercicios con los labios: apretar, simular como enviar besos')
                    actividades_expre_com.append(
                        'Realizar ejercicios con la lengua: sacar y meter la lengua de manera rápida y lenta, etc.')
                    actividades_expre_com.append(
                        'Reforzar con ejercicios de antes y después (orden de eventos, sembrar plantas, etc.)')
                    actividades_expre_com.append(
                        'Realizar ejercicios de soplo: Soplar burbujas, material con papel picado, trozos de papel sobre '
                        'la mesa, hacer sonar diversos instrumentos musicales de viento, como trompetas, flautas, armónicas, '
                        'etc.')
                    actividades_expre_com.append(
                        'Reforzar la movilidad de órganos por medio de la masticación de alimentos duros')
                    actividades_expre_com.append(
                        'Evitar el uso de biberón')
                    actividades_expre_com.append(
                        'Realizar ejercicios de ritmo ej. Caminar siguiendo el ritmo que se le marque en el tambor')
                    actividades_expre_com.append(
                        'Repetir sílabas que no formen palabra por ejemplo: pa - ba - ta, be - me - pe, da - ta – na, '
                        'ta-ta, ta-ta ta-ta, pa pa-pa-pa pa pa-pa-pa.')
                    actividades_expre_com.append(
                        'El adulto deberá identificar la posición de la letra a reforzar para que el niño/a imite y '
                        'aprenda la correcta ubicación para la producción de cada letra. Ej.'
                        '/m/, cerrar/apretar los labios'
                        '/d/, apretar la lengua contra los dientes y expulsar aire')
                    actividades_expre_com.append(
                        'Evitar utilizar un lenguaje infantil en casa, hablar con el niño/a de manera clara y fuerte')
                if edad >= 3 and edad < 4.5:
                    actividades_expre_com.append(
                        'Realizar ejercicios de ritmo ej. Caminar siguiendo el ritmo que se le marque en el tambor')
                    actividades_expre_com.append(
                        'Evitar el uso de biberón')
                    actividades_expre_com.append(
                        'Realizar ejercicios con los labios: apretar, simular como enviar besos, vibrar ')
                    actividades_expre_com.append(
                        'Realizar ejercicios con la lengua: sacar y meter la lengua de manera rápida y lenta, elevar y descender ')
                    actividades_expre_com.append(
                        'Estimular la percepción de sonidos, realizando juegos de identificación de sonidos (animales, medio ambiente, story)'
                    )
                    actividades_expre_com.append(
                        'Realizar ejercicios de ritmo ej. Caminar siguiendo el ritmo que se le marque en el tambor posteriormente'
                        ' escuchar el ritmo marcado por el tambor y seguirlo a la vez, golpeando con la mano sobre la mesa  '
                    )
                    actividades_expre_com.append(
                        'Repetir sílabas que no formen palabra por ejemplo: pa - ba - fa, be - me - pe, ja - ga - ca.')
                    actividades_expre_com.append(
                        'El adulto deberá identificar la posición de la letra a reforzar para que el niño/a imite y aprenda la correcta '
                        'ubicación para la producción de cada letra. Ej.'
                        '/m/, cerrar/apretar los labios'
                        '/d/, apretar la lengua contra los dientes y expulsar aire'
                        '/l/, elevar la lengua a la parte posterior de los incisivos superiores'
                        '/ch/, juntar los dientes y emitir sonidos con fuerza')
                if edad >= 4.5:
                    actividades_expre_com.append(
                        'Realizar ejercicios de ritmo ej. Caminar siguiendo el ritmo que se le marque en el tambor posteriormente'
                        ' escuchar el ritmo marcado por el tambor y seguirlo a la vez, golpeando con la mano sobre la mesa  '
                    )
                    actividades_expre_com.append(
                        'Estimular la percepción de sonidos, realizando juegos de identificación de sonidos (animales, medio ambiente, story)'
                    )
                    actividades_expre_com.append(
                        'Realizar ejercicios de ritmo ej. Caminar siguiendo el ritmo que se le marque en el tambor')
                    actividades_expre_com.append(
                        'Realizar ejercicios con los labios: apretar, simular como enviar besos, vibrar ')
                    actividades_expre_com.append(
                        'Evitar utilizar un lenguaje infantil en casa, hablar con el niño/a de manera clara y fuerte')
                    actividades_expre_com.append(
                        'Reforzar la movilidad de órganos por medio de la masticación de alimentos duros')
                    actividades_expre_com.append(
                        'Realizar ejercicios con la lengua: sacar y meter la lengua de manera rápida y lenta, elevar y descender, '
                        'lateralizar, vibrar ')
                    actividades_expre_com.append(
                        'Repetir sílabas que no formen palabra por ejemplo: pa - ba - fa, be - me - pe, '
                        'ja - ga – ca, ra-ra-ra , ri , ra-ra-ra , ri')
                    actividades_expre_com.append(
                        'Realizar ejercicios de soplo: Soplar burbujas, hacer sonar diversos instrumentos musicales de'
                        ' viento, como trompetas, flautas, armónicas, etc. Se hará soplar al niño/a  con un sorbete '
                        'o tubo pequeño a la que adaptará los labios, colocar una portería y jugar con pelotas soplándolas '
                        'para realizar anotaciones  ')
                    actividades_expre_com.append(
                        'Realizar ejercicios de imitación: su hijo/a deberá  observa la postura del adulto y '
                        'luego cerrando los ojos, lo imita ')
                    actividades_expre_com.append(
                        'Realizar ejercicios de silencio que ayuden a centrar la atención y luego preguntarle por '
                        'los sonidos ocasionales que haya podido percibir.')
                    actividades_expre_com.append(
                        'El adulto deberá identificar la posición de la letra a reforzar para que el niño/a imite y aprenda '
                        'la correcta ubicación para la producción de cada letra. Ej.'
                        '/m/, cerrar/apretar los labios /d/, apretar la lengua contra los dientes y expulsar aire'
                        '/l/, elevar la lengua a la parte posterior de los incisivos superiores'
                        '/ch/, juntar los dientes y emitir sonidos con fuerza'
                        '/r/ colocar la punta de la lengua el paladar y que el niño/a produzca el sonido mientras se '
                        'aprieta las mejillas para motivar la expulsión de vibración.')
                    actividades_expre_com.append(
                        'Iniciar la enseñanza con las letras más simples como /m/, /p/ /c,q/k/  dejar para'
                        'el último letras como /r/, /s/, / y sínfones')
            if request.POST.get('p34', False) == 'no':
                actividades_fluidez.append(
                    'Iniciar con interacción básica mediante temas de interés que motiven a su hijo/a a compartir tiempos de atención')
                actividades_fluidez.append(
                    'Establecer rutinas que motiven a instaurar conversaciones, ej. el adulto puede seleccionar espacios '
                    'en el día para llamar por teléfono al niño/a; formular preguntas de las actividades realizadas'
                    ' en el día (el adulto deberá conocer de antemano lo ocurrido en el día)')
                actividades_fluidez.append(
                    'Motivar el uso de lenguaje espontáneo por medio de canciones de agrado para el niño, uso de '
                    'títeres o marionetas para recrear una historia, etc.')
            if request.POST.get('p35', False) == 'no':
                actividades_fluidez.append(
                    'Si su niño/a presenta ecolalia (repetición de palabras), se requiere identificar si la dificultad es'
                    ' descartada por: una alteración en el área comprensiva, horas excesivas de ocio, o bloqueo en la comunicación '
                    'en el cual el niño/a no se encuentran interesados en el tema o la orden')
                actividades_fluidez.append(
                    'Simplificar la información, no sobre cargar de órdenes')
                actividades_fluidez.append(
                    'Establecer actividades organizadas y estructuradas en el día,  para que el niño/a permanezca '
                    'centrado en una organización y evite sentirse ansioso en el día, ya que esto puede provocar su ecolalia')
                actividades_fluidez.append(
                    'Utilizar preguntas de clave tipo Q “Qué es, quién es, qué hace” ')
            if request.POST.get('p36', False) == 'no':
                actividades_voz.append(
                    'El uso de la entonación “peculiar” en su niño/a puede estar ligado a alteraciones a nivel sensorial'
                    ' (oído, gusto, tacto, olfato, visión), por lo que es importante trabajar en un programa de integración '
                    'sensorial con un especialista')
                actividades_voz.append(
                    'Estimular la producción de la voz en intensidad, ritmo, melodía por medio de la música')
                actividades_voz.append(
                    'Realizar juegos de roles ( dramatizaciones) en los que se pueda establecer diálogos con '
                    'diferentes guiones en los que se incorpore emociones diversas ')
            if request.POST.get('p37', False) == 'no':
                actividades_voz.append(
                    'El uso de la entonación “peculiar” en su niño/a puede estar ligado a alteraciones a nivel sensorial'
                    ' (oído, gusto, tacto, olfato, visión), por lo que es importante trabajar en un programa de integración '
                    'sensorial con un especialista')
                actividades_voz.append(
                    'Estimular la producción de la voz en intensidad, ritmo, melodía por medio de la música')
                actividades_voz.append(
                    'Realizar juegos de roles ( dramatizaciones) en los que se pueda establecer diálogos con '
                    'diferentes guiones en los que se incorpore emociones diversas ')
            if request.POST.get('p38', False) == 'no':
                actividades_voz.append(
                    'El uso de la entonación “peculiar” en su niño/a puede estar ligado a alteraciones a nivel sensorial'
                    ' (oído, gusto, tacto, olfato, visión), por lo que es importante trabajar en un programa de integración '
                    'sensorial con un especialista')
                actividades_voz.append(
                    'Estimular la producción de la voz en intensidad, ritmo, melodía por medio de la música')
                actividades_voz.append(
                    'Realizar juegos de roles ( dramatizaciones) en los que se pueda establecer diálogos con '
                    'diferentes guiones en los que se incorpore emociones diversas ')

            request.session['actividades_alimentacion'] = actividades_alimentacion
            request.session['actividades_comprension'] = actividades_comprension
            request.session['actividades_expre_com'] = actividades_expre_com
            request.session['actividades_fluidez'] = actividades_fluidez
            request.session['actividades_voz'] = actividades_voz

            return redirect('automata:resultadoTest')
    return render(request, 'automata/test.html', {'edad': edad})


def resultadoTest(request):
    return render(request, 'automata/resultadoTest.html')


# Definimos las caracteristicas fijas de la primera página
def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Plainced")
    archivo_imagen = 'InclusionEducativa/static/pdf/img/cover.png'
    canvas.drawImage(archivo_imagen, 40, 750, 120, 90, preserveAspectRatio=True, mask='auto')
    canvas.setFont('Times-Bold', 20)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, titulo)
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Página %s" % (doc.page))
    canvas.restoreState()


# Definimos disposiciones alternas para las caracteristicas de las otras páginas
def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Página %d" % (doc.page))
    canvas.restoreState()


# ===============================
def reporte(request):
    buffer = io.BytesIO()
    h1 = ParagraphStyle(
        'subtitulo',
        fontName="Times-Roman",
        fontSize=14,
        leading=20)
    h2 = ParagraphStyle(
        'subtitulo',
        fontName="Times-Roman",
        fontSize=12,
        leading=16)

    # Creamos un documento basándonos en una plantilla
    doc = SimpleDocTemplate(buffer)
    # Iniciamos el story para los registros
    story = [Spacer(0, 80)]
    # Definimos un estilo
    estilo = styles['Normal']
    linkStyle = ParagraphStyle(
        'link',
        textColor='#3366BB'
    )
    paragraphStyle = ParagraphStyle('parrafos',
                                    alignment=TA_JUSTIFY,
                                    fontSize=10,
                                    fontName="Times-Roman",
                                    )

    # Creamos 100 párrafos
    # for i in range(100):
    #     texto = ("Este es el párrafo número %s. " % (i + 1)) * 20
    #     # Definimos un párrafo usando un estilo
    #     p = Paragraph(texto, estilo)
    #     # Registramos en el story
    #     story.append(p)
    #     # También registramos el espacio que tendrá entre párrafos
    #     story.append(Spacer(0, 20))

    # actividades_alimentacion = request.session.get('actividades_alimentacion')
    # if actividades_alimentacion:
    #     story.append(Paragraph('Alimentacion', h1))
    #     story.append(Spacer(1, 0.1 * inch))
    #     story.append(Spacer(1, 0.1 * inch))
    #     for i, actividad in enumerate(actividades_alimentacion):
    #         story.append(Paragraph(actividad, estilo, bulletText=str(i + 1) + '.'))
    #         story.append(Spacer(1, 0.1 * inch))
    #     story.append(Paragraph('<b>Links de apoyo:</b>', estilo))
    #     story.append(Spacer(1, 0.1 * inch))
    #     story.append(Paragraph('http://www.arasaac.org/herramientas.php', linkStyle))
    #     story.append(Paragraph('http://wikinclusion.org/index.php/1028', linkStyle))
    #     story.append(Paragraph('http://wikinclusion.org/index.php/1018', linkStyle))
    #     story.append(Paragraph('http://wikinclusion.org/index.php/1020', linkStyle))
    #     story.append(Spacer(1, 0.1 * inch))

    actividades_alimentacion = request.session.get('actividades_alimentacion')
    if actividades_alimentacion:
        story.append(Paragraph('<b>Alimentación</b>', h1))
        lista = ListFlowable(
            [ListItem(Paragraph(actividad, paragraphStyle)
                      )
             for actividad in
             actividades_alimentacion], bulletFontSize=10, bulletFontName="Times-Roman", bulletType='bullet',

            leftIndent=10)
        story.append(lista)
        story.append(Spacer(1, 0.1 * inch))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('Links de apoyo:', h2))
        story.append(Paragraph('http://www.arasaac.org/herramientas.php', linkStyle))
        story.append(Paragraph('http://wikinclusion.org/index.php/1028', linkStyle))
        story.append(Paragraph('http://wikinclusion.org/index.php/1018', linkStyle))
        story.append(Paragraph('http://wikinclusion.org/index.php/1020', linkStyle))
        story.append(Spacer(1, 0.1 * inch))
    actividades_comprension = request.session.get('actividades_comprension')
    if actividades_comprension:
        story.append(Paragraph('<b>Comprensión</b>', h1))
        lista = ListFlowable(
            [ListItem(Paragraph(actividad, paragraphStyle)
                      )
             for actividad in
             actividades_comprension], bulletFontSize=10, bulletFontName="Times-Roman", bulletType='bullet',

            leftIndent=10)
        story.append(lista)
        story.append(Spacer(1, 0.1 * inch))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('Links de apoyo:', h2))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('http://www.arasaac.org/herramientas.php', linkStyle))
        story.append(Paragraph('http://www.arasaac.org/materiales.php?id_material=2705', linkStyle))
        story.append(Paragraph('http://www.arasaac.org/materiales.php?id_material=2728', linkStyle))
        story.append(
            Paragraph('https://elsonidodelahierbaelcrecer.blogspot.com/search/label/Categor%C3%ADas', linkStyle))
        story.append(Paragraph('http://www.arasaac.org/catalogos.php', linkStyle))
        story.append(Paragraph('http://wikinclusion.org/index.php/Estimulaci%C3%B3n', linkStyle))
        story.append(Spacer(1, 0.1 * inch))

    actividades_expre_com = request.session.get('actividades_expre_com')
    if actividades_expre_com:
        story.append(Paragraph('<b>Expresion y Comunicacion</b>', h1))
        lista = ListFlowable(
            [ListItem(Paragraph(actividad, paragraphStyle)
                      )
             for actividad in
             actividades_expre_com], bulletFontSize=10, bulletFontName="Times-Roman", bulletType='bullet',

            leftIndent=10)
        story.append(lista)
        story.append(Spacer(1, 0.1 * inch))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('Links de apoyo:', h2))
        story.append(Paragraph('http://www.arasaac.org/materiales.php?id_material=2710', linkStyle))
        story.append(Paragraph('http://www.arasaac.org/materiales.php?id_material=2725', linkStyle))
        story.append(Paragraph('https://elsonidodelahierbaelcrecer.blogspot.com/search/label/Lenguaje', linkStyle))
        story.append(Paragraph('http://wikinclusion.org/index.php/Escuchar,_hablar_y_conversar', linkStyle))
        story.append(Spacer(1, 0.1 * inch))

    actividades_fluidez = request.session.get('actividades_fluidez')
    if actividades_fluidez:
        story.append(Paragraph('<b>Fluidez</b>', h1))
        lista = ListFlowable(
            [ListItem(Paragraph(actividad, paragraphStyle)
                      )
             for actividad in
             actividades_fluidez], bulletFontSize=10, bulletFontName="Times-Roman", bulletType='bullet',

            leftIndent=10)
        story.append(lista)
        story.append(Spacer(1, 0.1 * inch))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('Links de apoyo:', h2))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('http://www.arasaac.org/materiales.php?id_material=2716', linkStyle))
        story.append(Paragraph('https://elsonidodelahierbaelcrecer.blogspot.com/search/label/conversacion', linkStyle))
        story.append(Spacer(1, 0.1 * inch))

    actividades_voz = request.session.get('actividades_voz')
    if actividades_voz:
        story.append(Paragraph('<b>Voz</b>', h1))
        lista = ListFlowable(
            [ListItem(Paragraph(actividad, paragraphStyle)
                      )
             for actividad in
             actividades_voz], bulletFontSize=10, bulletFontName="Times-Roman", bulletType='bullet',
            leftIndent=10)
        story.append(lista)
        story.append(Spacer(1, 0.1 * inch))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('Links de apoyo:', estilo))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph('http://www.arasaac.org/materiales.php?id_material=2636', linkStyle))
        story.append(Spacer(1, 0.1 * inch))

    # Construimos el documento a partir de los argumentos definidos
    doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='plainced_actividades.pdf')
