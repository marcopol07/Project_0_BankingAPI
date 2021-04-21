def route(app):
    @app.route("/")
    def greeting():
        return "Welcome to the Banking App. Get started by sending your requests now!"
