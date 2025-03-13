import numpy as np
import sqlite3
import pandas as pd

# Função para conectar ao banco de dados SQLite
def conectar_banco_de_dados():
    return sqlite3.connect('projeto_teste.db')

# Carregar o dataset
df = pd.read_csv("projeto _1_diabete/diabetes.csv")

# Criar conexão com o banco
conn = conectar_banco_de_dados()

# Salvar DataFrame no banco SQLite
df.to_sql("diabetes", conn, if_exists="replace", index=False)

# Consultar pacientes com glicose maior que 190
query = "SELECT Age, Glucose, Outcome FROM diabetes WHERE Glucose > 190"
df_glicose_alta = pd.read_sql(query, conn)
print(df_glicose_alta)

# Fechar a conexão
conn.close()

# Criar tabela de pacientes
create_table_query = """
CREATE TABLE pacientes (
    Pregnancies INT,
    Glucose INT,
    BloodPressure INT,
    SkinThickness INT,
    Insulin INT,
    BMI DECIMAL(8, 2),
    DiabetesPedigreeFunction DECIMAL(8, 2),
    Age INT,
    Outcome INT
);
"""
conn = conectar_banco_de_dados()
cursor = conn.cursor()
cursor.execute(create_table_query)
conn.commit()
conn.close()

# Inserir dados de pacientes com idade superior a 50 anos
insert_query = """
INSERT INTO pacientes (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome) 
SELECT Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome 
FROM diabetes WHERE Age > 50;
"""
conn = conectar_banco_de_dados()
cursor = conn.cursor()
cursor.execute(insert_query)
conn.commit()
conn.close()

# Consultar todos os pacientes
query = "SELECT * FROM pacientes"
conn = conectar_banco_de_dados()
consultar_pacientes = pd.read_sql(query, conn)
print(consultar_pacientes)
conn.close()

# Adicionar coluna 'perfil'
add_coluna_perfil = "ALTER TABLE pacientes ADD perfil VARCHAR(10)"
conn = conectar_banco_de_dados()
cursor = conn.cursor()
cursor.execute(add_coluna_perfil)
conn.commit()
conn.close()

# Atualizar a coluna 'perfil'
alimentar_coluna_perfil = "UPDATE pacientes SET perfil = 'normal' WHERE BMI < 30"
conn = conectar_banco_de_dados()
cursor = conn.cursor()
cursor.execute(alimentar_coluna_perfil)
conn.commit()
conn.close()

# Criar DataFrame com os dados da tabela 'pacientes'
conn = conectar_banco_de_dados()
cursor = conn.cursor()
cursor.execute("SELECT * FROM pacientes")
colunas = [coluna[0] for coluna in cursor.description]
novo_dataframe = pd.DataFrame.from_records(data=cursor.fetchall(), columns=colunas)
conn.close()

# Exportar para CSV
novo_dataframe.to_csv("pacientes.csv", index=False, encoding="utf-8")
