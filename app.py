from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from functools import reduce

from trajet import Trajet

app = Flask(__name__)
sess = Session(app)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)


@app.route('/', methods=['GET'])
def main():
	t = Trajet([],
			   (session['km_cost'] if (
					   'km_cost' in session and session['km_cost'] is not None and session['km_cost'] > 0) else 1.),
			   (session['departure'] if (
					   'departure' in session and session['departure'] is not None) else 'Toulouse')
			   )
	if 'lines' in session and len(session['lines']) > 1:
		t = Trajet(session['lines'], (session['km_cost'] if (
				'km_cost' in session and session['km_cost'] is not None and session['km_cost'] > 0) else 1.),
				   (session['departure'] if (
						   'departure' in session and session['departure'] is not None) else 'Toulouse')
				   )
	return render_template('index.html', s=session, lines=(session['lines'] if 'lines' in session else []), trajet=t,
						   allocs=(session['alloc'] if 'alloc' in session else []))


@app.route('/ajouter-voyageur')
def add_traveler():
	if 'lines' not in session:
		session['lines'] = []
	session['lines'].append(
		(request.args.get('voyageurs'), request.args.get('arrets'), int(request.args.get('distances'))))
	session['lines'].sort(key=lambda tup: tup[2])

	if 'alloc' in session and len(session['alloc']) > 0:
		session['alloc'] = []
	return redirect("/")


@app.route('/modifier-voyageur')
def edit_traveler():
	session['lines'][int(request.args.get('id'))] = (
		request.args.get('voyageurs'), request.args.get('arrets'), int(request.args.get('distances')))
	session['lines'].sort(key=lambda tup: tup[2])
	return redirect("/")


@app.route('/modifier-allocation')
def edit_alloc():
	values = [float(x) for x in request.args.getlist('alloc_values')]
	session['alloc'][int(request.args.get('id'))] = (
		request.args.get('alloc_name'), values, reduce((lambda x, y: x + y), values))
	return redirect("/")


@app.route('/ajouter-allocation')
def add_alloc():
	if 'alloc' not in session:
		session['alloc'] = []
	values = [float(x) for x in request.args.getlist('alloc_values')]
	session['alloc'].append((request.args.get('alloc_name'), values, reduce((lambda x, y: x + y), values)))
	return redirect("/")


@app.route('/supprimer-voyageur')
def delete_traveler():
	del session['lines'][int(request.args.get('id'))]
	if 'alloc' in session and len(session['alloc']) > 0:
		session['alloc'] = []
	return redirect("/")


@app.route('/configuration')
def config():
	session['km_cost'] = float(request.args.get('km_cost'))
	session['departure'] = request.args.get('departure')
	return redirect("/")


@app.route('/supprimer-allocation')
def delete_alloc():
	del session['alloc'][int(request.args.get('id'))]
	return redirect("/")


if __name__ == '__main__':
	app.run()
