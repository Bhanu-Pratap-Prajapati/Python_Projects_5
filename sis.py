import mysql.connector
import csv
def connect():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="bp37@73pb",
        database="data"
    )
    return conn

def setup_database():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            student_id INT,
            subject VARCHAR(100),
            score INT,
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
def calculate_grade(avg):
  
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'

def calculate_gpa(marks):  
    total_points = 0
    for _, score in marks:
        if score >= 90:
            total_points += 4.0
        elif score >= 80:
            total_points += 3.0
        elif score >= 70:
            total_points += 2.0
        elif score >= 60:
            total_points += 1.0
        else:
            total_points += 0.0
    return round(total_points / len(marks), 2) if marks else 0.0

def import_students_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute("INSERT INTO students (id, name) VALUES (%s, %s)", (int(row['id']), row['name']))
                student_id = int(row['id'])
                for subject in row['subjects'].split(','):
                    subj, score = subject.split(':')
                    cur.execute("INSERT INTO marks (student_id, subject, score) VALUES (%s, %s, %s)",
                                (student_id, subj.strip(), int(score)))
        conn.commit()
        print("✅ Data imported successfully.")
    except Exception as e:
        print(f"❌ Error importing data: {e}")
    finally:
        conn.close()

def export_students_to_csv(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM students')
        students = cur.fetchall()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name', 'subjects'])

            for student in students:
                sid, name = student
                cur.execute("SELECT subject, score FROM marks WHERE student_id = %s", (sid,))
                marks = cur.fetchall()
                subjects = ','.join([f"{s}:{sc}" for s, sc in marks])
                writer.writerow([sid, name, subjects])
        print("✅ Data exported successfully.")
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
    finally:
        conn.close()

def add_student(student_id, name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (id, name) VALUES (%s, %s)", (student_id, name))
    conn.commit()
    conn.close()

def update_student(student_id, name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name = %s WHERE id = %s", (name, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM marks WHERE student_id = %s", (student_id,))
    cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    conn.close()

def enter_marks(student_id, subject, score):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO marks (student_id, subject, score) VALUES (%s, %s, %s)", (student_id, subject, score))
    conn.commit()
    conn.close()

def view_summary(student_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT name FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()

    if not student:
        print("❌ Student not found.")
        conn.close()
        return

    print(f"\n📘 Student: {student[0]}")
    cur.execute("SELECT subject, score FROM marks WHERE student_id = %s", (student_id,))
    marks = cur.fetchall()

    if not marks:
        print("⚠️ No marks found for this student.")
        conn.close()
        return

    total = sum(score for _, score in marks)
    count = len(marks)
    avg = total / count if count else 0
    grade = calculate_grade(avg)
    gpa = calculate_gpa(marks)

    for subject, score in marks:
        print(f"{subject}: {score}")

    print(f"\n📊 Average: {avg:.2f}, Grade: {grade}, GPA: {gpa}")
    conn.close()

def find_class_topper():
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id FROM students')
    students = cur.fetchall()

    topper = None
    highest_avg = 0

    for (sid,) in students:
        cur.execute('SELECT score FROM marks WHERE student_id = %s', (sid,))
        scores = cur.fetchall()
        if scores:
            total = sum(score[0] for score in scores)
            avg = total / len(scores)
            if avg > highest_avg:
                highest_avg = avg
                topper = sid

    if topper:
        cur.execute("SELECT name FROM students WHERE id = %s", (topper,))
        name = cur.fetchone()[0]
        print(f"\n🏆 Class Topper: {name} (ID: {topper}) with Average: {highest_avg:.2f}")
    else:
        print("⚠️ No data available.")
    conn.close()
def menu():
    setup_database()

    while True:
        print("\n--- Student Information System ---")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Enter Marks")
        print("5. View Student Summary")
        print("6. Find Class Topper")
        print("7. Import Students from CSV")
        print("8. Export Students to CSV")
        print("0. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                sid = int(input("Enter student ID: "))
                name = input("Enter name: ").strip()
                add_student(sid, name)

            elif choice == "2":
                sid = int(input("Enter student ID: "))
                name = input("New name: ").strip()
                update_student(sid, name)

            elif choice == "3":
                sid = int(input("Enter student ID to delete: "))
                delete_student(sid)

            elif choice == "4":
                sid = int(input("Enter student ID: "))
                subject = input("Enter subject: ").strip()
                score = int(input("Enter score: "))
                enter_marks(sid, subject, score)

            elif choice == "5":
                sid = int(input("Student ID: "))
                view_summary(sid)

            elif choice == "6":
                find_class_topper()

            elif choice == "7":
                filename = input("CSV filename to import: ")
                import_students_from_csv(filename)

            elif choice == "8":
                filename = input("CSV filename to export: ")
                export_students_to_csv(filename)

            elif choice == "0":
                print("👋 Exiting...")
                break

            else:
                print("❌ Invalid choice. Try again.")

        except Exception as e:
            print(f"🚨 An error occurred: {e}")

if __name__ == "__main__":
    menu()
