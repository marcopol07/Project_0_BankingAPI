import unittest

from exceptions.client_not_found import ClientNotFound
from dao.model_dao import ModelDAO
from models.client import Client
from dao.db_connection import connection


class ClientDAO(ModelDAO):
    def new_object(self, client, null=None):
        sql = "INSERT INTO clients VALUES (DEFAULT,%s,%s) RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (client.username, client.password))
        connection.commit()
        record = cursor.fetchone()
        return Client(record[0], record[1], record[2])

    def get_object(self, client_id, null=None):
        sql = "SELECT * FROM clients WHERE client_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])

        record = cursor.fetchone()

        if record:
            return Client(record[0], record[1], record[2])
        else:
            raise ClientNotFound(f"Client with ID {client_id} not found.")

    def get_all_objects(self):
        sql = "SELECT * FROM clients"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        client_list = []
        for record in records:
            client = Client(record[0], record[1], record[2])
            client_list.append(client.json())

        return client_list

    def update_object(self, change):
        sql = "UPDATE clients SET username=%s,password=%s WHERE client_id=%s RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (change.username, change.password, change.client_id))
        connection.commit()

        return ""

    def delete_object(self, client_id, null=None):
        try:
            ClientDAO.get_object(self, client_id)
        except ClientNotFound as c:
            raise c

        sql = "DELETE FROM clients WHERE client_id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        connection.commit()
