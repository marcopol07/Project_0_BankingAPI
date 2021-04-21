from exceptions.account_not_found import AccountNotFound
from dao.model_dao import ModelDAO
from models.account import Account
from dao.db_connection import connection


class AccountDAO(ModelDAO):
    def new_object(self, client_id, account):
        sql = "INSERT INTO accounts VALUES (DEFAULT,%s,%s) RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (client_id, account.value))
        connection.commit()
        record = cursor.fetchone()
        return Account(record[0], record[1], record[2])

    def get_object(self, client_id, account_id):
        sql = "SELECT * FROM accounts WHERE client_id = %s and account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (client_id, account_id))

        record = cursor.fetchone()

        if record:
            return Account(record[0], record[1], record[2])
        else:
            raise AccountNotFound(f"Account with ID {account_id} not found for Client with ID {client_id}.")

    def get_all_objects(self):
        sql = "SELECT * FROM accounts"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        account_list = []
        for record in records:
            account = Account(record[0], record[1], record[2])
            account_list.append(account.json())

        return account_list

    @staticmethod
    def get_all_objects_from_client(client_id):
        sql = "SELECT * FROM accounts WHERE client_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        account_list = []
        for record in records:
            account = Account(record[0], record[1], record[2])
            account_list.append(account.json())

        return account_list

    def update_object(self, change):
        sql = "UPDATE accounts SET value=%s WHERE account_id=%s RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (change.value, change.account_id))
        connection.commit()

        return ""

    def delete_object(self, client_id, account_id):
        try:
            account = AccountDAO().get_object(client_id, account_id)
        except AccountNotFound as a:
            raise a

        sql = "DELETE FROM accounts WHERE client_id = %s and account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (client_id, account_id))
        connection.commit()

        return ""
