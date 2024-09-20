import spacy
import re
import es_core_news_md
import unicodedata
#nlp = spacy.load('en_core_news_sm')
nlp = es_core_news_md.load() # https://spacy.io/models/es

def remove_accents(input):
    tilde = unicodedata.normalize('NFKD', input)
    return "".join([c for c in tilde if not unicodedata.combining(c)])

class Extraction:
    def __init__(self, text):
        self.text = text

    def send_extraction(self):
        doc = nlp(self.text.lower())
        clave = ['enviar', 'envío', 'envio', 'envía', 'mandar', 'pasar', 'transferir', 'remitir', 'despachar']
        for token in doc:
            if token.lemma_ in clave:
                return token.lemma_
        return "No se encuentra envio"

    def mount_extraction(self):
        patron = r'\b\d+'
        result = re.search(patron, self.text.lower())
        return result.group() if result else "No se encontró monto"

    def name_extraction(self):
        doc = nlp(self.text)
        for entidad in doc.ents:
            if entidad.label_ == 'PER':
                word = remove_accents(entidad.text)
                return word
        return "No se encontró nombre"