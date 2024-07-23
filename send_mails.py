from mailjet_rest import Client
import os
api_key = 'f672fa3673f2a393922100ffd05a28eb'
api_secret = 'a491ddbb086fbc61f7751f493a3da170'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

mail_dict = {
    "Manuel": "faciomanuel@gmail.com",
    "Celeste": "faciomanuel@gmail.com",
    "Simon": "faciomanuel@gmail.com",
    "Jimena": "faciomanuel@gmail.com",
}

def send_mail(name, day, trash_type):

    body = f"<h3>Hola {name}, hoy es {day}, te toca sacar la basura {trash_type}!</h3><br />May the force be with you!"
    data = {
    'Messages': [
        {
        "From": {
            "Email": "faciomanuel@gmail.com",
            "Name": "Manuel"
        },
        "To": [
            {
            "Email": mail_dict[name],
            "Name": "Manuel"
            }
        ],
        "Subject": "Sacar la basura.",
        "TextPart": "Sacar la basura",
        "HTMLPart": body,
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    return result