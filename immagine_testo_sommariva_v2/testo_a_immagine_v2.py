import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import io
from google.cloud import vision

# Funzione per rilevare il testo e salvarlo in un file .txt
def detect_text(image_path):
    """Rileva il testo nell'immagine e lo salva in un file .txt"""
    # Crea un client per l'API Google Cloud Vision
    client = vision.ImageAnnotatorClient()

    # Apre l'immagine in modalità binaria
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Crea un oggetto Image con il contenuto dell'immagine
    image = vision.Image(content=content)

    # Chiama l'API Vision per eseguire il rilevamento del testo
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        messagebox.showerror("Errore", "Nessun testo rilevato nell'immagine.")
        return None

    # Estrai il testo rilevato
    extracted_text = texts[0].description

    # Crea la cartella di output se non esiste
    output_dir = "TestiEstratti"
    os.makedirs(output_dir, exist_ok=True)

    # Estrae solo il nome del file immagine senza estensione
    image_filename = os.path.basename(image_path)
    base_name = os.path.splitext(image_filename)[0]

    # Percorso del file .txt di output
    output_path = os.path.join(output_dir, base_name + ".txt")

    # Scrive il testo estratto nel file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    return output_path

# Funzione chiamata dal pulsante per caricare l'immagine
def load_image():
    # Apre il file dialog per selezionare un'immagine
    file_path = filedialog.askopenfilename(filetypes=[("Immagini", "*.jpg;*.jpeg;*.png;*.gif")])
    
    if file_path:
        image_path_var.set(file_path)  # Imposta il percorso dell'immagine nell'entry
        message_label.config(text="Immagine pronta per l'elaborazione!")

# Funzione per eseguire l'analisi OCR e salvare il testo
def process_image():
    image_path = image_path_var.get()
    if not image_path:
        messagebox.showwarning("Avviso", "Seleziona un'immagine prima di procedere.")
        return

    output_path = detect_text(image_path)

    if output_path:
        messagebox.showinfo("Successo", f"Testo estratto e salvato in: {output_path}")
        message_label.config(text=f"File salvato in: {output_path}")
    else:
        message_label.config(text="Errore durante l'estrazione del testo.")

# Imposta la finestra principale
root = tk.Tk()
root.title("OCR con Google Vision API")
root.geometry("600x350")
root.config(bg="#f7f7f7")  # Colore di sfondo

# Stile personalizzato per i widget
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat", background="#4CAF50", foreground="black")
style.map("TButton", background=[("active", "#45a049")])
style.configure("TEntry", font=("Helvetica", 12), padding=5, relief="solid", borderwidth=2)
style.configure("TLabel", font=("Helvetica", 14), background="#f7f7f7", foreground="#333")

# Variabile per il percorso dell'immagine
image_path_var = tk.StringVar()

# Etichetta per l'immagine selezionata
image_label = ttk.Label(root, text="Seleziona un'immagine:", anchor="w")
image_label.pack(pady=10, padx=20, fill="x")

# Entry per visualizzare il percorso dell'immagine
image_entry = ttk.Entry(root, textvariable=image_path_var, width=40)
image_entry.pack(pady=5, padx=20)

# Pulsante per caricare l'immagine
load_button = ttk.Button(root, text="Carica Immagine", command=load_image)
load_button.pack(pady=15)

# Pulsante per avviare l'analisi OCR
process_button = ttk.Button(root, text="Elabora Immagine", command=process_image)
process_button.pack(pady=15)

# Etichetta per mostrare lo stato dell'operazione
message_label = ttk.Label(root, text="Pronto per l'elaborazione", anchor="center")
message_label.pack(pady=10, padx=20, fill="x")

# Avvia la GUI
root.mainloop()
