from flask import Flask, render_template, request, redirect, url_for, session, flash
from blockchain import Blockchain
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
blockchain = Blockchain()

# In-memory storage for users and candidates
users = {
    'admin@gmail.com': {'password': 'admin', 'is_admin': True}  # Predefined admin user
}
candidates = {}
votes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        id_photo = request.files['id_photo']
        city = request.form['city']
        job = request.form['job']

        if email in users:
            flash('Email already registered.')
            return redirect(url_for('register'))

        users[email] = {
            'name': name,
            'surname': surname,
            'dob': dob,
            'password': password,
            'id_photo': id_photo,
            'city': city,
            'job': job,
            'is_admin': False
        }
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['logged_in'] = True
            session['email'] = email
            if users[email]['is_admin']:
                session['admin'] = True
                return redirect(url_for('admin'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        candidate = request.form['candidate']
        if candidate in votes:
            votes[candidate] += 1
        else:
            votes[candidate] = 1
        blockchain.add_vote(candidate)
        flash('Vote successfully cast.')
        return redirect(url_for('vote'))
    return render_template('vote.html', candidates=candidates)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session or not users.get(session['email'], {}).get('is_admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        candidate_name = request.form['candidate']
        candidates[candidate_name] = candidates.get(candidate_name, 0)
        flash(f'Candidate {candidate_name} added.')
        return redirect(url_for('admin'))
    return render_template('admin.html', candidates=candidates)

@app.route('/results')
def results():
    return render_template('results.html', votes=votes, chain=blockchain.chain)

@app.route('/end_vote')
def end_vote():
    if 'logged_in' not in session or not users.get(session['email'], {}).get('is_admin'):
        flash('Access denied. Please log in as an administrator.')
        return redirect(url_for('login'))
    flash('Voting has ended. Results are published.')
    return redirect(url_for('results'))

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
