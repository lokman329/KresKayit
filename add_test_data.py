from app import app, db, Student, Kindergarten, Class
from datetime import datetime, date
import random

def create_test_data():
    # Clear existing data
    Student.query.delete()
    Class.query.delete()
    Kindergarten.query.delete()
    db.session.commit()

    # Create kindergartens and classes
    kindergartens = [
        {
            "name": "Atakum Merkez Kreş",
            "classes": [
                {"name": "Papatya", "limit": 15, "age_group": 3},
                {"name": "Gül", "limit": 15, "age_group": 4},
                {"name": "Menekşe", "limit": 15, "age_group": 5}
            ]
        },
        {
            "name": "Deniz Kreş",
            "classes": [
                {"name": "Martı", "limit": 20, "age_group": 3},
                {"name": "Yunus", "limit": 20, "age_group": 4},
                {"name": "Balina", "limit": 20, "age_group": 5}
            ]
        },
        {
            "name": "Güneş Kreş",
            "classes": [
                {"name": "Güneş A", "limit": 12, "age_group": 3},
                {"name": "Güneş B", "limit": 12, "age_group": 4},
                {"name": "Güneş C", "limit": 12, "age_group": 5},
                {"name": "Güneş D", "limit": 12, "age_group": 6}
            ]
        }
    ]

    created_kindergartens = {}
    for k_data in kindergartens:
        k = Kindergarten(name=k_data["name"])
        db.session.add(k)
        db.session.flush()
        
        created_kindergartens[k.name] = k.id
        
        for c_data in k_data["classes"]:
            c = Class(
                name=c_data["name"],
                kindergarten_id=k.id,
                limit=c_data["limit"],
                age_group=c_data["age_group"]
            )
            db.session.add(c)

    db.session.commit()

    # Test data scenarios
    students_data = [
        # 3 years old case
        {
            "name": "Ayşe Yılmaz",
            "tc_number": "10000000001",
            "birth_date": date(2021, 1, 15),  # 3 years old
            "address": "Atakum Merkez Mah.",
            "toilet_trained": True,
            "school_experience": True,
            "school_type": "Devlet",
            "sibling_count": 2,
            "mother_alive": True,
            "mother_name": "Fatma Yılmaz",
            "mother_phone": "5551112233",
            "mother_education": "Üniversite",
            "mother_job": "Memur",
            "mother_employer": "Atakum Belediyesi",
            "mother_salary": 15000,
            "father_alive": False,
            "father_name": None,
            "father_phone": None,
            "father_education": None,
            "father_job": None,
            "father_employer": None,
            "father_salary": 0,
            "house_ownership": "Kiracı",
            "marital_status": "Dul",
            "preferred_kindergarten_1_id": created_kindergartens["Atakum Merkez Kreş"],
            "preferred_kindergarten_2_id": created_kindergartens["Deniz Kreş"],
            "preferred_kindergarten_3_id": created_kindergartens["Güneş Kreş"]
        },
        # 4 years old case
        {
            "name": "Mehmet Demir",
            "tc_number": "10000000002",
            "birth_date": date(2020, 6, 20),  # 4 years old
            "address": "Atakum Sahil Mah.",
            "toilet_trained": True,
            "school_experience": False,
            "school_type": None,
            "sibling_count": 1,
            "mother_alive": True,
            "mother_name": "Zeynep Demir",
            "mother_phone": "5552223344",
            "mother_education": "Lise",
            "mother_job": "Öğretmen",
            "mother_employer": "Özel Okul",
            "mother_salary": 25000,
            "father_alive": True,
            "father_name": "Ali Demir",
            "father_phone": "5553334455",
            "father_education": "Üniversite",
            "father_job": "Mühendis",
            "father_employer": "ABC Şirketi",
            "father_salary": 35000,
            "house_ownership": "Ev Sahibi",
            "marital_status": "Evli",
            "preferred_kindergarten_1_id": created_kindergartens["Güneş Kreş"],
            "preferred_kindergarten_2_id": created_kindergartens["Atakum Merkez Kreş"],
            "preferred_kindergarten_3_id": None
        },
        # 5 years old case
        {
            "name": "Can Kaya",
            "tc_number": "10000000003",
            "birth_date": date(2019, 3, 10),  # 5 years old
            "address": "İlkadım Merkez",  # Not in Atakum
            "toilet_trained": True,
            "school_experience": True,
            "school_type": "Özel",
            "sibling_count": 0,
            "mother_alive": True,
            "mother_name": "Ayşe Kaya",
            "mother_phone": "5554445566",
            "mother_education": "Yüksek Lisans",
            "mother_job": "Doktor",
            "mother_employer": "Devlet Hastanesi",
            "mother_salary": 45000,
            "father_alive": True,
            "father_name": "Murat Kaya",
            "father_phone": "5555556677",
            "father_education": "Doktora",
            "father_job": "Akademisyen",
            "father_employer": "Üniversite",
            "father_salary": 40000,
            "house_ownership": "Ev Sahibi",
            "marital_status": "Evli",
            "preferred_kindergarten_1_id": created_kindergartens["Deniz Kreş"],
            "preferred_kindergarten_2_id": None,
            "preferred_kindergarten_3_id": None
        },
        # 6 years old case
        {
            "name": "Elif Şahin",
            "tc_number": "10000000004",
            "birth_date": date(2018, 1, 1),  # 6 years old
            "address": "Atakum Yeni Mah.",
            "toilet_trained": True,
            "school_experience": True,
            "school_type": "Devlet",
            "sibling_count": 1,
            "mother_alive": True,
            "mother_name": "Sema Şahin",
            "mother_phone": "5556667788",
            "mother_education": "Lise",
            "mother_job": "Ev Hanımı",
            "mother_employer": None,
            "mother_salary": 0,
            "father_alive": True,
            "father_name": "Kemal Şahin",
            "father_phone": "5557778899",
            "father_education": "Üniversite",
            "father_job": "Memur",
            "father_employer": "Atakum Belediyesi",
            "father_salary": 30000,
            "house_ownership": "Ev Sahibi",
            "marital_status": "Evli",
            "preferred_kindergarten_1_id": created_kindergartens["Güneş Kreş"],
            "preferred_kindergarten_2_id": None,
            "preferred_kindergarten_3_id": None
        },
        # Disqualified case (age)
        {
            "name": "Ahmet Yıldız",
            "tc_number": "10000000005",
            "birth_date": date(2017, 12, 1),  # 7 years old
            "address": "Atakum Deniz Mah.",
            "toilet_trained": True,
            "school_experience": False,
            "school_type": None,
            "sibling_count": 0,
            "mother_alive": True,
            "mother_name": "Hatice Yıldız",
            "mother_phone": "5558889900",
            "mother_education": "Üniversite",
            "mother_job": "Öğretmen",
            "mother_employer": "MEB",
            "mother_salary": 32000,
            "father_alive": True,
            "father_name": "Mustafa Yıldız",
            "father_phone": "5559990011",
            "father_education": "Üniversite",
            "father_job": "Mühendis",
            "father_employer": "XYZ Şirketi",
            "father_salary": 38000,
            "house_ownership": "Ev Sahibi",
            "marital_status": "Evli",
            "preferred_kindergarten_1_id": created_kindergartens["Güneş Kreş"],
            "preferred_kindergarten_2_id": None,
            "preferred_kindergarten_3_id": None
        }
    ]

    # Add more random students to fill up classes
    turkish_names = [
        "Zeynep", "Defne", "Eylül", "Nehir", "Ecrin",
        "Yusuf", "Ömer", "Miraç", "Eymen", "Aras"
    ]
    turkish_surnames = [
        "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik",
        "Yıldız", "Özdemir", "Arslan", "Doğan", "Kılıç"
    ]

    tc_base = 10000000006
    # Add students with specific age distributions
    age_distribution = {
        3: 10,  # 10 students of age 3
        4: 10,  # 10 students of age 4
        5: 10,  # 10 students of age 5
        6: 5    # 5 students of age 6
    }

    for age, count in age_distribution.items():
        for i in range(count):
            birth_year = datetime.utcnow().year - age
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            
            mother_salary = random.randint(22000, 100000)
            father_salary = random.randint(22000, 100000)
            
            student_data = {
                "name": f"{random.choice(turkish_names)} {random.choice(turkish_surnames)}",
                "tc_number": str(tc_base),
                "birth_date": date(birth_year, birth_month, birth_day),
                "address": "Atakum" if random.random() > 0.3 else "İlkadım",
                "toilet_trained": True,
                "school_experience": random.choice([True, False]),
                "school_type": random.choice(["Devlet", "Özel", None]),
                "sibling_count": random.randint(0, 3),
                "mother_alive": True,
                "mother_name": f"Anne {random.choice(turkish_names)}",
                "mother_phone": f"555{random.randint(1000000, 9999999)}",
                "mother_education": random.choice(["İlkokul", "Ortaokul", "Lise", "Üniversite"]),
                "mother_job": random.choice(["Öğretmen", "Memur", "Doktor", "Ev Hanımı"]),
                "mother_employer": random.choice(["Kamu", "Özel Sektör", "Atakum Belediyesi"]),
                "mother_salary": mother_salary,
                "father_alive": random.choice([True, False]),
                "father_name": f"Baba {i}",
                "father_phone": f"555{random.randint(1000000, 9999999)}",
                "father_education": random.choice(["İlkokul", "Ortaokul", "Lise", "Üniversite", "Yüksek Lisans", "Doktora"]),
                "father_job": random.choice(["Mühendis", "Öğretmen", "Doktor", "Avukat", "Esnaf", "Memur"]),
                "father_employer": random.choice(["Kamu", "Özel Sektör", "Atakum Belediyesi"]),
                "father_salary": father_salary,
                "house_ownership": random.choice(["Ev Sahibi", "Kiracı"]),
                "marital_status": random.choice(["Evli", "Dul", "Ayrı"]),
                "preferred_kindergarten_1_id": random.choice(list(created_kindergartens.values())),
                "preferred_kindergarten_2_id": random.choice([None] + list(created_kindergartens.values())),
                "preferred_kindergarten_3_id": random.choice([None] + list(created_kindergartens.values()))
            }
            tc_base += 1
            students_data.append(student_data)

    # Add all students to database
    for student_data in students_data:
        student = Student(**student_data)
        student.calculate_points()
        db.session.add(student)

    db.session.commit()
    print("Test data has been added successfully!")

if __name__ == "__main__":
    with app.app_context():
        create_test_data() 