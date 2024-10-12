from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Charger la clé API depuis .env
load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

# Route pour récupérer la définition d'un mot
@app.route('/definition/<word>', methods=['GET'])
def get_definition(word):
    # URL de l'API Merriam-Webster avec la clé API
    api_url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={API_KEY}"

    # Faire la requête à l'API
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()

        # Vérifier si la réponse contient des définitions valides
        if data and isinstance(data, list) and "shortdef" in data[0]:
            definitions = data[0]["shortdef"]  # Récupérer les définitions courtes
            return jsonify({"word": word, "definitions": definitions}), 200
        else:
            return jsonify({"error": "Definition not found"}), 404
    else:
        return jsonify({"error": "API request failed"}), 500

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
