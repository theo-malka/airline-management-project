from flask import render_template, flash, redirect, url_for, request
from app import app
import psycopg2

from app.forms import EmployeeCreationForm, EngineCreationForm, AirportAdminForm, ConnectionAdminForm, FlightCreationForm, PilotCreationForm, OtherNavigatingCreationForm, DepartureCreationForm, StaffDepartureCreationForm, BilletBookingForm, BilletInfoBookingForm

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

@app.route('/create/employe', methods=['GET', 'POST'])
def create_employe():
    form = EmployeeCreationForm()
    if form.validate_on_submit():
        numeross = str(form.numeross.data)
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute('select numeross from employe where numeross=' + numeross)
        check = cursor.fetchall()
        cursor.close()
        if len(check) > 0:
            flash('This staff member is already in the DB',"alert alert-info")
        else :
            nom = str(form.nom.data)
            prenom = str(form.prenom.data)
            adresse = str(form.adresse.data)
            salaire = str(form.salaire.data)
            if str(form.typeid.data) == 'naviguant_pilote' :
                typeid = '1' 
                navigatingtypeid = '1'
            elif str(form.typeid.data) == 'naviguant_autre' :
                typeid = '1'
                navigatingtypeid = '2'
            elif str(form.typeid.data) == 'au_sol' :
                typeid = '2'
            flash('{} {} has been added as a new staff member.'.format(prenom,nom),"alert alert-info")
            cursor = conn.cursor()
            cursor.execute('insert into employe (numeross,nom,prenom,adresse,salaire,typeid) values (%s, %s, %s, %s, %s, %s)',(numeross,nom,prenom,adresse,salaire,typeid))
            conn.commit()
            cursor.close()
            conn.close()
            if typeid == '1' and navigatingtypeid == '1' :
                return redirect(url_for('create_navigating_pilot', numeross = numeross))
            elif typeid == '1' and navigatingtypeid == '2' :
                return redirect(url_for('create_navigating_other', numeross = numeross))
            else :
                return redirect('/homepage')
    return render_template('create_employe.html', title='New Staff', form=form)

@app.route('/create/employe/naviguant/pilote/<numeross>', methods=['GET', 'POST'])
def create_navigating_pilot(numeross):
    form = PilotCreationForm()
    if form.validate_on_submit():
        nombreheuresvol = str(form.nombreheuresvol.data)
        numerolicence = str(form.numerolicence.data)
        typeid = '1'
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute('insert into naviguant (numeross,nombreheuresvol,numerolicence,typeid) values (%s, %s, %s, %s)', (numeross,nombreheuresvol,numerolicence,typeid))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Pilot with licence Id ' + numerolicence + ' is now in the Data Base.',"alert alert-info")
        return redirect('/homepage')
    return render_template('create_navigating_pilot.html', title='New Pilot', form=form)

@app.route('/create/employe/naviguant/autre/<numeross>', methods=['GET', 'POST'])
def create_navigating_other(numeross):
    form = OtherNavigatingCreationForm()
    if form.validate_on_submit():
        nombreheuresvol = str(form.nombreheuresvol.data)
        fonction = str(form.fonction.data)
        typeid = '2'
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute('insert into naviguant (numeross,nombreheuresvol,fonction,typeid) values (%s, %s, %s, %s)', (numeross,nombreheuresvol,fonction,typeid))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Navigating Staff ' + fonction + ' is now in the Data Base.',"alert alert-info")
        return redirect('/homepage')
    return render_template('create_navigating_other.html', title='New Navigating Staff - Other', form=form)

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
            return redirect('/homepage')
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
    idaeroportdepart = str(form.idaeroportdepart.data)
    idaeroportarrivee = str(form.idaeroportarrivee.data)
    if form.validate_on_submit():
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute("insert into liaison (idaeroportdepart, idaeroportarrivee) values (%s, %s)",(idaeroportdepart,idaeroportarrivee))
        conn.commit()
        cursor.close()
        flash('Connection between ' +  idaeroportdepart + ' and ' + idaeroportarrivee + ' is now in the Data Base.',"alert alert-info")
        conn.close()
    return render_template('admin_liaison.html', title='ADMIN - New Connection', form=form)

