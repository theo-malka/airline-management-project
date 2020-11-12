from flask import render_template, flash, redirect, url_for, request
from app import app
import psycopg2

from app.forms import EmployeeCreationForm, EngineCreationForm, AirportAdminForm, ConnectionAdminForm

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
import os

host = 'ec2-18-203-62-227.eu-west-1.compute.amazonaws.com'
database = 'd7af4mf6emn94b'
user = 'qavzwkbywthquc'
password = 'fbb5b3967556f188ed15775e0a650fdfa4f9eb9c7210ae6d6d4622e227bac875'

@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title = 'Homepage')

@app.route('/resources')
def resources():
    return render_template('resources.html', title = 'Resources')

@app.route('/manage_db')
def manage_db():
    return render_template('manage_db.html', title = 'Manage DB')

@app.route('/create/employe', methods=['GET', 'POST'])
def create_employe():
    form = EmployeeCreationForm()
    if form.validate_on_submit():
        numeross = str(form.numeross.data)
        engine = create_engine(app.config['DATABASE_URL'])
        db = scoped_session(sessionmaker(bind=engine))
        db_response = db.execute('select numeross from employe where numeross=' + numeross).fetchall()
        if len(db_response) > 0:
            flash('This staff member is already in the DB',"alert alert-info")
        else :
            nom = str(form.nom.data)
            prenom = str(form.prenom.data)
            adresse = str(form.adresse.data)
            salaire = str(form.salaire.data)
            if str(form.typeid.data) == 'naviguant':
                typeid = '1' 
            else:
                typeid = '2'
            flash('{} {} as been added as a new staff member.'.format(prenom,nom),"alert alert-info")
            statement = films.insert().values(title="Doctor Strange", director="Scott Derrickson", year="2016")  
            db.execute('insert into employe (numeross,nom,prenom,adresse,salaire,typeid) values (' + numeross + ',' + nom + ',' + prenom + ',' + adresse + ',' + salaire + ',' + typeid + ')')
            db.commit()
            db.close()
            if typeid == 1:
                return redirect(url_for(create_employe_navigating, numeross = numeross))
            else :
                return redirect('/homepage')
    return render_template('create_employe.html', title='New Staff', form=form)

@app.route('/create/appareil', methods=['GET', 'POST'])
def create_engine():
    form = EngineCreationForm()
    numeroimmatriculation = str(form.numeroimmatriculation.data)
    type = str(form.type.data)
    if form.validate_on_submit():
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute("select numeroimmatriculation from appareil where numeroimmatriculation='" + numeroimmatriculation + "'")
        check = cursor.fetchall()
        cursor.close()
        if len(check)>0:
            flash('This engine is already in the DB',"alert alert-info")
        else:
            cursor = conn.cursor()
            cursor.execute("insert into appareil values (%s, %s)",(numeroimmatriculation,type))
            conn.commit()
            cursor.close()
            flash(numeroimmatriculation + ' is now in the Data Base.',"alert alert-info")
        conn.close()
    return render_template('create_engine.html', title='New Engine', form=form)

@app.route('/admin/aeroport', methods=['GET', 'POST'])
def admin_airport():
    form = AirportAdminForm()
    code = str(form.code.data)
    nom = str(form.nom.data)
    pays = str(form.pays.data)
    ville = str(form.ville.data)
    if form.validate_on_submit():
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute("insert into aeroport (code, nom, pays, ville) values (%s, %s, %s, %s)",(code,nom,pays,ville))
        conn.commit()
        cursor.close()
        flash(code + ' is now in the Data Base.',"alert alert-info")
        conn.close()
    return render_template('admin_aeroport.html', title='ADMIN - New Engine', form=form)

@app.route('/admin/liaison', methods=['GET', 'POST'])
def admin_liaison():
    form = ConnectionAdminForm()
    idaeroportdepart = int(form.idaeroportdepart.data)
    idaeroportarrivee = int(form.idaeroportarrivee.data)
    if form.validate_on_submit():
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute("insert into liaison (idaeroportdepart, idaeroportarrivee) values (%s, %s)",(idaeroportdepart,idaeroportarrivee))
        conn.commit()
        cursor.close()
        flash('Connection between ' +  idaeroportdepart + 'and' + idaeroportarrivee + ' is now in the Data Base.',"alert alert-info")
        conn.close()
    return render_template('admin_liaison.html', title='ADMIN - New Connection', form=form)