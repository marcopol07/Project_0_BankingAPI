import decimal
import logging

from flask import jsonify, request
from werkzeug.exceptions import BadRequestKeyError

from exceptions.account_not_found import AccountNotFound
from exceptions.client_not_found import ClientNotFound
from exceptions.insufficient_funds import InsufficientFunds
from models.account import Account
from services.banking_service import BankingService
from models.client import Client


def route(app):
    logging.basicConfig(filename="app.log", filemode="a", format="%(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)

    @app.route("/clients", methods=["GET"])
    def get_all_clients():
        return jsonify(BankingService.get_all_clients()), 200

    @app.route("/clients/<client_id>", methods=["GET"])
    def get_client(client_id):
        try:
            client = BankingService.get_client_by_id(int(client_id))
            return jsonify(client.json()), 200
        except ValueError:
            logging.warning("Invalid Client ID input.")
            return "Not a valid Client ID.", 400
        except ClientNotFound as c:
            logging.warning(f"No client found with ID {client_id}.")
            return c.message, 404

    @app.route("/clients", methods=["POST"])
    def post_client():
        try:
            client = Client.json_parse(request.json)
            client = BankingService.new_client(client)
            return jsonify(client.json()), 201
        except KeyError:
            logging.exception("User input resulted in KeyError.")
            return "A username and password are required to register a client.", 400

    @app.route("/clients/<client_id>", methods=["PUT"])
    def put_client(client_id):
        clienty = get_client(client_id)
        if clienty[1] == 404 or clienty[1] == 400:
            return clienty

        try:
            client = Client.json_parse(request.json)
            client.client_id = int(client_id)
            BankingService.update_client(client)
            return jsonify(client.json()), 200
        except KeyError:
            logging.warning("User input resulted in KeyError.")
            return "Please input both the new username and password to edit client account.", 400

    @app.route("/clients/<client_id>", methods=["DELETE"])
    def delete_client(client_id):
        try:
            BankingService.delete_client(client_id)
            return "", 204
        except ValueError:
            logging.warning("Invalid Client ID input.")
            return "Not a valid Client ID.", 400
        except ClientNotFound as c:
            logging.warning(f"No client found with ID {client_id}.")
            return c.message, 404

    @app.route("/clients/<client_id>/accounts", methods=["GET"])
    def get_all_accounts_for_client(client_id):
        try:
            max_value = float(request.args["amountLessThan"])
        except BadRequestKeyError:
            max_value = None
        except ValueError:
            return "Parameters must be of type int or float.", 400
        try:
            min_value = float(request.args["amountGreaterThan"])
        except BadRequestKeyError:
            min_value = 0
        except ValueError as e:
            logging.warning("Can't retrieve accounts in invalid range.")
            return "Parameters must be of type int or float.", 400

        if max_value and max_value < min_value:
            return "This client has no linked accounts with given parameters.", 200

        accounts = BankingService.get_all_client_accounts(client_id, min_value, max_value)
        if accounts:
            return jsonify(accounts), 200
        else:
            return "This client has no linked accounts with given parameters.", 200

    # @app.route("/clients/<client_id>/accounts?amountLessThan=<max_value>&amountGreaterThan=<min_value>")

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
    def get_account_for_client(client_id, account_id):
        clienty = get_client(client_id)
        if clienty[1] == 404 or clienty[1] == 400:
            return clienty

        try:
            account = BankingService.get_account(int(client_id), int(account_id))
            return jsonify(account.json()), 200
        except ValueError:
            logging.warning("Invalid Account ID input.")
            return f"Not a valid Account ID.", 400
        except AccountNotFound as a:
            logging.warning(f"No account found with ID {account_id} for client {client_id}.")
            return a.message, 404

    @app.route("/clients/<client_id>/accounts", methods=["POST"])
    def post_account(client_id):
        clienty = get_client(client_id)
        if clienty[1] == 404 or clienty[1] == 400:
            return clienty

        account = Account.json_parse(request.json)
        account = BankingService.new_account(client_id, account)

        return jsonify(account.json()), 201

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["PUT"])
    def put_account(client_id, account_id):
        clienty = get_client(client_id)
        if clienty[1] == 404 or clienty[1] == 400:
            return clienty

        accounty = get_account_for_client(client_id, account_id)
        if accounty[1] == 404 or accounty[1] == 400:
            return accounty

        try:
            account = Account.json_parse(request.json)
            account.account_id = int(account_id)
            account.client_id = int(client_id)
            BankingService.update_account(account)
            return jsonify(account.json()), 200
        except KeyError:
            logging.warning("Could not update account with information provided.")
            return "Please input a new value for the account.", 400

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["DELETE"])
    def delete_account(client_id, account_id):
        clienty = get_client(client_id)
        if clienty[1] == 404 or clienty[1] == 400:
            return clienty

        try:
            BankingService.delete_account(client_id, account_id)
            return "", 204
        except ValueError:
            logging.warning("Invalid Account ID input.")
            return "Not a valid Account ID.", 400
        except AccountNotFound as a:
            logging.warning(f"No account found with ID {account_id} for client with ID {client_id}.")
            return a.message, 404

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["PATCH"])
    def deposit_or_withdraw(client_id, account_id):
        clienty = get_client(client_id)
        if clienty[1] == 404 or clienty[1] == 400:
            return clienty

        accounty = get_account_for_client(client_id, account_id)
        if accounty[1] == 404 or accounty[1] == 400:
            return accounty

        try:
            change = request.json
            if "deposit" in change.keys() and "withdraw" in change.keys():
                return "Please choose to either deposit or withdraw, not both.", 400
            elif "deposit" in change.keys():
                new_account = BankingService.deposit_funds(client_id, account_id, change["deposit"])
                return jsonify(new_account.json()), 200
            elif "withdraw" in change.keys():
                new_account = BankingService.withdraw_funds(client_id, account_id, change["withdraw"])
                return jsonify(new_account.json()), 200
            else:
                return "Please choose to either deposit or withdraw.", 400
        except decimal.InvalidOperation:
            logging.warning("Must deposit or withdraw a numeric amount.")
            return "The amount to deposit or withdraw must be numeric.", 400
        except InsufficientFunds as e:
            logging.warning("Attempted to withdraw more funds than exist in account.")
            return e.message, 422

    @app.route("/clients/<client_id>/accounts/<account1_id>/transfer/<account2_id>", methods=["PATCH"])
    def transfer_funds(client_id, account1_id, account2_id):
        clienty = get_client(client_id)
        if clienty[1] == 404 or clienty[1] == 400:
            return clienty

        accounty1 = get_account_for_client(client_id, account1_id)
        if accounty1[1] == 404 or accounty1[1] == 400:
            return accounty1

        accounty2 = get_account_for_client(client_id, account2_id)
        if accounty2[1] == 404 or accounty2[1] == 400:
            return accounty2

        try:
            change = request.json
            if "transfer" in change.keys():
                new_account1 = BankingService.withdraw_funds(client_id, account1_id, change["transfer"])
                new_account2 = BankingService.deposit_funds(client_id, account2_id, change["transfer"])
                return jsonify([new_account1.json(), new_account2.json()]), 200
            else:
                return "Please enter an amount to transfer.", 400
        except decimal.InvalidOperation:
            logging.warning("Must deposit or withdraw a numeric amount.")
            return "The amount to deposit or withdraw must be numeric.", 400
        except InsufficientFunds as e:
            logging.warning("Attempted to withdraw more funds than exist in account.")
            return e.message, 422
