from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length

class PersonalForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=20)])
    position = StringField('position', validators=[DataRequired(), Length(min=2)])
    github = StringField('github', validators=[DataRequired()])
    linkedin = StringField('linkedin', validators=[DataRequired()])
    insta_id = StringField('insta_id', validators=[DataRequired()])
    image = FileField('profile_pic', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('submit')
