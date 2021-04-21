import unittest
from client_dao import ClientDAO
from account_dao import AccountDAO
from exceptions.account_not_found import AccountNotFound
from exceptions.client_not_found import ClientNotFound
from models.client import Client
from models.account import Account


class TestDAO(unittest.TestCase):
    def test_create_new_client_success(self):
        client = Client(username="tester", password="password")
        new_client = ClientDAO().new_object(client)
        self.assertEqual(isinstance(new_client, Client), True)

    def test_get_all_clients_success(self):
        clients = ClientDAO().get_all_objects()
        for client in clients:
            if not isinstance(Client.json_parse(client), Client):
                raise AssertionError("Not every return is a Client object.")
        assert True

    def test_get_client_success(self):
        check_client = Client(1, "marc", "password").json()
        client = ClientDAO().get_object(1).json()
        self.assertDictEqual(client, check_client)

    def test_get_client_not_found(self):
        try:
            client = ClientDAO().get_object(100000)
            raise AssertionError("There should be no client with ID 100000.")
        except ClientNotFound as c:
            self.assertEqual(c.message, "Client with ID 100000 not found.")

    def test_update_client_success(self):
        client = Client(777, "goose", "berry")
        result = ClientDAO().update_object(client)
        self.assertEqual(result, "")

    def test_delete_client_no_client_found(self):
        try:
            ClientDAO().delete_object(100000)
            raise AssertionError
        except ClientNotFound as c:
            self.assertEqual(c.message, "Client with ID 100000 not found.")

    def test_create_new_account_success(self):
        account = Account(value=1000)
        new_account = AccountDAO().new_object(1, account)
        self.assertEqual(isinstance(new_account, Account), True)

    def test_get_all_accounts_success(self):
        accounts = AccountDAO().get_all_objects()
        for account in accounts:
            if not isinstance(Account.json_parse(account), Account):
                raise AssertionError("Not every return is an Account object.")
        assert True

    def test_get_all_accounts_for_client_success(self):
        accounts = AccountDAO().get_all_objects_from_client(1)
        for account in accounts:
            if not isinstance(Account.json_parse(account), Account):
                raise AssertionError("Not every return is an Account object.")
        assert True

    def test_update_account_success(self):
        account = Account(5, 1, 1000)
        result = AccountDAO().update_object(account)
        self.assertEqual(result, "")

    def test_delete_account_account_not_found(self):
        try:
            account = AccountDAO().delete_object(1000, 100000)
            raise AssertionError("Account should not exist")
        except AccountNotFound as a:
            self.assertEqual(a.message, "Account with ID 100000 not found for Client with ID 1000.")


if __name__ == '__main__':
    unittest.main()
