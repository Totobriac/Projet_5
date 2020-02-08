

CREATE TABLE IF NOT EXISTS off(
    marque VARCHAR(200) NOT NULL,
    nom VARCHAR(200) NOT NULL,
    nutriscore VARCHAR(5),
    store VARCHAR(200) NOT NULL,
    category VARCHAR(20),
    code_id BIGINT, 
    productID int PRIMARY KEY AUTO_INCREMENT)""")


INSERT INTO off (marque, nom, nutriscore, store, category, code_id)
                 VALUES (%s,%s,%s,%s,%s,%s)",
                 (marque, nom, nutriscore, store, category, code_id)


CREATE TABLE IF NOT EXISTS substitute (
    nom VARCHAR(100),
    marque VARCHAR(100),
    category VARCHAR(20),
    nutriscore VARCHAR(1),
    store VARCHAR(100), code_id BIGINT)
            
INSERT INTO substitute (marque, nom, nutriscore, store, code_id)
			SELECT marque, nom, nutriscore, store,
                    	code_id FROM off WHERE productID= %s)
