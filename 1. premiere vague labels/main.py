import base64
import email
import os.path
import ollama
from mistralai import Mistral
import firebase_admin
from firebase_admin import credentials, db

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Setup
cred = credentials.Certificate("creds_firebase.json")
firebase_admin.initialize_app(cred)
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
api_key = "API KEY MISTRAL"
model = "mistral-large-latest"

def send_data(data, i ):
    """Fonction qui envoie les informations sur le mail sur Firebase. 
    1. Extrait l'ID du mail pour en créer le noeud d'accès dans firebase
    2. Supprimer le champ "id" du dictionnaire 
    3. Pousse le dictionnaire dans la firebase

    Args:
        data (dictionnaire): format {'id' : String, 'threadId' : String, 'label_premierTour' : String}
    """
    try:
        mailID = data['id']
        data.pop("id")
        ref = db.reference(f"/{mailID}")
        ref.set(data) 
        ref = db.reference("00-trace")
        ref.set(i)
        print("\tDictionnaire envoyé sur firebase")
    except Exception as e:
        print("Erreur lors de l'insertion :", e)

def getStringEntreDeuxString(chaine1, chaine2, chaine):
    """Fonction qui retorune une chaine de caractère contenue entre deux 
    chaines de caractères

    Args:
        chaine1 (String): Première chaine de caractères
        chaine2 (String): Deuxième Chaine de caractères
        chaine (String): Chaine de caractère contenant chaine1 et chaine2

    Returns:
        String : Chaine de caractère entre chaine1 et chaine2 dans chaine
    """
    indexDebut = chaine.find(chaine1) + len(chaine1)
    indexFin = chaine.find(chaine2, indexDebut)
    return chaine[indexDebut:indexFin]

def ollama_getLabel(expediteur, objet, mail):
    """Fonction qui retorune un label à partir de l'objet et de l'expéditeur
    d'un mail grâce à l'API d'Ollama

    Args:
        expediteur (String): expediteur du mail
        objet (String): objet du mail
        mail (String): contenu du mail

    Returns:
        String : label associé à ce mail
    """
    if not expediteur : 
        expediteur = "expéditeur non trouvé"
    if not objet : 
        objet = "objet non trouvé"
        
    response = ollama.chat(model='mistral', messages=[
        {
            "role": "user",
            "content": """
                Catégorise cet email de manière autonome, et retourne uniquement le mot correspondant à la catégorie que tu as déterminée, sans aucune explication ou texte additionnel.
                
                Voici l'expéditeur : """ + expediteur + """
                Voici l'objet : """ + objet + """

                Retourne simplement la catégorie exacte que tu as trouvée, entre guillemets, sans mise en forme de ta part.
            """
        }
    ])
    return response['message']['content'].strip()  

def mistral_getLabel(expediteur, objet, mail):
    """Fonction qui retorune un label à partir de l'objet et de l'expéditeur
    d'un mail grâce à l'API de Mistral

    Args:
        expediteur (String): expediteur du mail
        objet (String): objet du mail
        mail (String): contenu du mail

    Returns:
        String : label associé à ce mail
    """
    client = Mistral(api_key=api_key)
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
            "role": "user",
            "content": """"
                tu es un assitant de messagerie, ton rôle est de lire un email reçu, de déterminer la catégorie correspondant parmi les situations : 
                    - "newsletter" : si le mail est une newsletter
                    - "factures" : si le mail fait référence à un achat effectué sur internet (facture, confirmation de commande, livraison etc.). 
                    - "poubelle" : si le mail est une publicité
                Si un mail ne fait référence à aucune de ces situations, détermine la catégorie toi-même.

                Voici le format de réponse que tu dois me fournir : "categorie"

                Voici l'expéditeur du mail à catégoriser : """ + expediteur + 
                "Voici l'objet du mail à catégoriser : " + objet +
                "Voici le contenu du mail à catégoriser : " + mail
            },
        ]
    )
    return chat_response.choices[0].message.content

