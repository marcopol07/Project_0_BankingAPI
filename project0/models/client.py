class Client:
    def __init__(self, client_id=0, username="", password=""):
        self.client_id = client_id
        self.username = username
        self.password = password

    def json(self):
        return {
            "clientId": self.client_id,
            "username": self.username,
            "password": self.password
        }

    def __repr__(self):
        return str(self.json())

    @staticmethod
    def json_parse(json):
        client = Client()
        client.client_id = json["clientId"] if "clientId" in json else 0
        client.username = json["username"]
        client.password = json["password"]

        return client


if __name__ == '__main__':
    marc = Client(98, "marc", "password")
    print(marc.client_id)
    print(marc.password)
