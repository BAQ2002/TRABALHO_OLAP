
CREATE TABLE OLAP_Dim_Estado_Civil (
    ID_Estado_Civil INT PRIMARY KEY,
    Descricao VARCHAR(30) NOT NULL
);
INSERT INTO OLAP_Dim_Estado_Civil (ID_Estado_Civil, Descricao) VALUES (1, 'Casado');
INSERT INTO OLAP_Dim_Estado_Civil (ID_Estado_Civil, Descricao) VALUES (2, 'Solteiro');
