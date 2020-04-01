import psycopg2 as pg

def create_db():
    with pg.connect(dbname='hw_db', user='u', password='pass') as conn:
        with conn.cursor() as cur:
            cur.execute("""create table if not exists student(
                id integer primary key,
                name varchar(100),
                gpa numeric(10,2) null,
                birth timestamp with time zone null
                )
                """)
            cur.execute("""create table if not exists course(
                id integer primary key,
                name varchar(100)
                )
                """)
            cur.execute("""create table if not exists student_course(
                id serial primary key,
                student_id integer references student(id),
                course_id integer references course(id)
            )
            """)

def get_students(course_id):
    with pg.connect(dbname='hw_db', user='u', password='pass') as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from student_course where course_id = %s""", (course_id,))
            resp = cur.fetchall()
            res = []
            keys = ['id', 'name', 'gpa', 'birth']
            for r in resp:
                cur.execute("""select * from student where id = %s""", (r[1],))
                res.append(cur.fetchall())
            return res

def add_student(student):
    with pg.connect(dbname='hw_db', user='u', password='pass') as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into student values(%s, %s, %s, %s)""",
            (student['id'], student['name'], student.get('gpa'), student.get('birth')))

def add_course(course):
    with pg.connect(dbname='hw_db', user='u', password='pass') as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into course values(%s, %s)""",
            (course['id'], course['name']))

def add_students(course_id, students):
    with pg.connect(dbname='hw_db', user='u', password='pass') as conn:
        with conn.cursor() as cur:
            for student in students:
                try:
                    cur.execute("""insert into student_course(student_id, course_id) values(%s, %s)""", (student, course_id))
                except Exception:
                    conn.rollback()
                    print('wrong course id or students ids')

def get_student(id):
    with pg.connect(dbname='hw_db', user='u', password='pass') as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from student where id=%s""", (id,))
            x = cur.fetchall()
            return x
