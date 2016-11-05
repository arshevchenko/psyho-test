import MySQLdb
from app import public_key, private_key

class DataBase:
    cursor = None
    server = 'localhost'
    user = 'root'
    password = 'E3HKsGhpDeg'
    database = 'psycho'

    @staticmethod
    def connect():
        connection = MySQLdb.connect('localhost', 'root', 'E3HKsGhpDeg', 'psycho')
        return connection

    @staticmethod
    def user_select_tests():
        data_records = []
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute('SELECT id, test_name FROM test_list;')
        for row in cursor.fetchall():
            test = {'id': row[0], 'name': row[1]}
            data_records.append(test)

        connection.close()
        return data_records

    @staticmethod
    def get_one_test(id):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute('SELECT name, test_text FROM test_list WHERE id = %d;' % id)
        row = cursor.fetchone();

        return [{'name': row[0], 'test_text': row[1]}]


# Administrative part
    @staticmethod
    def add_test(text, adm_id, txt_name):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO test_list (test_text, admin_id, test_name)
            VALUES ("%s", %d, "%s");
            """ % text, adm_id, txt_name)
        connection.commit()
        connection.close()

    @staticmethod
    def admin_user_results():
        data_records = []
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT test_results.id, test_users.first_name, test_users.last_name,
                   test_list.test_name, test_results.test_time,
                   test_results.err_count
                FROM test_results, test_users, test_list
                WHERE test_results.user_id = test_users.id
                  AND test_results.test_id = test_list.id;
            """)
        for row in cursor.fetchall():
            test = {
                'id': row[0], 'first_name': row[1], 'last_name': row[2],
                'test_name': row[3], 'test_time': row[4], 'err_count': row[5]
            }
            data_records.append(test)

        connection.close()
        return data_records

    @staticmethod
    def check_adm_record(name, passw):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM user_admin WHERE user_name='%s'
                                     AND user_pass='%s';
            """ % name, passw)
        row = cursor.fetchone()
        if row == None:
            return False
        else:
            return [{'usr_key': rsa.encrypt(row[0])}]
