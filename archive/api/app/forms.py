"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class FormCreatePlot(FlaskForm):
    """New Plot form."""
    plotid = StringField(
        'plotid',
        [DataRequired()]
    )
    name = StringField(
        'name',
        [DataRequired()]
    )
    submit = SubmitField('Submit')

class EnterNewPlotForm(FlaskForm):
    """New Plot form."""
    plotid = StringField(
        'plotid',
        [DataRequired()]
    )
    name = StringField(
        'name',
        [DataRequired()]
    )
    submit = SubmitField('Submit')
