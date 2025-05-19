from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask('Companies')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comp.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    term = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'Company {self.id}: {self.company} term {self.term}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company = request.form['company']
        term = request.form['term']
        new_comp = Company(company=company, term=term)
        db.session.add(new_comp)
        db.session.commit()
        return redirect(url_for('index'))
    
    companies = Company.query.all()
    return render_template('index.html', companies=companies)

@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Company).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)