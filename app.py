from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class StudyLog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  subject = db.Column(db.String(100), nullable=False)
  duration = db.Column(db.Float, nullable=False)  # Duration in hours
  date = db.Column(db.String(20), nullable=False)


with app.app_context():
  db.create_all()


@app.route('/')
def index():
  logs = StudyLog.query.all()
  total_hours = sum(log.duration for log in logs)
  return render_template('index.html', logs=logs, total_hours=round(total_hours, 2))


@app.route('/add', methods=['POST'])
def add_log():
  subject = request.form.get('subject')
  duration = float(request.form.get('duration', 0))
  date = request.form.get('date') or datetime.now().strftime('%Y-%m-%d')

  new_log = StudyLog(subject=subject, duration=duration, date=date)
  db.session.add(new_log)
  db.session.commit()
  return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['POST'])
def delete_log(id):
  log = StudyLog.query.get_or_404(id)
  db.session.delete(log)
  db.session.commit()
  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True)
