DROP TABLE IF EXISTS favorites;

CREATE TABLE IF NOT EXISTS favorites (
	favorite_id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL DEFAULT 0,
	film_id INTEGER NOT NULL,
	FOREIGN KEY (film_id)
		REFERENCES films(film_id)
			ON DELETE CASCADE
);

INSERT INTO favorites (user_id, film_id)
VALUES (1, 1),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(2, 1),
(1, 2),
(3, 7),
(2, 10),
(3, 21);