def getID(service): 
    """Fonction qui retourne tous les ID et threadsID de ma boite mail et les enregistre sous 
    forme de tableau dans un fichier id_data.py
    1. Setup la fonction : création du tableau data_id, et configuration du fichier id_data.py pour pouvoir écrire dedans
    2. Récupère tous les "id" et "threadId" de ma boite mail
    3. Enregistre "id" et "threadId" dans id_data puis passe à la page suivante
    
    Returns:
        Table : [{"id" : id, "threadId" : threadId, "label_premierTour": ""}, ...]
    """
    data_ID = []
    fichierID = open("id_data.py", "a")
    fichierID.write("DATA = [")

    i = 0
    print(f"Page {i}")

    message = service.users().messages().list(userId="me").execute()
    for msg in message["messages"]:
        id = msg["id"]
        threadId = msg["threadId"]
        data_ID.append({"id" : id, "threadId" : threadId, "label_premierTour": ""})
    
    while "nextPageToken" in message:
        message = service.users().messages().list(userId="me", pageToken=message["nextPageToken"]).execute()
        for msg in message["messages"]:
            id = msg["id"]
            threadId = msg["threadId"]
            data_ID.append({"id" : id, "threadId" : threadId})
            fichierID.write(f"{{'id' : \"{id}\", 'threadId' : \"{threadId}\"}},\n")
        i += 1
        print(f"Page {i}")
    
    fichierID.write("]")
    fichierID.close()
    return(data_ID)

def getObjetExpediteur(service, mailID):
    """Fonction qui retourne l'objet et l'expediteur d'un mail en fonction de l'id d'un 
    mail avec l'API de gmail

    Args:
        service (): 
        mailID (String): ID du mail dans l'API Gmail

    Returns:
        Table: [objet, expediteur]
    """
    msg = service.users().messages().get(userId="me", id=mailID, format='metadata').execute()
    headers = msg.get("payload", {}).get("headers", [])
    
    expediteur = None
    objet = None
    
    for header in headers:
        if header.get("name") == "From":
            expediteur = header.get("value")
        elif header.get("name") == "Subject":
            objet = header.get("value")

    return [objet, expediteur]

def getContenuMail(service, mailID):
    """Fonction qui retourne le contenu d'un mail (texte) à partir de l'id d'un mail
    grâce à l'API de gmail. Décodage de l'encodement du mail pour afficher une chaîne
    de caractère classique que l'on peut lire sans problème.

    Args:
        service (): 
        mailID (String): id du mail

    Returns:
        String: contenu du mail
    """
    message = service.users().messages().get(userId="me", id=mailID, format='raw').execute()
    msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8", errors='replace')
    mime_msg = email.message_from_string(msg_str)

    contenuMail = ""
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                contenuMail = part.get_payload(decode=True)
                if contenuMail: 
                    contenuMail = contenuMail.decode('utf-8', errors='replace')
                    break 
    else:
        contenuMail = mime_msg.get_payload(decode=True)
        if contenuMail: 
            contenuMail = contenuMail.decode('utf-8', errors='replace')

    return contenuMail if contenuMail else "Contenu de l'e-mail introuvable"

def main():
    # Setup API
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
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        # service = build("gmail", "v1", credentials=creds)
        # getID(service)
        fichier = open("data.txt", "a")
        service = build("gmail", "v1", credentials=creds)
        
        dataFirebase = {}
        data = getID(service)
        i = 0
        tailleTotale = len(data)
        for mail in data:
            i += 1
            objet = getObjetExpediteur(service, mail["id"])[0]
            expediteur = getObjetExpediteur(service, mail["id"])[1]
            contenuMail = getContenuMail(service, mail["id"])
            label = mistral_getLabel(expediteur, objet, contenuMail)
            # label = ollama_getLabel(expediteur, objet, contenuMail)
            mail["label_premierTour"] = label
            print(f"{i}/{tailleTotale} - {expediteur} + {objet}")
            print(f"\t{{'id' : '{mail['id']}', 'threadId' : '{mail['threadId']}', 'label_premierTour' : '{label}'}},")
            dataFirebase = {"id" : mail["id"], 'threadId' : mail['threadId'], "label_premierTour" : label}
            send_data(dataFirebase, i)
        fichier.close()
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