@app.route('/create/vol', methods=['GET', 'POST'])
def create_vol():
    form = FlightCreationForm()
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("select numeroimmatriculation, type from appareil")
    engines = cursor.fetchall()
    engines_choices = [('',' - ')]+[(engines[i][0],engines[i][0] + ' - ' + engines[i][1]) for i in range(len(engines))]
    form.numeroimmatriculationappareil.choices = engines_choices
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("select l.id, concat(dep.nom, ', ', dep.ville, ', ', dep.pays),  concat(arr.nom, ', ', arr.ville, ', ', arr.pays) from liaison l left join aeroport dep on dep.id = l.idaeroportdepart left join aeroport arr on arr.id = l.idaeroportarrivee order by l.id")
    links = cursor.fetchall()
    links_choices = [('',' - ')]+[(links[i][0],str(links[i][0]) + ' : ' + links[i][1] + ' - ' + links[i][2]) for i in range(len(links))]
    form.idliaison.choices = links_choices
    cursor.close()
    numero = str(form.numero.data)
    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute("select numero from vol where numero='" + numero + "'")
        check = cursor.fetchall()
        cursor.close()
        if len(check) > 0:
            flash('There is already a flight number ' + numero + ' in the Data Base.',"alert alert-info")
        else :
            jourdepart = str(form.jourdepart.data)
            jourarrivee = str(form.jourarrivee.data)
            heuredepart = str(form.heuredepart.data)
            heurearrivee = str(form.heurearrivee.data)
            idliaison = str(form.idliaison.data)
            datedepart = jourdepart + ' ' + heuredepart
            datearrivee = jourarrivee + ' ' + heurearrivee
            if datedepart > datearrivee:
                flash('Departure date must be before arrival date.',"alert alert-info")
            else:
                numeroimmatriculationappareil = str(form.numeroimmatriculationappareil.data)
                cursor = conn.cursor()
                cursor.execute("select a.numeroimmatriculation from appareil a left join vol v on v.numeroimmatriculationappareil = a.numeroimmatriculation where v.datedepart <= %s and v.datearrivee >= %s and a.numeroimmatriculation = %s union select a.numeroimmatriculation from appareil a left join vol v on v.numeroimmatriculationappareil = a.numeroimmatriculation where v.datearrivee <= %s and v.datedepart >= %s and a.numeroimmatriculation = %s union select a.numeroimmatriculation from appareil a left join vol v on v.numeroimmatriculationappareil = a.numeroimmatriculation where v.datedepart <= %s and v.datedepart >= %s and a.numeroimmatriculation = %s ",(datearrivee,datearrivee,numeroimmatriculationappareil,datedepart,datedepart,numeroimmatriculationappareil,datedepart,datearrivee,numeroimmatriculationappareil))
                check = cursor.fetchall()
                cursor.close()
                if len(check)>0:
                    flash('The engine is not available at this time.',"alert alert-info")
                else:
                    cursor = conn.cursor()
                    cursor.execute("insert into vol (numero,dateDepart,dateArrivee,idLiaison,numeroImmatriculationAppareil) values (%s, %s, %s, %s, %s)", (numero,datedepart,datearrivee,idliaison,numeroimmatriculationappareil))
                    conn.commit()
                    cursor.close()
                    flash('Flight number ' + numero + ' is now in the Data Base.',"alert alert-info")
                    return redirect('/homepage')
        conn.close()
    conn.close()
    return render_template('create_vol.html', title='New Flight', form=form)

