
import requests
import os
from flask import Flask, request, redirect, url_for, render_template, Response
from werkzeug import secure_filename
from werkzeug.contrib.fixers import ProxyFix
import gmail_filter_refactor


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def home_page():
    #print flask.url_for('resources/css', filename='style.css')
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            xml = gmail_filter_refactor.main(filename)
            return Response(xml, mimetype='text/xml')
            
            # with open(filename) as fp:
            #     print fp.read()
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file', filename=filename))
        
        ### Working Captcha Code ###
        # payload = {
        #     "secret" : app.config.get('SECRET'),
        #     "response" : request.form['g-recaptcha-response'],
        #     "remoteip" : request.remote_addr 
        # }
        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        # if bool(r.json()['success']) is False:
        #     return "NOPE"
        # # Authorized by recaptcha.
        # else:
        #     pass
        #############################

        #return render_template('derived.html', result = result)
    #return render_template('uploaded.html', title = 'Upload')

if __name__ == '__main__':
    app.run(debug=True)

    