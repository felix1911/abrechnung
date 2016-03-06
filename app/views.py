from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EinkaufForm, MonatsauswahlForm
from .models import User, Eintrag
import datetime,time

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))



def after_login(name):
    if name is None:
        flash ('Keine Eingabe')
        return redirect(url_for('login'))
    user = User.query.filter_by(nickname = name).first()
    if user is None:
        flash('Falsche Eingabe')
        return redirect(url_for('login'))
    remember_me = False
    if'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

def einkauf_eintragen(betrage,orte,datume):
    if betrage is None or orte is None or datume is None:
        flash ('Leeres Feld')
        return redirect(url_for('eintrag'))
    e = Eintrag(betrag = betrage, ort = orte, datum = datume,user_name = g.user.nickname,timestamp = datetime.datetime.now().date())
    db.session.add(e)
    db.session.commit()
    flash('Einkauf eingetragen')
    return redirect(request.args.get('next') or url_for('buch'))
    

@app.route('/')
def base():
    return redirect(url_for('index'))
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home'
                          )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
       flash('Bereits eingeloggt') 
       return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        session['remember_me'] = form.remember_me.data 
        return after_login(form.benutzer.data)
    elif request.method == 'POST' and form.validate() == False:
        flash('Keine Eingabe')
    return render_template('login.html',
                           title='Login',
                           form=form
                           )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/eintrag', methods=['GET', 'POST'])
def eintrag():
    if not g.user.is_authenticated:        
        return redirect(url_for('login'))
    form = EinkaufForm()
    
    if request.method == 'POST' and form.validate():       
        return einkauf_eintragen(form.betrag.data,form.ort.data,form.datum.data)        
    elif request.method == 'POST' and form.validate() == False:
        flash("Falsche Eingabe")
    return render_template('eintrag.html',
                           title='Eintrag',
                           form=form
                           )

@app.route('/buch', methods=['GET', 'POST'])
def buch():
    if not g.user.is_authenticated:        
        return redirect(url_for('login'))
    form = MonatsauswahlForm()
    if form.validate_on_submit():
        if form.auswahl.data == 3:
            eintrage = Eintrag.query.filter().order_by('datum desc').all()
        else:
            month_begin = (datetime.datetime.now().month - 1 - form.auswahl.data)%12 + 1
            month_end = (datetime.datetime.now().month -form.auswahl.data)%12+1
            if (datetime.datetime.now().month - 1 - form.auswahl.data)<0:
                year_begin = datetime.datetime.now().year -1
                if (datetime.datetime.now().month  - form.auswahl.data)<0:
                    year_end = datetime.datetime.now().year -1
                else:
                    year_end = year_end = datetime.datetime.now().year                
            else:
                year_begin = datetime.datetime.now().year
                year_end = datetime.datetime.now().year
            eintrage = Eintrag.query.filter(Eintrag.datum >= datetime.date(year_begin,month_begin,1), Eintrag.datum < datetime.date(year_end,month_end,1)).order_by('datum desc').all()
        i = 0
        summe = []
        user = User.query.all()
        for u in user:
            summe.append(0)
            for e in eintrage:
                if e.user_name == u.nickname:
                    summe[i] += e.betrag                    
            i += 1          
        return render_template('buch.html',
                           title='Haushaltsbuch',
                           eintrage = eintrage,
                           form = form,
                           user = user,
                           summe = summe
                        )
    else:
        return render_template('buch.html',
                           title='Haushaltsbuch',
                           form = form
                           )
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%d.%m.%Y'
    return native.strftime(format) 