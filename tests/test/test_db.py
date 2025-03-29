from psycopg2.extras import RealDictCursor


def test_db(db):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('select  * from dev.fitness_club')
        print(cursor.fetchall())
