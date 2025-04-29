from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from forms import LoginForm, StudentForm
import pandas as pd
from io import BytesIO

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kindergarten.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Kindergarten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    classes = db.relationship('Class', backref='kindergarten', lazy=True)

    @property
    def student_limit(self):
        return sum(c.limit for c in self.classes)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    kindergarten_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'), nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    age_group = db.Column(db.Integer, nullable=False)  # 3, 4, 5, or 6
    students = db.relationship('Student', backref='assigned_class', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Student Info
    preferred_kindergarten_1_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'))
    preferred_kindergarten_2_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'))
    preferred_kindergarten_3_id = db.Column(db.Integer, db.ForeignKey('kindergarten.id'))
    name = db.Column(db.String(64), nullable=False)
    tc_number = db.Column(db.String(11), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    toilet_trained = db.Column(db.Boolean, default=False)
    school_experience = db.Column(db.Boolean, default=False)
    school_type = db.Column(db.String(20))
    sibling_count = db.Column(db.Integer, default=0)

    # Parent Info
    mother_alive = db.Column(db.Boolean, default=True)
    mother_name = db.Column(db.String(255))
    mother_phone = db.Column(db.String(10))
    mother_education = db.Column(db.String(100))
    mother_job = db.Column(db.String(100))
    mother_employer = db.Column(db.String(255))
    mother_salary = db.Column(db.Integer, default=0)

    father_alive = db.Column(db.Boolean, default=True)
    father_name = db.Column(db.String(255))
    father_phone = db.Column(db.String(10))
    father_education = db.Column(db.String(100))
    father_job = db.Column(db.String(100))
    father_employer = db.Column(db.String(255))
    father_salary = db.Column(db.Integer, default=0)

    # Shared Parent Info
    owns_house = db.Column(db.Boolean, default=True)
    marital_status = db.Column(db.String(10))

    # Registration Info
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, default=0)
    disqualified = db.Column(db.Boolean, default=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

    def calculate_points(self):
        points = 0
        current_year = datetime.utcnow().year
        age = current_year - self.birth_date.year

        if age > 6 or age < 3:
            self.disqualified = True
            return 'Elendi'

        if 'Atakum' in self.address:
            points += 5

        if not self.toilet_trained:
            self.disqualified = True
            return 'Elendi'

        points += self.sibling_count

        if self.school_experience and self.school_type == 'Devlet':
            points += 5

        if 'Atakum Bel' in (self.mother_employer or '') or 'Atakum Bel' in (self.father_employer or ''):
            points += 5

        if not self.mother_alive:
            points += 5

        if not self.father_alive:
            points += 5

        if not self.owns_house:
            points += 5

        if self.marital_status == 'Ayrı':
            points += 5

        total_salary = (self.mother_salary or 0) + (self.father_salary or 0)

        if total_salary < 17000:
            points += 20
        elif total_salary < 35000:
            points += 15
        elif total_salary < 53000:
            points += 10
        elif total_salary < 67000:
            points += 5

        self.points = points
        return points

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index_tr.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Geçersiz kullanıcı adı veya şifre')
    return render_template('login_tr.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = StudentForm()
    kindergartens = Kindergarten.query.all()
    
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            tc_number=form.tc_number.data,
            birth_date=form.birth_date.data,
            address=form.address.data,
            toilet_trained=form.toilet_trained.data,
            school_experience=form.school_experience.data,
            school_type=form.school_type.data,
            sibling_count=form.sibling_count.data,
            mother_alive=form.mother_alive.data,
            mother_name=form.mother_name.data,
            mother_phone=form.mother_phone.data,
            mother_education=form.mother_education.data,
            mother_job=form.mother_job.data,
            mother_employer=form.mother_employer.data,
            mother_salary=form.mother_salary.data,
            father_alive=form.father_alive.data,
            father_name=form.father_name.data,
            father_phone=form.father_phone.data,
            father_education=form.father_education.data,
            father_job=form.father_job.data,
            father_employer=form.father_employer.data,
            father_salary=form.father_salary.data,
            owns_house=form.owns_house.data,
            marital_status=form.marital_status.data,
            preferred_kindergarten_1_id=request.form.get('preferred_kindergarten_1'),
            preferred_kindergarten_2_id=request.form.get('preferred_kindergarten_2'),
            preferred_kindergarten_3_id=request.form.get('preferred_kindergarten_3')
        )
        student.calculate_points()
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('student_registration_tr.html', form=form, kindergartens=kindergartens)

@app.route('/success')
def success():
    return render_template('registration_success_tr.html')

@app.route('/students')
@login_required
def student_list():
    students = Student.query.order_by(Student.points.desc(), Student.registration_date).all()
    return render_template('student_list_tr.html', students=students)

@app.route('/assignment', methods=['GET', 'POST'])
@login_required
def assignment():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Get all unassigned students ordered by points
        students = Student.query.filter_by(
            disqualified=False, 
            class_id=None
        ).order_by(Student.points.desc(), Student.registration_date).all()

        for student in students:
            # Calculate student's age
            current_year = datetime.utcnow().year
            student_age = current_year - student.birth_date.year

            # Try to assign to preferred kindergartens in order
            for kindergarten_id in [
                student.preferred_kindergarten_1_id,
                student.preferred_kindergarten_2_id,
                student.preferred_kindergarten_3_id
            ]:
                if kindergarten_id:
                    kindergarten = Kindergarten.query.get(kindergarten_id)
                    if kindergarten:
                        # Find available classes in this kindergarten for student's age group
                        available_classes = Class.query.filter(
                            Class.kindergarten_id == kindergarten.id,
                            Class.age_group == student_age
                        ).all()
                        
                        # Sort classes by current capacity
                        available_classes.sort(key=lambda c: len(c.students))
                        
                        # Try to assign to the least filled class
                        for class_ in available_classes:
                            if len(class_.students) < class_.limit:
                                student.class_id = class_.id
                                db.session.commit()
                                flash(f'{student.name} öğrencisi {kindergarten.name} - {class_.name} sınıfına yerleştirildi')
                                break
                        
                        # If student was assigned to a class, break the kindergarten loop
                        if student.class_id is not None:
                            break

        flash('Yerleştirme işlemi tamamlandı.')
        return redirect(url_for('student_list'))

    # Get assignment statistics
    total_students = Student.query.filter_by(disqualified=False).count()
    assigned_students = Student.query.filter(Student.class_id.isnot(None)).count()
    unassigned_students = total_students - assigned_students
    
    kindergarten_stats = []
    for k in Kindergarten.query.all():
        total_capacity = sum(c.limit for c in k.classes)
        current_students = sum(len(c.students) for c in k.classes)
        kindergarten_stats.append({
            'name': k.name,
            'current_students': current_students,
            'total_capacity': total_capacity,
            'available_spots': total_capacity - current_students
        })

    return render_template('assignment_tr.html', 
                         total_students=total_students,
                         assigned_students=assigned_students,
                         unassigned_students=unassigned_students,
                         kindergarten_stats=kindergarten_stats)

@app.route('/manage_kindergartens', methods=['GET'])
@login_required
def manage_kindergartens():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.')
        return redirect(url_for('index'))
    kindergartens = Kindergarten.query.all()
    return render_template('manage_kindergartens_tr.html', kindergartens=kindergartens)

@app.route('/add_kindergarten', methods=['POST'])
@login_required
def add_kindergarten():
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    kindergarten = Kindergarten(name=name)
    db.session.add(kindergarten)
    db.session.commit()
    
    flash(f'{name} kreşi başarıyla eklendi.')
    return redirect(url_for('manage_kindergartens'))

@app.route('/update_kindergarten/<int:kindergarten_id>', methods=['POST'])
@login_required
def update_kindergarten(kindergarten_id):
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    kindergarten = Kindergarten.query.get_or_404(kindergarten_id)
    name = request.form.get('name')
    
    kindergarten.name = name
    db.session.commit()
    
    flash('Kreş bilgileri güncellendi.')
    return redirect(url_for('manage_kindergartens'))

@app.route('/add_class/<int:kindergarten_id>', methods=['POST'])
@login_required
def add_class(kindergarten_id):
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    kindergarten = Kindergarten.query.get_or_404(kindergarten_id)
    name = request.form.get('name')
    limit = int(request.form.get('limit'))
    age_group = int(request.form.get('age_group'))
    
    class_ = Class(
        name=name,
        kindergarten_id=kindergarten_id,
        limit=limit,
        age_group=age_group
    )
    db.session.add(class_)
    db.session.commit()
    
    flash(f'{kindergarten.name} kreşine {limit} öğrenci kapasiteli {name} sınıfı eklendi.')
    return redirect(url_for('manage_kindergartens'))

@app.route('/update_class/<int:class_id>', methods=['POST'])
@login_required
def update_class(class_id):
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    class_ = Class.query.get_or_404(class_id)
    name = request.form.get('name')
    limit = request.form.get('limit')
    age_group = request.form.get('age_group')
    
    if name:
        class_.name = name
    if limit:
        class_.limit = int(limit)
    if age_group:
        class_.age_group = int(age_group)
    
    db.session.commit()
    flash('Sınıf bilgileri güncellendi.')
    return redirect(url_for('manage_kindergartens'))

@app.route('/delete_class/<int:class_id>', methods=['POST'])
@login_required
def delete_class(class_id):
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    class_ = Class.query.get_or_404(class_id)
    
    if class_.students:
        flash('Öğrencisi olan sınıf silinemez.')
        return redirect(url_for('manage_kindergartens'))
    
    kindergarten_name = class_.kindergarten.name
    class_name = class_.name
    
    db.session.delete(class_)
    db.session.commit()
    
    flash(f'{kindergarten_name} kreşinden {class_name} sınıfı silindi.')
    return redirect(url_for('manage_kindergartens'))

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    kindergartens = Kindergarten.query.all()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Update student information
            form.populate_obj(student)
            
            # Update kindergarten preferences
            student.preferred_kindergarten_1_id = request.form.get('preferred_kindergarten_1', None)
            student.preferred_kindergarten_2_id = request.form.get('preferred_kindergarten_2', None)
            student.preferred_kindergarten_3_id = request.form.get('preferred_kindergarten_3', None)
            
            # Only admin can update class assignment
            if current_user.is_admin:
                new_class_id = request.form.get('class_id')
                if new_class_id:
                    new_class = Class.query.get(new_class_id)
                    if new_class and len(new_class.students) < new_class.limit:
                        student.class_id = new_class_id
                    else:
                        flash('Seçilen sınıf dolu veya mevcut değil.')
                else:
                    student.class_id = None
            
            # Recalculate points
            student.calculate_points()
            
            db.session.commit()
            flash('Öğrenci bilgileri güncellendi.')
            return redirect(url_for('student_list'))
    
    return render_template('edit_student_tr.html', form=form, student=student, kindergartens=kindergartens)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    student = Student.query.get_or_404(student_id)
    
    # Remove student from class if assigned
    if student.class_id:
        student.class_id = None
    
    db.session.delete(student)
    db.session.commit()
    
    flash(f'{student.name} öğrencisi başarıyla silindi.')
    return redirect(url_for('student_list'))

@app.route('/export_students')
@login_required
def export_students():
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    # Get all students
    students = Student.query.all()
    
    # Create a list of dictionaries with student data
    data = []
    for student in students:
        student_data = {
            'Ad Soyad': student.name,
            'TC Kimlik No': student.tc_number,
            'Doğum Tarihi': student.birth_date.strftime('%d.%m.%Y'),
            'Adres': student.address,
            'Puan': student.points,
            'Durum': 'Elendi' if student.disqualified else 'Uygun',
            'Atanan Sınıf': f"{student.assigned_class.kindergarten.name} - {student.assigned_class.name}" if student.assigned_class else 'Atanmadı',
            'Anne Adı': student.mother_name,
            'Anne Telefon': student.mother_phone,
            'Anne Eğitim': student.mother_education,
            'Anne Meslek': student.mother_job,
            'Baba Adı': student.father_name,
            'Baba Telefon': student.father_phone,
            'Baba Eğitim': student.father_education,
            'Baba Meslek': student.father_job
        }
        data.append(student_data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Öğrenci Listesi', index=False)
        
        # Auto-adjust columns' width
        worksheet = writer.sheets['Öğrenci Listesi']
        for i, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_length)
    
    output.seek(0)
    
    # Return Excel file
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='ogrenci_listesi.xlsx'
    )

@app.route('/undo_assignment', methods=['POST'])
@login_required
def undo_assignment():
    if not current_user.is_admin:
        flash('Bu işlemi yapmaya yetkiniz yok.')
        return redirect(url_for('index'))
    
    # Get all assigned students
    assigned_students = Student.query.filter(Student.class_id.isnot(None)).all()
    
    # Remove class assignments
    for student in assigned_students:
        student.class_id = None
    
    db.session.commit()
    
    flash('Tüm öğrenci yerleştirmeleri başarıyla geri alındı.')
    return redirect(url_for('assignment'))

# Create database tables
with app.app_context():
    db.create_all()
    # Create an admin user if it doesn't exist
    admin_username = os.environ.get('ADMIN_USERNAME', 'atakumbeladmin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'atakumbeladminkres')
    
    if not User.query.filter_by(username=admin_username).first():
        admin = User(username=admin_username, is_admin=True)
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True) 