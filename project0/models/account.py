class Account:
    def __init__(self, account_id=0, client_id=0, value="$0.00"):
        self.account_id = account_id
        self.client_id = client_id
        self.value = value

    def json(self):
        return {
            "accountId": self.account_id,
            "clientId": self.client_id,
            "value": self.value
        }

    @staticmethod
    def json_parse(json):
        account = Account()
        account.account_id = json["accountId"] if "accountId" in json else 0
        account.client_id = json["clientId"] if "clientId" in json else 0
        account.value = json["value"] if "value" in json else "$0.00"

        return account
