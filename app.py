from flask import Flask, render_template, request, redirect, session, flash, url_for
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change_this_secret"

def load_json(fn):
    return json.load(open(fn)) if os.path.exists(fn) else []

def save_json(fn, data):
    with open(fn, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = load_json('users.json')
        u, p = request.form['username'], request.form['password']
        if any(user['username']==u and user['password']==p for user in users):
            session['user'] = u
            return redirect('/dashboard')
        flash("Invalid username or password")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect('/')
    return render_template(
        'dashboard.html',
        expenses=load_json('expenses.json'),
        tasks=load_json('tasks.json'),
        today=datetime.today().strftime("%Y-%m-%d")
    )

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user' not in session: return redirect('/')
    exp = load_json('expenses.json')
    exp.append({
        "amount": float(request.form['amount']),
        "category": request.form['category'],
        "date": request.form['date'] or datetime.today().strftime("%Y-%m-%d")
    })
    save_json('expenses.json', exp)
    return redirect('/dashboard')

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user' not in session: return redirect('/')
    tk = load_json('tasks.json')
    tk.append({
        "desc": request.form['desc'],
        "due": request.form['due'] or "",
        "priority": request.form['priority'],
        "status": "Pending"
    })
    save_json('tasks.json', tk)
    return redirect('/dashboard')

@app.route('/complete_task/<int:i>')
def complete_task(i):
    if 'user' not in session: return redirect('/')
    tk = load_json('tasks.json')
    if 0 <= i < len(tk): tk[i]['status'] = "Completed"
    save_json('tasks.json', tk)
    return redirect('/dashboard')

@app.route('/delete_task/<int:i>')
def delete_task(i):
    if 'user' not in session: return redirect('/')
    tk = load_json('tasks.json')
    if 0 <= i < len(tk): tk.pop(i)
    save_json('tasks.json', tk)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
