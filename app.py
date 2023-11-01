from flask import Flask, request, session, redirect, url_for, render_template, jsonify, sessions
# import expense_tracker.models as models
from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta
from models import add_user, add_data, user_exists, get_user_data,username_check

app = Flask(__name__)

app.secret_key = 'dw@G*YmrDat'
app.permanent_session_lifetime = timedelta(minutes=10)

serializer = URLSafeTimedSerializer('dw@G*YmrDat')

def generate_token(username):
    data = {'user':username}
    return serializer.dumps(data) 

def decode_token(token):
    try:
        data = serializer.loads(token,max_age=1000)
        return data
    except:
        return None


@app.route('/',methods=['GET','POST'])
def main_page():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if user_exists(username,password):
            session['token'] = generate_token(username)
            session.permanent = True
            user_data = get_user_data(username)
            return render_template('index.html',existing_data=user_data)
    elif 'token' in session:
        token_data = decode_token(session['token'])
        username = token_data['user']
        user_data = get_user_data(username)
    # return jsonify(user_data)
        return render_template('index.html',existing_data = user_data)
    return render_template('login.html')
    # with open('user_data.json','r')as json_file:
        # existing_data = json.load(json_file)
    # print(existing_data)

    # return "watch your terminal !!!"

@app.route('/login')
def login_page():
    return redirect('/')

@app.route('/expense',methods=['GET','POST'])
def expense_creator():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        description = request.form['description']
        payment_type = request.form['paymentType']
        token_data = decode_token(session['token'])
        username = token_data['user']
        # json_format = {"Title":title,"Amount":amount,'Description':description,'payment_type':payment_type}
        # write_data(json_format)
        add_data(username,title,amount,description,payment_type)
        return redirect('/')
    return render_template('expense_adder.html')

@app.route('/sign_up',methods=['GET','POST'])
def register_user():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username_check(username):
            return "username has already been used !!!"
        add_user(username,email,password)
        session['token'] = generate_token(username)
        session.permanent = True
        return redirect('/')
    return render_template('sign_up.html')#add the functionality to register the user in the database...

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")