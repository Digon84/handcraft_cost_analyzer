CREATE TABLE items (material VARCHAR(100) NOT NULL, type VARCHAR(100) NOT NULL, shape VARCHAR(100) NOT NULL, color VARCHAR(40) NOT NULL, finishing_effect VARCHAR(100) NOT NULL, size FLOAT NOT NULL, amount SMALLINT NOT NULL, other JSON DEFAULT('[]'), unit_price FLOAT NOT NULL, total_price FLOAT NOT NULL, CONSTRAINT bead_key)