@app.route('/create/depart', methods=['GET', 'POST'])
def create_depart():
    form = DepartureCreationForm()
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("select v.numero, dep.nom, v.datedepart, arr.nom, v.datearrivee, concat(dep.code,' - ',arr.code), dep.code, arr.code from vol v left join appareil a on a.numeroimmatriculation = v.numeroimmatriculationappareil left join liaison l on l.id = v.idliaison left join aeroport dep on dep.id = l.idaeroportdepart left join aeroport arr on arr.id = l.idaeroportarrivee left join depart d on d.numerovol = v.numero where d.id is null ")
    vols = cursor.fetchall()
    cursor.close()
    conn.close()
    vols_formatted = []
    for vol in vols:
        vols_formatted.append({'numero':vol[0], 'aeroportdepart':vol[1], 'datedepart':vol[2], 'aeroportarrivee':vol[3], 'datearrivee':vol[4], 'liaison':vol[5], 'dep':vol[6], 'arr':vol[7]})
    if form.validate_on_submit():
        vols_selected = request.form.getlist('VOL')
        if len(vols_selected) > 0:
            vol_selected = vols_selected[0]
            id_aeroport_depart, id_aeroport_arrivee = '', ''
            for x in vols_formatted:
                if x['numero'] == vol_selected:
                    id_aeroport_depart = x['dep']
                    id_aeroport_arrivee = x['arr']
            return redirect(url_for('create_depart_staff', vol_selected=vol_selected, id_aeroport_depart=id_aeroport_depart, id_aeroport_arrivee=id_aeroport_arrivee))
    return render_template('create_depart.html', title='New Departure', form=form, vols=vols_formatted)

