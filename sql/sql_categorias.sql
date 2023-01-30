CREATE TABLE categorias(
	nome_produto varchar(255) not null,
	categoria varchar(255) not null
)

INSERT INTO categorias(nome_produto, categoria)
VALUES 
('Geladeira', 'Eletrodomésticos'),
('iPhone', 'Eletrônicos'),
('Macbook', 'Eletrônicos'),
('Tablet', 'Eletrônicos')