# coding: ascii
import MySQLdb
import hashlib
from app import public_key, private_key

class DataBase:
    cursor = None

    @staticmethod
    def connect():
        connection = MySQLdb.connect('localhost', 'root', 'E3HKsGhpDeg', 'psycho')
        return connection

    @staticmethod
    def all_tests():
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
    def add_user(first_name, last_name):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO test_users (first_name, last_name)
            VALUES ('%s', '%s')
        """ % (first_name.encode("utf-8"),
               last_name.encode("utf-8")))
        connection.commit()

        cursor.execute("""
            SELECT id FROM test_users WHERE id = (SELECT MAX(id) FROM test_users);
         """)
        row = cursor.fetchone()
        connection.close()

        return [{"uni": hashlib.md5(str(row[0])).hexdigest(), "id": str(row[0])}]


    @staticmethod
    def get_test(id):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute('SELECT test_name, test_text FROM test_list WHERE id = %d;' % id)
        row = cursor.fetchone();

        return [{'name': row[0], 'text': row[1]}]

    @staticmethod
    def add_stat(uid, test_id, test_time, err_count, pos):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO test_result (user_id, test_id, test_time, err_count, positions)
            VALUES (%s, %s, '%s', %s, '%s');
        """ % (uid,
               test_id,
               test_time.encode("utf-8"),
               err_count,
               pos.encode("utf-8")))
        connection.commit()
        connection.close()

# Administrative part
    @staticmethod
    def add_test(text, adm_id, txt_name):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO test_list (test_text, admin_id, test_name)
            VALUES ('%s', %s, '%s');
            """ % (text.encode("utf-8"), adm_id.encode("utf-8"), txt_name.encode("utf-8")))
        connection.commit()
        connection.close()

    @staticmethod
    def get_all_results():
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
    def get_result(id):
        data_records = []
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT test_id, test_time, err_count FROM test_result WHERE user_id = %d" % id)
        rows = cursor.fetchall()

        if rows == None:
            return [{"has_info": False}]
            connection.close()

        for row in rows:
            result = {'test_id': row[0], 'test_time': str(row[1]), 'err_count': row[2]}
            data_records.append(result)

        connection.close()
        return data_records

    @staticmethod
    def get_last_result(id):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT test_id, test_time, err_count FROM test_result WHERE user_id = %d and id = (SELECT MAX(id) FROM test_result WHERE user_id = %d);" % (id, id))
        row = cursor.fetchone()
        print row
        result = {'test_id': row[0], 'test_time': str(row[1]), 'err_count': row[2]}

        connection.close()
        return result


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
            return [{'usr_key': str(hashlib.md5(row[0]).hexdigest())}]


    @staticmethod
    def remove_test(id):
        connection = DataBase.connect()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM test_list WHERE id = %d;" % id)
        connection.commit()
        connection.close()
