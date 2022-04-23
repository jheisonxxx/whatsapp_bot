import json
import requests
import datetime

from models import Wstatus, session


class ultraChatBot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['data']
        self.ultraAPIUrl = 'https://api.ultramsg.com/instance5531/'
        self.token = '4s825sqzypk7rpv9'
        self.tree_level = 0
        self.q_a = 'q'

   
    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to" : chatID,
                "body" : text}  
        answer = self.send_requests('messages/chat', data)
        return answer

    def send_image(self, chatID):
        data = {"to" : chatID,
                "image" : "https://file-example.s3-accelerate.amazonaws.com/images/test.jpeg"}  
        answer = self.send_requests('messages/image', data)
        return answer

    def send_video(self, chatID):
        data = {"to" : chatID,
                "video" : "https://file-example.s3-accelerate.amazonaws.com/video/test.mp4"}  
        answer = self.send_requests('messages/video', data)
        return answer

    def send_audio(self, chatID):
        data = {"to" : chatID,
                "audio" : "https://file-example.s3-accelerate.amazonaws.com/audio/2.mp3"}  
        answer = self.send_requests('messages/audio', data)
        return answer


    def send_voice(self, chatID):
        data = {"to" : chatID,
                "audio" : "https://file-example.s3-accelerate.amazonaws.com/voice/oog_example.ogg"}  
        answer = self.send_requests('messages/voice', data)
        return answer

    def send_contact(self, chatID):
        data = {"to" : chatID,
                "contact" : "14000000001@c.us"}  
        answer = self.send_requests('messages/contact', data)
        return answer


    def time(self, chatID):
        t = datetime.datetime.now()
        time = t.strftime('%Y-%m-%d %H:%M:%S')
        return self.send_message(chatID, time)


    def welcome(self,chatID):
        welcome_string = "Hola, gracias por Comunicarte con Yachay"
        wstatus = Wstatus(level="menu1", chatId=chatID)
        session.add(wstatus)
        session.commit()
        return self.send_message(chatID, welcome_string)

    def menu_level_2(self, chatID, text):
        if text[0].lower() == 'hi':
            return self.welcome(chatID)
        elif text[0].lower() == 'time':
            return self.time(chatID)
        elif text[0].lower() == 'image':
            return self.send_image(chatID)
        elif text[0].lower() == 'video':
            return self.send_video(chatID)
        elif text[0].lower() == 'audio':
            return self.send_audio(chatID)
        elif text[0].lower() == 'voice':
            return self.send_voice(chatID)
        elif text[0].lower() == 'contact':
            return self.send_contact(chatID)
        else:
            return self.welcome(chatID)

    def menu_level_1(self, chatID, text):
        return


    def Processingـincomingـmessages(self):
        if self.dict_messages != []:
            message =self.dict_messages
            text = message['body'].split()
            if not message['fromMe']:
                chatID  = message['from']
                wstatus = session.query(Wstatus).filter_by(chatId=chatID).first()
                if wstatus is None:
                    return self.welcome(chatID)
                elif wstatus.level == "menu1":
                    text_menu1 = """Seleccione una opcion del menu
                                    1)Solicitudes
                                    2)Consultas"""
                    wstatus.level = "menu1op"
                    session.commit()
                    return self.send_message(chatID, text_menu1)
                elif wstatus.level == "menu1op":
                    if text[0].lower() == '1':
                        text_menu1 = """Gracias por comunicarte a nuestro canal de Solicitudes, 
                                                        por favor ingresa el tipo de Solicitud quedeseas generar
                                                        1)Envío de la última factura 
                                                        2)Envío de las Cuatro facturas anteriores 
                                                        3)Ultima nota de credita"""
                        wstatus.level = "menu12op"
                        session.commit()
                        return self.send_message(text_menu1, chatID)
                    elif text[0].lower() == '2':
                        text_menu2 = """Gracias por comunicarte a nuestro canal de Solicitudes, 
                                                        por favor ingresa el tipo de Solicitud quedeseas generar
                                                        1)Forma de Pago de Servicios 
                                                        2)Deseo saber mi consultor asignado 
                                                        3)Deseo comunicarme con mi consultor"""
                        wstatus.level = "menu22op"
                        session.commit()
                        return self.send_message(text_menu2, chatID)
                    else:
                        text_menu_na = "Selecciona bien las opciones"
                        return self.send_message(text_menu_na, chatID)

                elif wstatus.level == "menu12op":
                    if text[0].lower() == '1':
                        text_menu3_1 = "valid response"
                        return self.send_message(text_menu3_1, chatID)
                    elif text[0].lower() == '2':
                        text_menu3_2 = "opcion2"
                        return self.send_message(text_menu3_2, chatID)
                    else:
                        text_menu_na = "Selecciona bien las opciones"
                        return self.send_message(text_menu_na, chatID)
                elif wstatus.level == "menu22op":
                    if text[0].lower() == '1':
                        text_menu3_1 = "Tu consultor es Jheison"
                        #return self.send_message(text_menu3_1, chatID)
                        return self.time(chatID)
                    elif text[0].lower() == '2':
                        text_menu3_2 = "As click aca para comunicarte con tu consultor"
                        return self.send_message(text_menu3_2, chatID)
                    else:
                        text_menu_na = "Selecciona bien las opciones"
                        return self.send_message(text_menu_na, chatID)
            else: return 'NoCommand'


        
        




