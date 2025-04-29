# Progetto OCR - Estrazione Testo da Immagini  
### Autore: Enrico Sommariva (Classe 3INF4)

---

## 📌 Descrizione del Progetto

Questo è un progetto scolastico che permette di **estrarre automaticamente il testo da immagini** utilizzando l'**API di Google Cloud Vision**.  
L'immagine viene analizzata con tecniche di **OCR (Optical Character Recognition)** e il testo viene poi **salvato in un file `.txt`**.

È disponibile una versione **a riga di comando** e una con **interfaccia grafica (GUI) con Tkinter**, per rendere l'utilizzo più accessibile.

Il progetto permette all'utente di:
- Caricare e analizzare immagini contenenti testo (es. fotografie di documenti, testi scritti a mano, ecc.)
- Visualizzare a schermo il testo riconosciuto
- Salvare automaticamente il testo in un file `.txt` nella cartella `TestoEstratto`

---

## 🗂️ Struttura del Progetto
**VERSIONE 1 - "a riga di comando"**

![image](https://github.com/user-attachments/assets/cf1d1f4c-4116-4cc2-8d6b-9c1d64a6e172)
**VERSIONE 2 - "GUI Tkinter"**

![image](https://github.com/user-attachments/assets/944ae415-7b84-4891-b1b1-171740fff7cb)

---

## 🛠️ Come Configurare l'API di Google Vision

1. Vai su: [console.cloud.google.com](https://console.cloud.google.com/)
2. Crea un nuovo progetto.
3. Vai su **"API e Servizi" > "Libreria"** e abilita la **Google Cloud Vision API**.
4. Vai su **"Credenziali" > "Crea credenziali" > "Account di servizio"**.
5. Dopo aver creato l’account, clicca su **“Chiave”** e scarica il file `.json`.
6. Metti quel file nella cartella `API/` del progetto.

---

## 💻 Versione 1 (Riga di Comando)

### ▶️ Codice

```python
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
```

Questa versione permette all'utente di:
- Impostare manualmente il percorso di immagine e credenziali
- Analizzare l'immagine e visualizzare il testo estratto nel terminale
- Salvare il risultato in `TestoEstratto/risultato_estratto.txt`

---

## 🖼️ VERSIONE 2 -Interfaccia Grafica

![Immagine 2025-04-29 194032](https://github.com/user-attachments/assets/191a3e50-e1e2-4d43-b3e7-920ca68d79c4)

Permette all'utente di:
- Caricare un’immagine da una finestra di dialogo.
- Avviare il processo OCR con un clic.
- Salvare il testo automaticamente in un file `.txt`.

### ▶️ Codice

```python
import tkinter as tk
from tkinter import filedialog
from google.cloud import vision
import os
import io

# Imposta le credenziali Google
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "API/chiave_google.json"

def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        with open("TestoEstratto/risultato.txt", "w", encoding="utf-8") as f:
            for text in texts:
                f.write(text.description + "\n")
        return texts[0].description
    else:
        return "Nessun testo rilevato."

def carica_immagine():
    filepath = filedialog.askopenfilename()
    if filepath:
        label_immagine.config(text=f"Immagine selezionata:\n{filepath}")
        return filepath
    return None

def elabora_immagine():
    filepath = carica_immagine()
    if filepath:
        testo = detect_text(filepath)
        label_risultato.config(text="Testo estratto:\n" + testo)

# Interfaccia Grafica
root = tk.Tk()
root.title("OCR - Riconoscimento Testo da Immagine")
root.geometry("500x300")

label_immagine = tk.Label(root, text="Seleziona un'immagine", wraplength=480)
label_immagine.pack(pady=10)

button_carica = tk.Button(root, text="Carica Immagine", command=carica_immagine, fg="black")
button_carica.pack()

button_elabora = tk.Button(root, text="Elabora Immagine", command=elabora_immagine, fg="black")
button_elabora.pack(pady=5)

label_risultato = tk.Label(root, text="Testo rilevato apparirà qui", wraplength=480)
label_risultato.pack(pady=20)

root.mainloop()
```

---

## ✅ Requisiti

- Python 3.x
- Google Cloud Vision API attiva
- File `.json` delle credenziali di servizio
- Librerie Python:
  - `google-cloud-vision`
  - `tkinter` (incluso in Python)

### Installazione della libreria "CLOUD-VISION"

```bash
pip install google-cloud-vision
```

---

## 🧪 Output Aspettato

Esempio di output dopo l’elaborazione:

```
Testo estratto:
Art. 1
L’Italia è una Repubblica democratica fondata sul lavoro...
```

![Costituzione_b_gr](https://github.com/user-attachments/assets/f100846e-809f-4d81-b71d-e32f55b0402a)


![image](https://github.com/user-attachments/assets/dd69fdd4-0ddb-47f5-a844-7753ded5d3a2)



Il file `risultato.txt` o `risultato_estratto.txt` sarà salvato nella cartella `TestoEstratto/`.




---

## 📌 Conclusioni

Questo progetto dimostra l’utilizzo pratico dell’intelligenza artificiale per l’analisi automatica di testi da immagini.  
Sfruttando l’API di Google Cloud Vision, è stato possibile implementare sia un sistema a riga di comando, sia uno dotato di interfaccia grafica intuitiva.

La struttura del progetto è pensata per essere facilmente estendibile e adattabile ad altri contesti: archiviazione documentale, lettura da immagini scansionate, digitalizzazione di testi scolastici, ecc.

Il lavoro ha richiesto comprensione del funzionamento delle API, gestione dei file, e utilizzo di librerie grafiche con Python.

---

## 🎓 Crediti

**Realizzato da**: Enrico Sommariva  
**Classe**: 3INF4  
**Scopo**: Progetto scolastico interdisciplinare
