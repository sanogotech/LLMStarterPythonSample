# Application des labels sur ta boite mail

Ce script permet d'appliquer les labels obtenus dans la deuxieme vague

## 😱 Fonctionnalités

- **Création de labels Gmail** : Définir des labels personnalisés dans Gmail.
- **Application de labels aux emails** : Associer des labels à des emails en fonction de leur catégorie.
- **Catégories prises en charge** :
  - `commercial`
  - `service`
  - `personnel`
  - `newsletter`
  - `autre`
- **Gestion des emails non catégorisés** : Identifie les emails qui ne correspondent à aucune des catégories définies.

## 😳 Prérequis

Avant de commencer, assurez-vous d'avoir :

1. **Python 3.x** installé sur votre machine.
2. Une configuration d'API Google pour accéder à Gmail :
   - Créez un projet dans [Google Cloud Console](https://console.cloud.google.com/).
   - Activez l'API Gmail.
   - Téléchargez un fichier `credentials.json` et placez-le dans le répertoire racine du projet.
3. Les bibliothèques Python nécessaires :
   - Installez-les via le fichier `requirements.txt` :
     ```bash
     pip install -r requirements.txt
     ```

## 🫡 Installation

1. Clonez le dépôt :
   ```bash
   git clone hhttps://github.com/solene-drnx/Beemail---public.git
   cd "3. appliquer les labels"
2. Placez le fichier credentials.json dans le répertoire principal.
3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 🤩 Utilisation
1. Lancez le script principal :
```bash
python3 main.py
```
2. Fonctionnement :
Le script initialise l'authentification avec l'API Gmail.
Les emails sont parcourus en fonction des informations contenues dans le fichier labels.py.
Chaque email reçoit un label approprié en fonction de sa catégorie.
Les emails non catégorisés sont listés pour un traitement manuel.

3. Fichier d'entrée : `labels.py`
Contient les emails et leurs catégories à traiter. Format :
```python
LABELS = {
	"14cd8333fblablabla": {
		"label_premierTour": "Notification",
		"threadId": "14cd8333fbcblablabla",
		"label_deuxiemeTour": "commercial"
	},
	"14e2b708cablablabla": {
		"label_premierTour": "Spam (non sollicitation commerciale)",
		"threadId": "14e2b708cafablablabla",
		"label_deuxiemeTour": "commercial"
	},
    ...
}
```
## 🫣 Exemple de Résultat
Lors de l'exécution, le script affiche les étapes du traitement :
```less
1/100 - email_id_1 : commercial
Label ajouté avec succès !
2/100 - email_id_2 : service
Label ajouté avec succès !
...
Emails non catégorisés : ['email_id_101', 'email_id_102']
```
