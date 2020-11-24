from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, DecimalField, PasswordField, BooleanField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError, Regexp
from wtforms.fields.html5 import DateField, TimeField

class EmployeeCreationForm(FlaskForm):
    numeross = IntegerField('Sécurité sociale number', validators=[DataRequired('Integer required')])
    nom = StringField('Name', validators=[DataRequired()])
    prenom = StringField('Surname', validators=[DataRequired()])
    adresse = StringField('Address', validators=[DataRequired()])
    salaire = DecimalField('Salary', places=2, validators=[DataRequired('Maximum 2 decimals')])
    typeid = SelectField('Type',choices=[('',' - '), ('naviguant_pilote', 'Navigating Staff - Pilot'), ('naviguant_autre', 'Navigating Staff - Other'), ('au_sol', 'Ground Staff')],validators=[DataRequired()])
    submit = SubmitField('Submit')

class PilotCreationForm(FlaskForm):
    nombreheuresvol = IntegerField('Total flying time', validators=[DataRequired()])
    numerolicence = IntegerField('Licence Id', validators=[DataRequired()])
    submit = SubmitField('Submit')

class OtherNavigatingCreationForm(FlaskForm):
    nombreheuresvol = IntegerField('Total flying time', validators=[DataRequired()])
    fonction = StringField('Function', validators=[DataRequired()])
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
    idaeroportdepart = IntegerField('Departure Airport', validators=[DataRequired('Please specify the airportid')])
    idaeroportarrivee = IntegerField('Arrival Airport', validators=[DataRequired('Please specify the airportid')])
    submit = SubmitField('Submit')

class FlightCreationForm(FlaskForm):
    numero = StringField('Number', validators=[DataRequired()])
    jourdepart = DateField('Departure Date', format="%Y-%m-%d", validators=[DataRequired()])
    jourarrivee = DateField('Arrival Date', format="%Y-%m-%d", validators=[DataRequired()])
    heuredepart = TimeField('Departure Time', format='%H:%M', validators=[DataRequired()])
    heurearrivee = TimeField('Arrival Time', format='%H:%M', validators=[DataRequired()])
    idliaison = SelectField('Connection id', validators=[DataRequired()])
    numeroimmatriculationappareil = SelectField('Engine immatriculation number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DepartureCreationForm(FlaskForm):
    submit = SubmitField('Submit')

class StaffDepartureCreationForm(FlaskForm):
    nombreplaceslibres = IntegerField('Number of tickets for this departure', validators=[DataRequired()])
    submit = SubmitField('Submit')

class BilletBookingForm(FlaskForm):
    submit = SubmitField('Submit')

class BilletInfoBookingForm(FlaskForm):
    nom = StringField('Surname', validators=[DataRequired()])
    prenom = StringField('Name', validators=[DataRequired()])
    adresse = StringField('Address', validators=[DataRequired()])
    numero = IntegerField('Billet Number', validators=[DataRequired()])
    prix = DecimalField('Ticket Price', places=2, validators=[DataRequired('Maximum 2 decimals')])
    submit = SubmitField('Submit')