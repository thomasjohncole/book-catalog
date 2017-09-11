from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(__name__)

@app.route('/')
def indexPage():
    return "This is the index page!"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)




