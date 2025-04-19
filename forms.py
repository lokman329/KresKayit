from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş')

class StudentForm(FlaskForm):
    # Student Info
    name = StringField('Ad Soyad', validators=[DataRequired(), Length(max=64)])
    tc_number = StringField('TC Kimlik No', validators=[DataRequired(), Length(min=11, max=11)])
    birth_date = DateField('Doğum Tarihi', validators=[DataRequired()])
    address = StringField('Adres', validators=[DataRequired(), Length(max=500)])
    toilet_trained = BooleanField('Tuvalet Eğitimi Almış')
    school_experience = BooleanField('Okul Deneyimi Var')
    school_type = SelectField('Okul Türü', choices=[('', 'Seçiniz...'), ('Devlet', 'Devlet'), ('Özel', 'Özel')], validators=[Optional()])
    sibling_count = IntegerField('Kardeş Sayısı', default=0)

    # Mother Info
    mother_alive = BooleanField('Anne Hayatta', default=True)
    mother_name = StringField('Anne Adı Soyadı', validators=[Optional(), Length(max=255)])
    mother_phone = StringField('Anne Telefon', validators=[Optional(), Length(max=10)])
    mother_education = SelectField('Anne Eğitim Durumu', choices=[
        ('', 'Seçiniz...'),
        ('İlkokul', 'İlkokul'),
        ('Ortaokul', 'Ortaokul'),
        ('Lise', 'Lise'),
        ('Üniversite', 'Üniversite'),
        ('Yüksek Lisans', 'Yüksek Lisans'),
        ('Doktora', 'Doktora')
    ], validators=[Optional()])
    mother_job = StringField('Anne Meslek', validators=[Optional(), Length(max=100)])
    mother_employer = StringField('Anne İşyeri', validators=[Optional(), Length(max=255)])
    mother_salary = IntegerField('Anne Aylık Gelir', default=0)

    # Father Info
    father_alive = BooleanField('Baba Hayatta', default=True)
    father_name = StringField('Baba Adı Soyadı', validators=[Optional(), Length(max=255)])
    father_phone = StringField('Baba Telefon', validators=[Optional(), Length(max=10)])
    father_education = SelectField('Baba Eğitim Durumu', choices=[
        ('', 'Seçiniz...'),
        ('İlkokul', 'İlkokul'),
        ('Ortaokul', 'Ortaokul'),
        ('Lise', 'Lise'),
        ('Üniversite', 'Üniversite'),
        ('Yüksek Lisans', 'Yüksek Lisans'),
        ('Doktora', 'Doktora')
    ], validators=[Optional()])
    father_job = StringField('Baba Meslek', validators=[Optional(), Length(max=100)])
    father_employer = StringField('Baba İşyeri', validators=[Optional(), Length(max=255)])
    father_salary = IntegerField('Baba Aylık Gelir', default=0)

    # Additional Info
    owns_house = BooleanField('Ev Sahibi', default=True)
    marital_status = SelectField('Medeni Durum', choices=[
        ('Evli', 'Evli'),
        ('Ayrı', 'Ayrı'),
        ('Boşanmış', 'Boşanmış'),
        ('Dul', 'Dul')
    ], validators=[DataRequired()])

    submit = SubmitField('Kaydet') 