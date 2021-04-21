from re import sub
from decimal import Decimal

from dao.client_dao import ClientDAO
from dao.account_dao import AccountDAO
from exceptions.insufficient_funds import InsufficientFunds
from models.account import Account


class BankingService:
    client_dao = ClientDAO()
    account_dao = AccountDAO()

    @classmethod
    def new_client(cls, client):
        return cls.client_dao.new_object(client)

    @classmethod
    def get_all_clients(cls):
        return cls.client_dao.get_all_objects()

    @classmethod
    def get_client_by_id(cls, client_id):
        return cls.client_dao.get_object(client_id)

    @classmethod
    def update_client(cls, change):
        return cls.client_dao.update_object(change)

    @classmethod
    def delete_client(cls, client_id):
        return cls.client_dao.delete_object(client_id)

    @classmethod
    def new_account(cls, client_id, account):
        return cls.account_dao.new_object(client_id, account)

    @classmethod
    def get_account(cls, client_id, account_id):
        return cls.account_dao.get_object(client_id, account_id)

    @classmethod
    def get_all_client_accounts(cls, client_id, min_value=0, max_value=None):
        accounts = cls.account_dao.get_all_objects_from_client(client_id)
        id_to_remove = []
        for account in accounts:
            value = Decimal(sub(r'[^\d.]', '', account['value']))
            if max_value and (Decimal(max_value) < value):
                id_to_remove.append(accounts.index(account))
            if min_value and (value < Decimal(min_value)):
                id_to_remove.append(accounts.index(account))
            else:
                continue

        for i in reversed(id_to_remove):
            accounts.remove(accounts[i])

        return accounts

    @classmethod
    def update_account(cls, change):
        return cls.account_dao.update_object(change)

    @classmethod
    def delete_account(cls, client_id, account_id):
        return cls.account_dao.delete_object(client_id, account_id)

    @classmethod
    def deposit_funds(cls, client_id, account_id, deposit_amount='0'):
        if not isinstance(deposit_amount, str):
            deposit_amount = str(deposit_amount)
        account = cls.account_dao.get_object(client_id, account_id)
        account_value = Decimal(sub(r'[^\d.]', '', account.value))
        account_value += Decimal(sub(r'[^\d.]', '', deposit_amount))

        change = Account(account_id, client_id, float(account_value))
        cls.account_dao.update_object(change)
        return change

    @classmethod
    def withdraw_funds(cls, client_id, account_id, withdraw_amount='0'):
        if not isinstance(withdraw_amount, str):
            withdraw_amount = str(withdraw_amount)
        account = cls.account_dao.get_object(client_id, account_id)
        account_value = Decimal(sub(r'[^\d.]', '', account.value))
        withdraw_amount = Decimal(sub(r'[^\d.]', '', withdraw_amount))
        if account_value < withdraw_amount:
            raise InsufficientFunds(f"Account {account_id} does not have the funds to withdraw ${withdraw_amount}.")
        else:
            account_value -= withdraw_amount
            change = Account(account_id, client_id, float(account_value))
            cls.account_dao.update_object(change)
            return change

