from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    eintrag = db.relationship('Eintrag',backref = 'User', lazy = 'dynamic')
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Eintrag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ort = db.Column(db.String(13), unique = False)
    datum = db.Column(db.Date,unique=False)
    betrag = db.Column(db.Numeric, unique=False)
    user_name = db.Column(db.String,  db.ForeignKey('user.nickname'), unique = False)
    timestamp = db.Column(db.Date,unique=False)

    def __repr__(self):
        return '<Eintrag %r>' % (self.ort)