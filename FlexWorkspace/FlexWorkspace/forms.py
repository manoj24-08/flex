from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, Email, Length, NumberRange

class WorkerRegistrationForm(FlaskForm):
    name = StringField('Full Name', [DataRequired(), Length(min=2, max=50)])
    email = StringField('Email Address', [DataRequired(), Email()])
    phone = StringField('Phone Number', [DataRequired(), Length(min=10, max=15)])
    
    service = SelectField('Service Type', [DataRequired()], choices=[
        ('', 'Select a service...'),
        ('Plumbing', 'Plumbing'),
        ('Electrical', 'Electrical'),
        ('Carpentry', 'Carpentry'),
        ('Cleaning', 'Cleaning'),
        ('Painting', 'Painting'),
        ('Gardening', 'Gardening'),
        ('Handyman', 'Handyman'),
        ('Other', 'Other')
    ])
    
    location = StringField('Location/Area', [DataRequired(), Length(min=2, max=100)])
    experience = IntegerField('Years of Experience', [DataRequired(), NumberRange(min=0, max=50)])
    description = TextAreaField('Description of Services', [DataRequired(), Length(min=10, max=500)])
    rate = IntegerField('Hourly Rate ($)', [DataRequired(), NumberRange(min=1, max=1000)])
    
    availability = SelectField('Availability', [DataRequired()], choices=[
        ('', 'Select availability...'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Weekends only', 'Weekends only'),
        ('Evenings only', 'Evenings only'),
        ('Flexible', 'Flexible')
    ])
    
    profile_image = FileField('Profile Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

class ContactForm(FlaskForm):
    name = StringField('Your Name', [DataRequired(), Length(min=2, max=50)])
    email = StringField('Email Address', [DataRequired(), Email()])
    subject = StringField('Subject', [DataRequired(), Length(min=5, max=100)])
    message = TextAreaField('Message', [DataRequired(), Length(min=10, max=1000)])
