from flask import Flask, render_template

app_web = Flask(__name__)

@app_web.route('/skynet_interface')
def skynet_interface():
    return render_template('skynet_interface.html')

if __name__ == '__main__':
    app_web.run(port=6123)
