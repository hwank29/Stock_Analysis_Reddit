from .website import app
from waitress import serve

# def create_app():
#     return app

if __name__ == '__main__':
    # app.run()
    serve(app, host="0.0.0.0", port=8080)