@app.route('/create/depart/staff/<vol_selected>_<id_aeroport_depart>-<id_aeroport_arrivee>', methods=['GET', 'POST'])
def create_depart_staff(vol_selected,id_aeroport_depart,id_aeroport_arrivee):
    form = StaffDepartureCreationForm()
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("select datedepart, datearrivee from vol v where v.numero = '" + vol_selected +"'")
    vol = cursor.fetchall()[0]
    cursor.close()
    datedepart, datearrivee = vol[0], vol[1]
    cursor = conn.cursor()
    cursor.execute("with staff as( select e.numeross as numeross, e.nom as nom, e.prenom as prenom, n.nombreheuresvol as nombreheuresvol, n.fonction as fonction, ve1.datedepart as datedepart, ve1.datearrivee as datearrivee from employe e left join naviguant n on n.numeross = e.numeross left join employetype et on et.id = e.typeid left join naviguanttype nt on nt.id = n.typeid left join depart e1 on e1.ssequipage1 = e.numeross left join vol ve1 on ve1.numero = e1.numerovol where nt.id = 2 union select e.numeross as numeross, e.nom as nom, e.prenom as prenom, n.nombreheuresvol as nombreheuresvol, n.fonction as fonction, ve2.datedepart as datedepart, ve2.datearrivee as datearrivee from employe e left join naviguant n on n.numeross = e.numeross left join employetype et on et.id = e.typeid left join naviguanttype nt on nt.id = n.typeid left join depart e2 on e2.ssequipage2 = e.numeross left join vol ve2 on ve2.numero = e2.numerovol where nt.id = 2 order by numeross, datedepart), conditions as ( select numeross from staff s where s.datedepart <= %s and s.datearrivee >= %s union select numeross from staff s where s.datearrivee <= %s and s.datedepart >= %s union select numeross from staff s where s.datedepart <= %s and s.datedepart >= %s) select distinct numeross, nom, prenom, nombreheuresvol, fonction from staff s where s.numeross not in (select * from conditions) ",(datearrivee,datearrivee,datedepart,datedepart,datedepart,datearrivee))
    staff = cursor.fetchall()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("with staff as( select e.numeross as numeross, e.nom as nom, e.prenom as prenom, n.nombreheuresvol as nombreheuresvol, n.numerolicence as numerolicence, vp1.datedepart as datedepart, vp1.datearrivee as datearrivee from employe e left join naviguant n on n.numeross = e.numeross left join employetype et on et.id = e.typeid left join naviguanttype nt on nt.id = n.typeid left join depart p1 on p1.sspilote1 = e.numeross left join vol vp1 on vp1.numero = p1.numerovol where nt.id = 1 union select e.numeross as numeross, e.nom as nom, e.prenom as prenom, n.nombreheuresvol as nombreheuresvol, n.numerolicence as numerolicence, vp2.datedepart as datedepart, vp2.datearrivee as datearrivee from employe e left join naviguant n on n.numeross = e.numeross left join employetype et on et.id = e.typeid left join naviguanttype nt on nt.id = n.typeid left join depart p2 on p2.sspilote2 = e.numeross left join vol vp2 on vp2.numero = p2.numerovol where nt.id = 1 order by numeross, datedepart), conditions as ( select numeross from staff s where s.datedepart <= %s and s.datearrivee >= %s union select numeross from staff s where s.datearrivee <= %s and s.datedepart >= %s union select numeross from staff s where s.datedepart <= %s and s.datedepart >= %s) select distinct numeross, nom, prenom, nombreheuresvol, numerolicence from staff s where s.numeross not in (select * from conditions) ",(datearrivee,datearrivee,datedepart,datedepart,datedepart,datearrivee))
    pilots = cursor.fetchall()
    cursor.close()
    staff_formatted = []
    pilots_formatted = []
    for s in staff:
        staff_formatted.append({'numeross':s[0] ,'nom':s[1] ,'prenom':s[2] ,'nombreheuresvol':s[3] ,'fonction':s[4]})
    for p in pilots:
        pilots_formatted.append({'numeross':p[0] ,'nom':p[1] ,'prenom':p[2] ,'nombreheuresvol':p[3] ,'numerolicence':p[4]})
    if form.validate_on_submit():
        pilots_selected = request.form.getlist('PILOTS')
        staff_selected = request.form.getlist('STAFF')
        nombreplaceslibres = str(form.nombreplaceslibres.data)
        nombreplacesoccupees = '0'
        if len(staff_selected) != 2 :
            flash('Please select 2 Staff members.',"alert alert-info")
        elif len(pilots_selected) == 0 or len(pilots_selected) > 2:
            flash('Please select 1 or 2 Pilots.',"alert alert-info")
        else :
            if len(pilots_selected) == 1:
                sspilote2 = None
            else:
                sspilote2 = pilots_selected[1]
            sspilote1 = pilots_selected[0]
            ssequipage1 = staff_selected[0]
            ssequipage2 = staff_selected[1]
            cursor = conn.cursor()
            cursor.execute("insert into depart (numerovol,sspilote1,sspilote2,ssequipage1,ssequipage2,nombreplaceslibres,nombreplacesoccupees) values (%s,%s,%s,%s,%s,%s,%s)",(vol_selected,sspilote1,sspilote2,ssequipage1,ssequipage2,nombreplaceslibres,nombreplacesoccupees))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Departure has been created.',"alert alert-info")
            return redirect('/homepage')
    return render_template('create_depart_staff.html', title='New Departure - Staff', form=form, staff=staff_formatted, pilots=pilots_formatted)

@app.route('/book/billet', methods=['GET', 'POST'])
def book_billet():
    form = BilletBookingForm()
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("select d.id, d.numerovol, a1.nom as aeroportdepart, concat(a1.ville,', ',a1.pays) as depart, v.datedepart, a2.nom as aeroportarrivee, concat(a2.ville,', ',a2.pays) as arrivee, v.datearrivee, d.nombreplaceslibres from depart d left join vol v on v.numero = d.numerovol left join liaison l on l.id = v.idliaison left join aeroport a1 on a1.id = l.idaeroportdepart left join aeroport a2 on a2.id = l.idaeroportarrivee where d.nombreplaceslibres > 0 ")
    departs = cursor.fetchall()
    cursor.close()
    conn.close()
    departs_formatted = []
    for depart in departs:
        departs_formatted.append({'id': depart[0], 'numerovol': depart[1], 'aeroportdepart': depart[2], 'villedepart': depart[3], 'datedepart': depart[4], 'aeroportarrivee': depart[5], 'villearrivee': depart[6], 'datearrivee': depart[7], 'nombreplaceslibres': depart[8]})
    if form.validate_on_submit():
        departs_selected = request.form.getlist('DEPART')
        if len(departs_selected) > 0:
            depart_selected = departs_selected[0]
            return redirect(url_for('book_billet_info',depart_selected=depart_selected))
    return render_template('book_billet.html', title='New Booking', form=form, departs=departs_formatted)

