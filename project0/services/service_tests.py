import unittest

from exceptions.account_not_found import AccountNotFound
from exceptions.client_not_found import ClientNotFound
from models.account import Account
from models.client import Client
from services.banking_service import BankingService


class TestService(unittest.TestCase):
    def test_create_new_client(self):
        client = Client(username="tester", password="password")
        new_client = BankingService().new_client(client)
        self.assertEqual(isinstance(new_client, Client), True)

    def test_get_all_clients_success(self):
        clients = BankingService().get_all_clients()
        for client in clients:
            if not isinstance(Client.json_parse(client), Client):
                raise AssertionError("Not every return is a Client object.")
        assert True

    def test_get_client_success(self):
        check_client = Client(1, "marc", "password").json()
        client = BankingService().get_client_by_id(1).json()
        self.assertDictEqual(client, check_client)

    def test_get_client_not_found(self):
        try:
            client = BankingService().get_client_by_id(100000)
            raise AssertionError("There should be no client with ID 100000.")
        except ClientNotFound as c:
            self.assertEqual(c.message, "Client with ID 100000 not found.")

    def test_update_client_success(self):
        client = Client(777, "goose", "berry")
        result = BankingService().update_client(client)
        self.assertEqual(result, "")

    def test_delete_client_no_client_found(self):
        try:
            BankingService().delete_client(100000)
            raise AssertionError
        except ClientNotFound as c:
            self.assertEqual(c.message, "Client with ID 100000 not found.")

    def test_create_new_account_success(self):
        account = Account(value=1000)
        new_account = BankingService().new_account(1, account)
        self.assertEqual(isinstance(new_account, Account), True)

    def test_get_all_client_accounts_success(self):
        accounts = BankingService().get_all_client_accounts(1)
        for account in accounts:
            if not isinstance(Account.json_parse(account), Account):
                raise AssertionError("Not every return is an Account object.")
        assert True

    def test_update_account_success(self):
        account = Account(5, 1, 1000)
        result = BankingService().update_account(account)
        self.assertEqual(result, "")

    def test_delete_account_account_not_found(self):
        try:
            account = BankingService().delete_account(1000, 100000)
            raise AssertionError("Account should not exist.")
        except AccountNotFound as a:
            self.assertEqual(a.message, "Account with ID 100000 not found for Client with ID 1000.")

    def test_deposit_funds_invalid_client(self):
        try:
            value = BankingService().deposit_funds(client_id=100000, account_id=100, deposit_amount=100)
            raise AssertionError("Account should not exist.")
        except AccountNotFound as a:
            self.assertEqual(a.message, "Account with ID 100 not found for Client with ID 100000.")

    def test_withdraw_funds_invalid_client(self):
        try:
            value = BankingService().withdraw_funds(client_id=100000, account_id=100, withdraw_amount=100)
            raise AssertionError("Account should not exist.")
        except AccountNotFound as a:
            self.assertEqual(a.message, "Account with ID 100 not found for Client with ID 100000.")


if __name__ == '__main__':
    unittest.main()
