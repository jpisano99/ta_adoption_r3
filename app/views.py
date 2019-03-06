from app import app


@app.route('/')
def index():
    print('index')
    return 'Hello Jimmy!'


@app.route('/test')
def test():
    print('hello')
    return 'index.html'
