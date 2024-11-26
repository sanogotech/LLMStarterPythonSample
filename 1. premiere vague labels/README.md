# Premier set de labels

Ce fichier permet de catégoriser automatiquement une première fois des emails à l'aide d'API (Mistral ou Ollama) et de sauvegarder les informations associées dans une base de données Firebase. Il utilise l'API Gmail pour récupérer les emails et analyse les expéditeurs, objets, et contenus pour attribuer des étiquettes aux emails.

## Fonctionnalités

- **Connexion à Gmail** : Extraction des emails via l'API Gmail.
- **Catégorisation automatique** : Utilisation des modèles d'intelligence artificielle Mistral et Ollama pour attribuer des étiquettes aux emails.
- **Sauvegarde sur Firebase** : Les données des emails (ID, thread ID, catégorie, etc.) sont stockées dans Firebase.

## Prérequis

Avant de démarrer, assurez-vous d'avoir les éléments suivants :

- Python 3.x installé.
- Compte Firebase configuré avec un fichier de credentials.
- API Gmail activée dans Google Cloud Console.
- Modèle Mistral ou Ollama configuré avec une clé API.

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone 
   cd email-categorization
2. Installez les dépendances Python :
    ```bash
    pip install -r requirements.txt  
3. Ajoutez vos fichiers de configuration :
    - Placez votre fichier de credentials à la racine de `Première vague labels`.
    - Configurez un fichier credentials.json pour l'API Gmail.
3. Mettez à jour les variables nécessaires :
    - Remplacez `creds_firebase.json` par votre fichier de credentials firebase
    - Ajoutez votre clé API Mistral dans la variable `api_key`.

## Utilisation
Lancez le script principal :
```bash
Copier le code
python3 main.py
```

Le programme effectuera les étapes suivantes :
- Connexion à Gmail pour extraire les emails.
- Analyse et catégorisation des emails.
- Enregistrement des informations dans Firebase.

## Structure du Code
- `main.py` : Point d'entrée principal pour le programme.
- `send_data` : Fonction pour envoyer les données sur Firebase.
- `ollama_getLabel` et `mistral_getLabel` : Intégrations pour catégoriser les emails avec Ollama et Mistral.
- `getID` : Extraction des IDs et threads des emails depuis Gmail.
- `getObjetExpediteur` et `getContenuMail` : Extraction des métadonnées et du contenu des emails.

## Exemple de Configuration Firebase
Assurez-vous d'avoir configuré Firebase avec une base de données en temps réel. Exemple de structure pour les emails :

```json
Copier le code
{
  "emailID": {
    "threadId": "xxx",
    "label_premierTour": "factures"
  }
}