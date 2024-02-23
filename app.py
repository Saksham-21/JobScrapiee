from flask import Flask, render_template, request,url_for,session,redirect,Response,send_file
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import os
import re
import csv
from scrape import fetch_job_data,save_to_csv
app = Flask(__name__)
load_dotenv()

app.secret_key='abcxyz'



# private_key = os.getenv("PRIVATE_KEY")

# if private_key is not None:
#     private_key = private_key.replace(r'\n', '\n')

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
})



#cred=credentials.Certificate("/firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        users_ref = db.collection('user')
        query = users_ref.where('email', '==', email).where('password', '==', password).limit(1).stream()
        user = next(query, None)
        if user:
            session['loggedin'] = True
            session['name'] = user.to_dict()['name']
            session['email'] = user.to_dict()['email']
            return redirect(url_for('index'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('Login.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']

        users_ref = db.collection('user')
        query = users_ref.where('email', '==', email).limit(1).stream()
        existing_user = next(query, None)

        if existing_user:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            users_ref.add({
                'name': userName,
                'email': email,
                'password': password
            })
            message = 'You have successfully registered!'
            return redirect(url_for('login'))

    return render_template('Register.html', message=message)



@app.route('/display_result',methods=['POST'])
def display_result():
    global jobs
    job_title=request.form['job-title']
    location=request.form['job-location']
    jobs=fetch_job_data(job_title,location)
    return render_template('featuredobs.html',job_disp=jobs)



@app.route('/download_csv')
def download_csv():
    save_to_csv(jobs)
    return send_file('job_data.csv', as_attachment=True)



@app.route('/index')
def index():
    user_name=session.get('name')
    print(f"User name in session: {user_name}")
    return render_template('index.html',user=user_name)



@app.route('/joblist')
def joblist():
    return render_template('job-listings.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/featuredjobs')
def featuredjobs():
    return render_template('featuredobs.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')       


# if __name__=='__main__':
#     app.run(debug=True)
