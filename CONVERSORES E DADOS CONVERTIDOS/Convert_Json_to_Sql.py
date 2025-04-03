import json

# Arquivos de entrada e saída
arquivo_json = "Clientes_Dados_Complementar.json"
arquivo_oltp_sql = "OLTP_DML_ALTER_CLIENTE.sql"
arquivo_olap_sql = "OLAP_DML_ESTADO_CIVIL.sql"

# Lendo o arquivo JSON
with open(arquivo_json, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Obtem a lista de clientes (evitando erro se não existir a chave)
clientes = dados.get("Cliente", [])

# Simulação da quantidade de clientes existentes no banco (ajuste conforme necessário)
quantidade_clientes_no_banco = 90

# Criação do script para OLAP (não sofreu alterações)
sql_olap = """
CREATE TABLE OLAP_Dim_Estado_Civil (
    ID_Estado_Civil INT PRIMARY KEY,
    Descricao VARCHAR(30) NOT NULL
);
"""

# Obtendo os estados civis únicos, considerando apenas os clientes que serão atualizados
estados_civis_unicos = {cliente.get("Estado_civil", "").strip().replace("'", "''")
                        for cliente in clientes[:quantidade_clientes_no_banco]
                        if cliente.get("Estado_civil", "").strip()}

# Adiciona INSERTs para cada estado civil único
for idx, estado_civil in enumerate(sorted(estados_civis_unicos), start=1):
    if estado_civil == "S":
        sql_olap += f"INSERT INTO OLAP_Dim_Estado_Civil (ID_Estado_Civil, Descricao) VALUES ({idx}, '{"Solteiro"}');\n"
    elif estado_civil == "C":
        sql_olap += f"INSERT INTO OLAP_Dim_Estado_Civil (ID_Estado_Civil, Descricao) VALUES ({idx}, '{"Casado"}');\n"
# Criação do script para OLTP: adiciona o novo campo e atualiza cada registro com o valor do JSON
sql_oltp = """
ALTER TABLE CLIENTES ADD ESTADO_CIVIL VARCHAR(30);
"""

# Para cada registro, gera um comando UPDATE. Se o campo ID_Cliente não existir, utiliza um contador incremental.
for contador, cliente in enumerate(clientes[:quantidade_clientes_no_banco], start=1):
    id_cliente = cliente.get("ID_Cliente") or contador
    estado_civil = cliente.get("Estado_civil", "").strip().replace("'", "''")
    if estado_civil == "S":
        sql_oltp += f"UPDATE CLIENTE SET ESTADO_CIVIL = '{"Solteiro"}' WHERE ID_Cliente = {id_cliente};\n"
    elif estado_civil == "C":
        sql_oltp += f"UPDATE CLIENTE SET ESTADO_CIVIL = '{"Casado"}' WHERE ID_Cliente = {id_cliente};\n"
       
# Salvando os arquivos SQL
with open(arquivo_oltp_sql, "w", encoding="utf-8") as f:
    f.write(sql_oltp)

with open(arquivo_olap_sql, "w", encoding="utf-8") as f:
    f.write(sql_olap)

print(f"Arquivos gerados: {arquivo_oltp_sql}, {arquivo_olap_sql}")
