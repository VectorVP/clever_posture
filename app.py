from flask import Flask, request, render_template, url_for

app = Flask(__name__)
app.secret_key = b'askghuy3y8rhf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/home')
def home:
    return render_template('templates/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threade=True)