@app.route('/book/billet/infos/<depart_selected>', methods=['GET', 'POST'])
def book_billet_info(depart_selected):
    form = BilletInfoBookingForm()
    if form.validate_on_submit():
        nom = str(form.nom.data)
        prenom = str(form.prenom.data)
        adresse = str(form.adresse.data)
        numero = str(form.numero.data)
        prix = str(form.prix.data)
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute("select numero from billet where numero =" + numero)
        check = cursor.fetchall()
        cursor.close()
        if len(check) > 0:
            flash('This ticket number already exists, please choose another.',"alert alert-info")
        else:
            cursor = conn.cursor()
            cursor.execute("insert into passager (nom,prenom,adresse) values (%s, %s, %s) returning id",(nom,prenom,adresse))
            conn.commit()
            passagerid = cursor.fetchall()
            id = passagerid[0][0]
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("insert into billet (numero,dateemission,prix,departid,passagerid) values (%s, current_timestamp, %s, %s, %s)", (numero,prix,depart_selected,id))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("update depart set nombreplaceslibres = nombreplaceslibres-1, nombreplacesoccupees = nombreplacesoccupees+1 where id = %s",(depart_selected))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Ticket number {} has been created. The customer id is {}'.format(numero,id),"alert alert-info")
            return redirect('/homepage')
        conn.close()
    return render_template('book_billet_info.html', title='Booking Information', form=form)

@app.route('/manage_db', methods=['GET', 'POST'])
def manage_db():
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("select * from appareil")
    appareil_raw = cursor.fetchall()
    cursor.close()
    appareil = []
    for a in appareil_raw:
        appareil.append({'numeroimmatriculation':a[0], 'type':a[1]})
    cursor = conn.cursor()
    cursor.execute("select * from aeroport")
    aeroport_raw = cursor.fetchall()
    cursor.close()
    aeroport = []
    for a in aeroport_raw:
        aeroport.append({'id':a[0],'code':a[1],'nom':a[2],'pays':a[3],'ville':a[4]})
    cursor = conn.cursor()
    cursor.execute("select l.id, dep.code, dep.nom, concat(dep.ville,', ',dep.pays), arr.code, arr.nom, concat(arr.ville,', ',arr.pays) from liaison l left join aeroport dep on dep.id = l.idaeroportdepart left join aeroport arr on arr.id = l.idaeroportarrivee")
    liaison_raw = cursor.fetchall()
    cursor.close()
    liaison = []
    for l in liaison_raw:
        liaison.append({'id':l[0],'codedepart':l[1],'nomdepart':l[2],'villedepart':l[3],'codearrivee':l[4],'nomarrivee':l[5],'villearrivee':l[6]})
    cursor = conn.cursor()
    cursor.execute("select e.numeross, e.nom, e.prenom, e.adresse, e.salaire, n.numerolicence, n.nombreheuresvol, n.fonction, concat(e2.nom, ' - ', n2.nom) from employe e left join naviguant n on n.numeross = e.numeross left join employetype e2 on e2.id = e.typeid left join naviguanttype n2 on n2.id = n.typeid")
    employe_raw = cursor.fetchall()
    cursor.close()
    employe = []
    for e in employe_raw:
        employe.append({'numeross':e[0],'nom':e[1],'prenom':e[2],'adresse':e[3],'salaire':e[4],'numerolicence':e[5],'nombreheuresvol':e[6],'fonction':e[7],'type':e[8]})
    cursor = conn.cursor()
    cursor.execute("select v.numero, v.datedepart, v.datearrivee, dep.nom, arr.nom from vol v left join liaison l on l.id = v.idliaison left join appareil a on a.numeroimmatriculation = v.numeroimmatriculationappareil left join aeroport dep on dep.id = l.idaeroportdepart left join aeroport arr on arr.id = l.idaeroportarrivee")
    vol_raw = cursor.fetchall()
    cursor.close()
    vol = []
    for v in vol_raw:
        vol.append({'numero':v[0],'datedepart':v[1],'datearrivee':v[2],'aeroportdepart':v[3],'aeroportarrivee':v[4]})
    cursor = conn.cursor()
    cursor.execute("select * from depart d")
    depart_raw = cursor.fetchall()
    cursor.close()
    depart = []
    for d in depart_raw:
        depart.append({'id':d[0],'numerovol':d[1],'sspilote1':d[2],'sspilote2':d[3],'ssequipage1':d[4],'ssequipage2':d[5],'nombreplaceslibres':d[6],'nombreplacesoccupees':d[7]})
    cursor = conn.cursor()
    cursor.execute("select * from billet b left join passager p on p.id = b.passagerid ")
    billet_raw = cursor.fetchall()
    cursor.close()
    billet = []
    for b in billet_raw:
        billet.append({'numero':b[0],'dateemission':b[1],'prix':b[2],'departid':b[3],'passagerid':b[4],'customerid':b[5],'customersurname':b[6],'customername':b[7],'custoemraddress':b[7]})
    conn.close()
    return render_template('manage_db.html', title = 'Manage DB', engine=appareil, employee=employe, airport=aeroport, link=liaison, flight=vol, departure=depart, ticket=billet)

