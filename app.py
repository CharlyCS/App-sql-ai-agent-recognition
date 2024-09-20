import pandas as pd
from ai_extraction import Extraction
from speech import transcription

from google.cloud import bigquery

client = bigquery.Client()


text = transcription()
PATH = "sql_ai_agent/database_clients.csv"
extraccion = Extraction(text)
df = pd.read_csv(PATH)


if extraccion.send_extraction().lower() in ["enviar", "mandar", 'envío', 'envio', 'envía']:
    
    full_name = extraccion.name_extraction().strip().split()
    name = full_name[0].capitalize()
    last_name = full_name[1].capitalize()

    for index, row in df.iterrows():
        if row['nombre'] == name and row['apellido'] == last_name:
            amount_init = float(row['Monto'])
            amount_send = float(extraccion.mount_extraction())
            if amount_init >= amount_send:
                new = amount_init - amount_send
                query = f""" UPDATE
                select nombre, apellido, Monto
                from `aiagent.clients`
                where nombre = {name} and apellido = {last_name};"""
                query_job = client.query(query)

            else:
                print("Saldo insuficiente")
                break
