import spacy
import re
import es_core_news_md
from transformers import pipeline
import stanfordnlp
#stanfordnlp.download('es')

# Inicializar el pipeline en español
nlp = stanfordnlp.Pipeline(lang='es')
#import en_core_web_sm
#nlp = spacy.load('en_core_news_sm')
#nlp = es_core_news_md.load() # https://spacy.io/models/es
ner_pipeline = pipeline("ner", model="Davlan/bert-base-multilingual-cased-ner-hrl")
class Extraction:
    def __init__(self, text):
        self.text = text

    def send_extraction(self):
        doc = nlp(self.text.lower())
        clave = ['envia', 'mandar', 'pasar', 'transferir', 'remitir', 'despachar']
        
        for token in doc:
            if token.lemma_ in clave:
                return token.lemma_
        return "No se encuentra envío"

    def mount_extraction(self):
        patron = r'\b\d+'
        #patron = r'\b\d+\s*soles\b'
        #number = patron.split()[1]
        result = re.search(patron, self.text.lower())
        return result.group() if result else "No se encontró monto"

    def name_extraction(self):
        doc = nlp(self.text)
        for entidad in doc.ents:
            #print(entidad)
            if entidad.label_ == 'PER':
                #print(entidad.label_)
                return entidad.text
        return "No se encontró nombre"
    
    def extract_names(self):
        # Aplicar el modelo de NER sobre el texto
        entities = ner_pipeline(self.text)
        names = []
        # Filtrar las entidades que son personas (PER)
        for entity in entities:
            if entity['entity'] == 'b-per':
                names.append(entity['word'])
        
        return names if names else "No se encontró nombre"
    
    def extract_names_stanford(self):
        doc = nlp(self.text)
        names = []
        
        for sentence in doc.sentences:
            for word in sentence.tokens:
                if word.ner == 'PER':  # Verifica si la entidad es de tipo 'PER' (persona)
                    names.append(word.text)
        
        return names if names else "No se encontró nombre"
    
text = "envia 200 soles a mi causa jose garcia"
#PATH = "sql_ai_agent/database_clients.csv"
extraccion = Extraction(text)
#print(extraccion.name_extraction())
#print(extraccion.extract_names())}
print(extraccion.extract_names_stanford())