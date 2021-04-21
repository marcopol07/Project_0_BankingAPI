from controllers import home_controller, bank_controller


def route(app):
    home_controller.route(app)
    bank_controller.route(app)