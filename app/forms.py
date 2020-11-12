from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, DecimalField, PasswordField, BooleanField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError, Regexp

class EmployeeCreationForm(FlaskForm):
    numeross = IntegerField('Sécurité sociale number', validators=[DataRequired('Integer required')])
    nom = StringField('Name', validators=[DataRequired()])
    prenom = StringField('Surname', validators=[DataRequired()])
    adresse = StringField('Address', validators=[DataRequired()])
    salaire = DecimalField(places=2, validators=[DataRequired('Maximum 2 decimals')])
    typeid = SelectField('Type',choices=[('',' - '),('naviguant', 'Navigating Staff'), ('au_sol', 'Ground Staff')],validators=[DataRequired()])
    submit = SubmitField('Submit')

class EngineCreationForm(FlaskForm):
    numeroimmatriculation = StringField('Immatriculation Number', validators=[DataRequired('Unique Immatriculation')])
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AirportAdminForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    nom = StringField('Name', validators=[DataRequired()])
    pays = StringField('Country', validators=[DataRequired()])
    ville = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ConnectionAdminForm(FlaskForm):
    idaeroportdepart = IntegerField('Departure Airport', validators=[DataRequired()])
    idaeroportarrivee = IntegerField('Arrival Airport', validators=[DataRequired()])
    submit = SubmitField('Submit')