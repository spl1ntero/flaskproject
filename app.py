from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:15931@localhost/my_database7'
db = SQLAlchemy(app)
Bootstrap(app)


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pulse = db.Column(db.String(100), nullable=False)
    pressure = db.Column(db.String(500), nullable=False)
    sugar = db.Column(db.String(500), nullable=False)
    hemoglobin = db.Column(db.String(500), nullable=False)


class RegistrationForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    pulse = IntegerField('Ваш пульс в данный момент', validators=[DataRequired()])
    pressure = FloatField(
        'Ваше давление в данный момент.',
        validators=[DataRequired()])
    sugar = IntegerField(
        'Ваш уровень сахара в данный момент.',
        validators=[DataRequired()]
    )
    hemoglobin = IntegerField(
        'Ваш уровень гемоглобина в данный момент.',
        validators=[DataRequired()]
    )
    submit = SubmitField('Отправить')


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)


class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Ваша почта', validators=[DataRequired()])
    message = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


name = Registration.name


@app.route('/')
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        registration = Registration(name=form.name.data, pulse=form.pulse.data, pressure=form.pressure.data,
                                    sugar=form.sugar.data, hemoglobin=form.hemoglobin.data)
        db.session.add(registration)
        db.session.commit()
        flash('Registration data submitted successfully!')
        redirect('/show')
    return render_template('reg.html', form=form, title="Ввод параметров")


@app.route('/show', methods=['GET', 'POST'])
def show():
    form = RegistrationForm()
    registration = None

    if form.validate_on_submit():
        registration = Registration(name=form.name.data, pulse=form.pulse.data, pressure=form.pressure.data,
                                    sugar=form.sugar.data, hemoglobin=form.hemoglobin.data)
        db.session.add(registration)
        db.session.commit()

    return render_template('show.html', form=form, title="Показ параметров", registration=registration)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!')
    return render_template('feedback.html', form=form, title="Обратная связь")


if __name__ == '__main__':
    app.run()
