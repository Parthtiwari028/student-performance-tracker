import sqlite3

# Connect to database
connection = sqlite3.connect("students.db")
cursor = connection.cursor()


# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    python REAL NOT NULL,
    dbms REAL NOT NULL,
    dsa REAL NOT NULL
)
""")

connection.commit()

def get_marks(subject):
    while True:
        try:
            marks = float(input(f"Enter {subject} marks: "))

            if 0 <= marks <= 100:
                return marks

            print("Marks must be between 0 and 100!")

        except ValueError:
            print("Please enter a valid number!")
            
            
# Add Student
def add_student():
    
    while True:
        name = input("Enter student name: ").strip()

        if name:
            break

        print("Name cannot be empty!")

    python_marks = get_marks("Python")
    dbms_marks = get_marks("DBMS")
    dsa_marks = get_marks("DSA")

    cursor.execute("""
    INSERT INTO students (name, python, dbms, dsa)
    VALUES (?, ?, ?, ?)
    """, (name, python_marks, dbms_marks, dsa_marks))

    connection.commit()

    print("Student added successfully!")


# View Students
def view_students():

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    print("\n===== STUDENTS =====")

    if len(students) == 0:
        print("No students found.")

    else:
        for student in students:

            print(
                "ID:", student[0],
                "| Name:", student[1],
                "| Python:", student[2],
                "| DBMS:", student[3],
                "| DSA:", student[4]
            )


# Main Menu
while True:

    print("\n===== STUDENT PERFORMANCE TRACKER =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Calculate Average")
    print("5. Find Top Student")
    print("6. Delete Student")
    print("7. Exit")

    choice = input("Enter your choice: ")


    if choice == "1":

        add_student()


    elif choice == "2":

        view_students()


    elif choice == "3":
    
        name = input("Enter student name to search: ").strip()

        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ("%" + name + "%",)
        )

        students = cursor.fetchall()

        print("\n===== SEARCH RESULTS =====")

        if len(students) == 0:
            print("No student found.")

        else:
            for student in students:

                average = (
                    student[2] +
                    student[3] +
                    student[4]
                ) / 3

                print(
                    "ID:", student[0],
                    "| Name:", student[1],
                    "| Python:", student[2],
                    "| DBMS:", student[3],
                    "| DSA:", student[4],
                    "| Average:", round(average, 2)
                )

    elif choice == "4":
    
        name = input("Enter student name: ").strip()

        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ("%" + name + "%",)
        )

        students = cursor.fetchall()

        print("\n===== STUDENT AVERAGE =====")

        if len(students) == 0:

            print("No student found.")

        else:

            for student in students:

                average = (
                    student[2] +
                    student[3] +
                    student[4]
                ) / 3

                print(
                    "Name:", student[1],
                    "| Average:", round(average, 2)
                )

    elif choice == "5":
    
        cursor.execute("""
            SELECT
                id,
                name,
                python,
                dbms,
                dsa,
                (python + dbms + dsa) / 3 AS average
            FROM students
            ORDER BY average DESC
            LIMIT 1
        """)

        top_student = cursor.fetchone()

        print("\n===== TOP STUDENT =====")

        if top_student is None:

            print("No students found.")

        else:

            print(
                "ID:", top_student[0],
                "| Name:", top_student[1],
                "| Python:", top_student[2],
                "| DBMS:", top_student[3],
                "| DSA:", top_student[4],
                "| Average:", round(top_student[5], 2)
            )

    elif choice == "6":
    
        try:
            student_id = int(input("Enter student ID to delete: "))

            cursor.execute(
                "SELECT * FROM students WHERE id = ?",
                (student_id,)
            )

            student = cursor.fetchone()

            if student is None:

                print("Student not found!")

            else:

                cursor.execute(
                    "DELETE FROM students WHERE id = ?",
                    (student_id,)
                )

                connection.commit()

                print("Student deleted successfully!")

        except ValueError:

            print("Please enter a valid student ID!")

    elif choice == "7":

        print("Thank you for using Student Performance Tracker!")

        break


    else:

        print("Invalid choice!")


# Close database connection
connection.close()