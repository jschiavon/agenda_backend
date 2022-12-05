from agenda_backend import create_app

# app = create_app(env='local')
app = create_app(env='aruba')

if __name__ == '__main__':
    app.debug = True
    app.run()