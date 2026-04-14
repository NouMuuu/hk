from flask import Flask, render_templates
app = Flask(__name__)
@app.route('/')
def index():
    render_templates('index.html')

if __name__ == '__main--':
    app.run(debug=True)