CREATE TABLE typ (
    typ_id INTEGER AUTOINCREMENT PRIMARY KEY,
    ksztalt VARCHAR(100) NOT NULL,
    kolor VARCHAR(100) NOT NULL,
    efekt_wykonczenia VARCHAR(100),
    rozmiar FLOAT NOT NULL,
    ilosc SMALLINT NOT NULL,
    cena FLOAT NOT NULL,
    inne JSON DEFAULT('[]')
);