@app.route('/deletion', methods=['GET', 'POST'])
def deletion():
    deletion_dict = request.get_json()
    print(deletion_dict)
    delete_employee = deletion_dict['EMPLOYEE']
    delete_flight = deletion_dict['FLIGHT']
    delete_departure = deletion_dict['DEPARTURE']
    delete_ticket = deletion_dict['TICKET']
    delete_link = deletion_dict['LINK']
    delete_airport = deletion_dict['AIRPORT']
    delete_engine = deletion_dict['ENGINE']
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)

    def deletion_employee(list):
        for l in list:
            cursor = conn.cursor()
            cursor.execute("select d.id from employe e left join depart d on d.ssequipage1 = e.numeross where e.numeross = %s and d.id is not null union select d.id from employe e left join depart d on d.ssequipage2 = e.numeross where e.numeross = %s and d.id is not null union select d.id from employe e left join depart d on d.sspilote1 = e.numeross where e.numeross = %s and d.id is not null union select d.id from employe e left join depart d on d.sspilote2 = e.numeross where e.numeross = %s and d.id is not null",(l,l,l,l))
            check = cursor.fetchall()
            cursor.close()
            if len(check)>0:
                flash('You cannot delete this employee as it is in departure number ' + str(check[0][0]) +'.',"alert alert-info")
            else:
                cursor = conn.cursor()
                cursor.execute("delete from naviguant where numeross = " + l)
                conn.commit()
                cursor.close()
                cursor = conn.cursor()
                cursor.execute("delete from employe where numeross = " + l)
                conn.commit()
                cursor.close()
                flash('Employee ' + l + ' has been deleted.',"alert alert-info")
    
    def deletion_departure(list):
        for l in list:
            cursor = conn.cursor()
            cursor.execute("select b.numero from billet b where b.departid =" + l)
            check = cursor.fetchall()
            cursor.close()
            if len(check)>0:
                flash('You cannot delete this departure, delete ticket number ' + str(check[0][0]) +'.',"alert alert-info")
            else:
                cursor = conn.cursor()
                cursor.execute("delete from depart where id =" + l)
                conn.commit()
                cursor.close()
                flash('Depart ' + l + ' has been deleted.',"alert alert-info")

    def deletion_ticket(list):
        for l in list:
            cursor = conn.cursor()
            cursor.execute("delete from billet where numero =" + l + "returning passagerid, departid")
            conn.commit()
            response = cursor.fetchall()
            print(response)
            passagerid, departid = response[0][0], response[0][1]
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("delete from passager where id = " + str(passagerid))
            conn.commit()
            cursor.close()
            flash('Ticket ' + str(l) + ' has been deleted, corresponding customer number ' + str(passagerid) + " also.","alert alert-info")
            cursor = conn.cursor()
            cursor.execute("update depart set nombreplaceslibres = nombreplaceslibres+1, nombreplacesoccupees = nombreplacesoccupees-1 where id = %s",(str(departid)))
            conn.commit()
            cursor.close()
            flash('Departure ' + str(departid) + ' available tickets have been updated.',"alert alert-info")
    
    def deletion_flight(list):
        for l in list:
            cursor = conn.cursor()
            cursor.execute("select d.id from depart d where d.numerovol = '" + l + "'")
            check = cursor.fetchall()
            cursor.close()
            if len(check)>0:
                flash('You cannot delete this flight as it is in departure number ' + str(check[0][0]) +'.',"alert alert-info")
            else:
                cursor = conn.cursor()
                cursor.execute("delete from vol where numero ='" + l + "'")
                conn.commit()
                cursor.close()
                flash('Flight ' + l + ' has been deleted.',"alert alert-info")

    def deletion_link(list):
        for l in list:
            cursor = conn.cursor()
            cursor.execute("select v.numero from vol v where v.idliaison = " + l)
            check = cursor.fetchall()
            cursor.close()
            if len(check)>0:
                flash('You cannot delete this connection as it is in flight number ' + check[0][0] +'.',"alert alert-info")
            else:
                cursor = conn.cursor()
                cursor.execute("delete from liaison where id =" + l)
                conn.commit()
                cursor.close()
                flash('Connection ' + l + ' has been deleted.',"alert alert-info")

    def deletion_airport(list):
        for l in list:
            cursor = conn.cursor()
            cursor.execute("select l.id from liaison l where l.idaeroportarrivee = %s union select l.id from liaison l where l.idaeroportdepart = %s",(l,l))
            check = cursor.fetchall()
            cursor.close()
            if len(check)>0:
                flash('You cannot delete this airport as it is in connection number ' + check[0][0] +'.',"alert alert-info")
            else:
                cursor = conn.cursor()
                cursor.execute("delete from aeroport where id =" + l)
                conn.commit()
                cursor.close()
                flash('Airport ' + l + ' has been deleted.',"alert alert-info")

    def deletion_engine(list):
        for l in list:
            cursor = conn.cursor()
            cursor.execute("select v.numero from vol v where v.numeroimmatriculationappareil = '" + l + "'")
            check = cursor.fetchall()
            cursor.close()
            if len(check)>0:
                flash('You cannot delete this engine as it is in flight number ' + str(check[0][0]) +'.',"alert alert-info")
            else:
                cursor = conn.cursor()
                cursor.execute("delete from appareil where numeroimmatriculation = '" + l +"'")
                conn.commit()
                cursor.close()
                flash('Engine ' + l + ' has been deleted.',"alert alert-info")

    if len(delete_engine) > 0:
        deletion_engine(delete_engine)
    if len(delete_airport) > 0:
        deletion_airport(delete_airport)
    if len(delete_link) > 0:
        deletion_link(delete_link)
    if len(delete_flight) > 0:
        deletion_flight(delete_flight)
    if len(delete_ticket) > 0:
        deletion_ticket(delete_ticket)
    if len(delete_employee) > 0:
        deletion_employee(delete_employee)
    if len(delete_departure) > 0:
        deletion_departure(delete_departure)

    conn.close()
    return ''