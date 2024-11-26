# Label Categorization with Mistral AI

Ce script nettoie les labels récupéré apres le premier tour de labels avec l'IA. Il parcourt une liste de labels issus de `1. premiere vague labels`, les analyse à l'aide du modèle Mistral, et génère une sortie catégorisée dans un fichier JSON.

## 🥰 Fonctionnalités

- **Analyse de labels** : Le script prend en entrée des labels et les attribue à l'une des catégories suivantes :
  - `commercial`
  - `newsletter`
  - `personnel`
  - `service`
  - `autre` (pour les labels ne correspondant à aucune des catégories principales)
  - Les spams sont automatiquement classés comme `commercial`.

- **Enregistrement des résultats** : Les résultats sont enregistrés dans un fichier `labels_apres.json`, incluant les informations suivantes :
  - Label initial (`label_premierTour`)
  - Thread ID
  - Label catégorisé après analyse (`label_deuxiemeTour`).

## 🤓 Prérequis

Avant d'exécuter ce script, assurez-vous d'avoir :

1. Python 3.x installé.
2. La bibliothèque `mistralai` installée :
   ```bash
   pip install mistralai
3. Un fichier labels_avant.py contenant les données `LABELS`récupérés depuis firebase
4. Une clé API valide pour le modèle Mistral.

## 🧐 Installation

1. Clonez ce dépôt ou copiez le script.
2. Placez votre clé API dans la variable api_key du script.
3. Vérifiez que le fichier `labels_avant.py` est structuré comme suit :

```python
LABELS = {
    "mail_id_1": {"label_premierTour": "label1", "threadId": "thread1"},
    "mail_id_2": {"label_premierTour": "label2", "threadId": "thread2"},
    ...
}
```

## 😝 Utilisation
1. Lancez le script en exécutant la commande suivante dans votre terminal :
```bash
python main.py
```
2. Processus : Chaque label dans `labels_avant.py` est analysé avec le modèle Mistral via l'API.
Une pause de 1 seconde est incluse entre chaque requête pour éviter les dépassements de limite de l'API.
Les résultats sont enregistrés dans le fichier `labels_apres.json`.
3. Format de sortie : Exemple de structure dans `labels_apres.json` :
```json
{
    "mail_id_1": {
        "label_premierTour": "label1",
        "threadId": "thread1",
        "label_deuxiemeTour": "newsletter"
    },
    "mail_id_2": {
        "label_premierTour": "label2",
        "threadId": "thread2",
        "label_deuxiemeTour": "commercial"
    }
}
```