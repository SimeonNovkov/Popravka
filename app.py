from flask import Flask
from flask import render_template, url_for, request, redirect
from rating import Rating


import logging


app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug') 

logging.basicConfig(filename = 'Info.log', level = logging.INFO)
log.disabled = True

@app.route('/', methods = ['GET', 'POST'])
def new_rating():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		values = (None, request.form['movie'], request.form['rating'])
		rating = Rating(*values).create()
		logging.info('%s created new rating!', rating.movie)
		return redirect('/all')

@app.route('/all')
def get_ratings():
	return render_template('all.html', ratings=Rating.all_ratings())

@app.route('/all/edit/<int:id>', methods = ['GET', 'POST'])
def edit_rating(id):
	if request.method == 'GET':
		rating = Rating.find(id)
		return render_template('edit.html', rating = rating)
	elif request.method == 'POST':
		rating = Rating.find(id)
		rating.rating = request.form['edit_rating'] 
		rating.update()
		logging.info('%s edited rating with id = %d!', rating.movie, rating.id)
		return redirect('/all')

@app.route('/all/delete/<int:id>', methods = ['POST'])
def delete_rating(id):
	rating = Rating.find(id)
	rating.delete()
	logging.info('%s deleted rating with id = %d', rating.movie, id)
	return redirect('/all')


if __name__ == "__main__":
	app.run(debug = True)
