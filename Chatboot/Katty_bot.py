import logging
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import utils
import spacy
from Levenshtein import *
import datetime
import psycopg2

from distancia import listAllSequence


class Chatbot:
    def __init__(self, token='1340263200:AAE6OzmX3mp3lGgE79dWFrXEI2ZlS8oKdFc'):  # token de telegram
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        authenticator = IAMAuthenticator('GI6QTbtMI-RDWkBED7PYeBKIgv1Qi0EY9lkQFfKuecQg')  # Token de IBM
        self.speech2text = SpeechToTextV1(authenticator)

        # Handler para crear un comando hola
        self.hola_handler = CommandHandler('start', self.hola)
        self.dispatcher.add_handler(self.hola_handler)

        # Handler para filtrar mensajes de audio
        self.bot = telegram.Bot(token=token)
        self.obtener_audio = MessageHandler(Filters.voice, self.guardar_audio)
        self.dispatcher.add_handler(self.obtener_audio)

        # Handler para filtrar mensajes de texto
        self.obtener_texto = MessageHandler(Filters.text, self.texto)
        self.dispatcher.add_handler(self.obtener_texto)

        self.updater.start_polling()
        self.updater.idle()

    # Metodo que procesa el audio que envia el usuario
    def guardar_audio(self, update, context):
        print('Llego un audio')
        archivo = self.bot.get_file(update.message.voice.file_id)
        archivo.download('mensaje_audio.ogg')
        audio = open('mensaje_audio.ogg', 'rb')
        res = self.speech2text.recognize(audio=audio, content_type='audio/ogg', timestamps=True,
                                         model='es-ES_NarrowbandModel', word_confidence=True)
        lista = res.get_result()['results'][0]['alternatives'][0]['timestamps']
        persona = update.message.from_user
        for datos in lista:
            print(datos[0], 'confianza', datos[1])
            if (datos[0] == 'hola') == 1:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=utils.MsgTemplate.inicial_msg, parser='Markdown')
            elif (datos[0] == 'significado' or datos[0] == 'palabras' or datos[0] == 'acciones') == True:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=utils.MsgTemplate.dificultad1_msg, parser='Markdown')
            elif (datos[0] == 'escuchar' or datos[0] == 'sonidos' or datos[0] == 'ambiente') == True:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=utils.MsgTemplate.dificultad2_msg, parser='Markdown')
            elif (datos[0] == 'ordenes' or datos[0] == 'sigue') == 1:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=utils.MsgTemplate.dificultad3_msg, parser='Markdown')
            elif (datos[0] == 'comprende' or datos[0] == 'preguntas' or datos[0] == 'responde') == True:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=utils.MsgTemplate.dificultad4_msg, parser='Markdown')
            elif (datos[0] == 'identifica' or datos[0] == 'contenidos' or datos[0] == 'trabajan') == True:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=utils.MsgTemplate.dificultad5_msg, parser='Markdown')
            elif (datos[0] == 'regresar') == True:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=utils.MsgTemplate.inicial_msg, parser='Markdown')

    # Texto que permite saber que mensajes manda el usuario
    def texto(self, update, context):
        user = update.message.from_user
        usuario_nombre = user['first_name']
        usuario_apellido = user['last_name']
        usuario = usuario_nombre + ' ' + usuario_apellido
        print(usuario)
        x = datetime.datetime.now()
        fecha = x.strftime("%Y-%m-%d")
        print(fecha)
        nlp = spacy.load("es_core_news_sm")
        verbos = []
        ra = []

        v = ''

        ordenes = ['Hola', 'Does not know the meaning of the words or actions',
                   'No puede escuchar sonidos del ambiente',
                   'No sigue órdenes ', 'No comprende preguntas o no las responde de manera lógica',
                   'No identifica contenidos pedagógicos que trabajan en su nivel escolar', 'Regresar']

        print('LLego texto')
        txt_mensaje = str(update.message.text)

        conexion1 = psycopg2.connect(database="chatbot", user="plainced")
        cursor1 = conexion1.cursor()
        # import mysql.connector
        #
        # cnx = mysql.connector.connect(user='plainced',
        #                               host='localhost',
        #                               database='plainced')

        sql = "insert into usuario(usuario_nombre, usuario_fecha) values (%s,%s)"
        datos = (usuario, fecha)
        cursor1.execute("insert into usuario(usuario_nombre, usuario_fecha) values (%s,%s)", datos)
        conexion1.commit()
        conexion1.close()
        #
        # cursor = cnx.cursor()
        # cursor.execute(sql, datos)
        # cnx.commit()
        # cnx.close()

        for orde in range(len(ordenes)):
            b = round(ratio(txt_mensaje, ordenes[orde]))
            ra.append(b)

        print(ra)

        pos_max = ra.index(max(ra))

        ordenparecerse = ordenes[pos_max]
        print('Es:', ordenparecerse)
        print(ordenparecerse)
        mensajecom = listAllSequence(txt_mensaje, ordenparecerse)
        print(mensajecom)
        print(pos_max)

        print(txt_mensaje)
        mensaje = mensajecom
        print('El mensaje completado es', mensaje)

        mensaje = mensajecom.split(' ')
        print(mensaje)
        persona = update.message.from_user

        # Aqui obtenemos los verbos que existen en la oracion mediante spacy y el post ==Verb
        verbos = [w for w in nlp(mensajecom) if w.is_punct != True and w.pos_ == 'VERB']
        print(verbos)

        if not verbos:
            v = txt_mensaje
        else:
            for x in verbos:
                v = str(x)
                print('Es:', v)

        if mensajecom.find('Hola') != -1:
            context.bot.send_message(chat_id=update.effective_chat.id, text=utils.MsgTemplate.inicial_msg,
                                     parser='Markdown')
        elif (v.find('know') and mensajecom.find('words')) != -1:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='La dificultad seleccionada es:\n' + mensajecom)
            context.bot.send_message(chat_id=update.effective_chat.id, text=utils.MsgTemplate.dificultad1_msg,
                                     parser='Markdown')
        elif (v.find('escuchar') and mensajecom.find('sonidos')) != -1:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='La dificultad seleccionada ha sido:\n' + mensajecom)
            context.bot.send_message(chat_id=update.effective_chat.id, text=utils.MsgTemplate.dificultad2_msg,
                                     parser='Markdown')
        elif (v.find('sigue') and mensajecom.find('órdenes')) != -1:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='La dificultad seleccionada ha sido:\n' + mensajecom)
            context.bot.send_message(chat_id=update.effective_chat.id, text=utils.MsgTemplate.dificultad3_msg,
                                     parser='Markdown')
        elif (v.find('comprende') and v.find('responde') and mensajecom.find('preguntas')) != -1:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='La dificultad seleccionada ha sido:\n' + mensajecom)
            context.bot.send_message(chat_id=update.effective_chat.id, text=utils.MsgTemplate.dificultad4_msg,
                                     parser='Markdown')
        elif (v.find('identifica') and mensajecom.find('pedagógicos')) != -1:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='La dificultad seleccionada ha sido:\n' + mensajecom)
            context.bot.send_message(chat_id=update.effective_chat.id, text=utils.MsgTemplate.dificultad5_msg,
                                     parser='Markdown')
        elif (v.find('regresar')):
            context.bot.send_message(chat_id=update.effective_chat.id, text=utils.MsgTemplate.inicial_msg,
                                     parser='Markdown')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=utils.MsgTemplate.understand_msg, parse='Markdown')

    def hola(self, update, context):
        print('Comando start')
        persona = update.message.from_user
        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgIAAxkBAAEBEJ9fEkFiRV1xrfxi4qtATfjjhxCnwwACVAADQbVWDGq3-McIjQH6GgQ')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="¡SOY INCLUBOT! \U0001f481\U0001f3fb" + '\n' +
                                      "\U0001f3c1 BRINDO ACTIVIDADES PARA NIÑOS CON DIFICULTADES RELACIONADAS AL LENGUAJE MISMAS QUE DEPENDERÁN DE TÍ PONERLAS EN PRÁCTICA" + "\n" +
                                      "\U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389" + '\n' +
                                      "PARA INTERACTUAR CONMIGO ENVÍA UN AUDIO \U0001f3a4 O UN TEXTO \u2709\uFE0F DICIENDO 'HOLA' \U0001f481\U0001f3fb:",
                                 parse='Markdown')


if __name__ == '__main__':
    chatbot = Chatbot()
