from labels_avant import LABELS, OLD_LABELS
import time
from mistralai import Mistral

api_key = "TA CLÉ D'API"
model = "mistral-large-latest"

"""
def ollama_getLabel(label):
    response = ollama.chat(model='mistral', messages = [
            {
            "role": "user",
            "content": "Peux tu me dire sans justifier et en retorunant uniquement la catégorie si ce label : " + label + " appartient à la catégorie : commercial, newsletter, personnel, service ou autre. Considère qu'un spam est commercial."
            },
        ])
    return response['message']['content']
"""

def mistral_getLabel(label):
    client = Mistral(api_key=api_key)
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
            "role": "user",
            "content": "Peux tu me dire sans justifier et en retorunant uniquement la catégorie si ce label : " + label + " appartient à la catégorie : commercial, newsletter, personnel, service ou autre. Considère qu'un spam est commercial."
            },
        ]
    )
    return chat_response.choices[0].message.content

labels = []
fichier = open("labels_apres.json", "a")
i = len(OLD_LABELS)
for mail_id, info in LABELS.items():
    i += 1
    label = info["label_premierTour"].strip('"').strip("'")
    labelV2 = mistral_getLabel(label)
    print(f"{i}/{len(LABELS) + len(OLD_LABELS)} - {label} : {labelV2}")
    fichier.write(f"\"{mail_id}\" : {{\n\t\t\"label_premierTour\": \"{label}\",\n\t\t\"threadId\": \"{info['threadId']}\",\n\t\t\"label_deuxiemeTour\": \"{labelV2}\"\n\t}},\n")
    time.sleep(1)
fichier.close()






