import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from labels import LABELS

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def defineLabel(name, mlv="show", llv="labelShow"):
    """Crée un dictionnaire représentant un label pour Gmail.

    Args:
        name (str): Le nom du label à créer.
        mlv (str, optional): Détermine si le label est visible dans la liste des messages. Valeur par défaut : "show".
        llv (str, optional): Détermine si le label est visible dans l'interface utilisateur de Gmail. Valeur par défaut : "labelShow".

    Returns:
        dict: Un dictionnaire représentant le label.
    """
    label = dict()
    label["messageListVisibility"] = mlv
    label["labelListVisibility"] = llv
    label["name"] = name
    return label

def addLabelToGmail(service, label):
    """Ajoute un label à un compte Gmail.

    Args:
        service: Objet service de l'API Gmail.
        label (dict): Un dictionnaire représentant le label à créer.

    Returns:
        dict: Les détails du label créé dans Gmail.
    """
    try:
        created_label = service.users().labels().create(userId='me', body=label).execute()
        print(f"{label} : \t\nlabel créé dans gmail")
        return created_label
    except Exception as e:
        print(f"erreur : {e}")

def getNewLabelDd(new_label):
    """Récupère l'ID d'un label Gmail créé.

    Args:
        new_label (dict): Dictionnaire contenant les informations du label.

    Returns:
        string: L'ID du label.
    """
    return new_label.get('id')

def manageLabels(service, msg_id, labelID_ajouter):
    """Ajoute un label à un email Gmail et retire le label "INBOX".

    Args:
        service: Objet service de l'API Gmail.
        msg_id (str): L'ID du message auquel le label doit être ajouté.
        labelID_ajouter (str): L'ID du label à ajouter.
    """
    try:
        msg = service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ["INBOX"], 'addLabelIds': [labelID_ajouter]}).execute()
        print(f"{labelID_ajouter} et {msg_id} : \t\nlabel ajouté au mail")
    except Exception as e:
        print(f"erreur dans l'ajout d'un mail à un label : {e}")

def main():
    """
    Programme qui :
    - Initialise l'API Gmail.
    - Catégorise et applique des labels prédéfinis aux emails en fonction des résultats d'analyse.

    Steps:
        1. Vérifie si des credentials Gmail existent, sinon les génère.
        2. Configure l'accès au service Gmail via l'API.
        3. Définit les labels pour les catégories "commercial", "service", "personnel", "newsletter" et "autre".
        4. Parcourt les emails définis dans LABELS.
        5. Associe un label à chaque email selon sa catégorie analysée ("label_deuxiemeTour").
        6. Affiche les emails non catégorisés.
    """
    # préparation de l'API
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Initialisation du service Gmail
    service = build("gmail", "v1", credentials=creds)

    try:
        labels = {
            "commercial" : "Label_87",
            "service" : "Label_88",
            "personnel" : "Label_89",
            "newsletter" : "Label_90",
            "autre" : "Label_91"
        }

        i = 0
        ids = LABELS.keys()
        labelsOrphelins = []
        for id in ids:
            i += 1
            match LABELS[id]["label_deuxiemeTour"]:
                case "commercial":
                    print(f"{i}/{len(LABELS)} - {id} : {LABELS[id]["label_deuxiemeTour"]}")
                    manageLabels(service, id, labels["commercial"])
                case "service":
                    print(f"{i}/{len(LABELS)} - {id} : {LABELS[id]["label_deuxiemeTour"]}")
                    manageLabels(service, id, labels["service"])
                case "personnel":
                    print(f"{i}/{len(LABELS)} - {id} : {LABELS[id]["label_deuxiemeTour"]}")
                    manageLabels(service, id, labels["personnel"])
                case "newsletter":
                    print(f"{i}/{len(LABELS)} - {id} : {LABELS[id]["label_deuxiemeTour"]}")
                    manageLabels(service, id, labels["newsletter"])
                case "autre":
                    print(f"{i}/{len(LABELS)} - {id} : {LABELS[id]["label_deuxiemeTour"]}")
                    manageLabels(service, id, labels["autre"])
                case _:
                    labelsOrphelins.append(id)
                    print("label non catégorisé")
        print(labelsOrphelins)
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
