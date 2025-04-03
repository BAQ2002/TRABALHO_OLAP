import pandas as pd

# Caminho dos arquivos - exemplo abaixo.
arquivo_xls = "Concorrente.xls"
arquivo_sql = "Concorrente.sql"

# Carregar o Excel
df = pd.read_excel(arquivo_xls, engine="xlrd")

# Função para converter mês em quadrimestre
def mes_para_quadrimestre(mes):
    if 1 <= mes <= 4:
        return 1
    elif 5 <= mes <= 8:
        return 2
    elif 9 <= mes <= 12:
        return 3
    else:
        return None  # Caso de erro

# Criar o arquivo SQL
with open(arquivo_sql, "w") as f:
    # Criar a tabela
    f.write("""
    CREATE TABLE Concorrente_Vendas (
        ID_Concorrente INT NOT NULL,
        Ano INT NOT NULL,
        Quadrimestre INT NOT NULL,
        Valor DECIMAL(10,2),
        Quantidade INT NOT NULL
    );
    ALTER TABLE Concorrente_Vendas ADD CONSTRAINT PK_Concorrente_Vendas PRIMARY KEY (ID_Concorrente);
    """.strip() + "\n\n")
    
    # Inserir dados
    ID = 1
    for _, row in df.iterrows():
        quadrimestre = mes_para_quadrimestre(row['Mês'])
        if quadrimestre is not None:
            sql = f"INSERT INTO Concorrente_Vendas (ID_Concorrente, Ano, Quadrimestre, Valor, Quantidade) " \
                  f"VALUES ({ID}, {row['Ano']}, {quadrimestre}, {row['Valor']}, {row['Quantidade']});\n"
            f.write(sql)
            ID += 1

print(f"Arquivo SQL gerado: {arquivo_sql}")
