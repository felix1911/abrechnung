from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,DecimalField,DateField,SelectField
from wtforms.validators import DataRequired
import datetime

class FlexibleDecimalField(DecimalField):
    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
        return super(FlexibleDecimalField, self).process_formdata(valuelist)
    
class LoginForm(Form):
    benutzer = StringField('benutzer', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)
    
class EinkaufForm(Form):
    betrag = FlexibleDecimalField('betrag',validators = [DataRequired()], default = 0)
    ort = StringField('ort', validators = [DataRequired()], default = "Rewe")
    datum = DateField('datum', format = "%d.%m.%Y", default = datetime.date.today,validators = [DataRequired()])
    
class MonatsauswahlForm(Form):
    auswahl = SelectField('auswahl',coerce=int,choices=[(0,'Dieser Monat'),(1,'Letzter Monat'),(2,'Vorletzter Monat'),(3,'Gesamt')])