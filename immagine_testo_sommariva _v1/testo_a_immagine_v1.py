import json
import requests
import io
import os
from google.cloud import vision

def detect_text(path):
    """Rileva il testo nell'immagine."""
    client = vision.ImageAnnotatorClient()  # Crea il client per l'API Vision

    # Apre il file immagine in modalità binaria
    with io.open(path, 'rb') as image_file:
        content = image_file.read()  # Legge il contenuto del file immagine

    # Crea un oggetto Image con il contenuto dell'immagine
    image = vision.Image(content=content)

    # Esegue il rilevamento del testo sull'immagine
    response = client.text_detection(image=image)

    # Estrae le annotazioni di testo dalla risposta
    texts = response.text_annotations

    print('Testi rilevati:')  # Stampa l'intestazione dei testi rilevati

    # Cicla attraverso i testi rilevati
    for text in texts:
        a = ("{}".format(text.description))  # Ottieni il testo dalla descrizione
        print(a)  # Stampa il testo rilevato

    # Salva il testo estratto in un file .txt nella cartella TestoEstratto
    output_path = os.path.join("TestoEstratto", "risultato_estratto.txt")
    with open(output_path, "w") as file:
        file.write(a)

# Impostazione del percorso delle credenziali
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "E:\\immagine_testo_sommariva\\API\\service-account-file.json"

# Percorso dell'immagine da analizzare
image_path = "E:\\immagine_testo_sommariva\\Immagine\\immagine_esempio.jpg"

# Chiama la funzione per estrarre il testo dall'immagine
detect_text(image_path)