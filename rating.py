from database import DB

class Rating:
	def __init__(self, id, movie, rating):
		self.id = id
		self.movie = movie
		self.rating = rating

	def create(self):
		with DB() as db:
			values = (self.movie, self.rating)
			db.execute(
				'INSERT INTO ratings (movie, rating) VALUES (?, ?)',
				values
	        )
			return self

	@staticmethod
	def all_ratings():
		with DB() as db:
			rows = db.execute('SELECT * FROM ratings').fetchall()
			print(rows)
			for i in range (0 , len(rows)-1):
                                for j in range (0 , len(rows)-1):
                                        if int(rows[j][2])<int(rows[j+1][2]):
                                                rows[j], rows[j+1] = rows[j+1], rows[j] 


			return [Rating(*row) for row in rows]

	def update(self):
		with DB() as db:
			db.execute('UPDATE ratings SET rating = ? WHERE id = ?', (self.rating, self.id))
			return self

	@staticmethod
	def find(id):
		with DB() as db:
			row = db.execute('SELECT * FROM ratings WHERE id = ?', (id,)).fetchone()
			return Rating(*row)

	def delete(self):
		with DB() as db:
			db.execute('DELETE FROM ratings WHERE id = ?', (self.id,))
