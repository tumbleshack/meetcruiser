from backend import create_app, initialize_socket

app = create_app(enable_sockets=False)
socket_app = initialize_socket(app)
socket_app.run(app, debug=True)