from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, BagCompanyName, BagName, GmailUser
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///bags.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Bags Bazar"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
mas_dot = session.query(BagCompanyName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    mas_dot = session.query(BagCompanyName).all()
    maes = session.query(BagName).all()
    return render_template('login.html',
                           STATE=state, mas_dot=mas_dot, maes=maes)
    # return render_template('myhome.html', STATE=state
    # mas_dot=mas_dot,maes=maes)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = GmailUser(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(
        GmailUser).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(GmailUser).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(GmailUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


# Home
@app.route('/')
@app.route('/home')
def home():
    mas_dot = session.query(BagCompanyName).all()
    return render_template('myhome.html', mas_dot=mas_dot)


# Bag Company for admins
@app.route('/BagsBazar')
def BagsBazar():
    try:
        if login_session['username']:
            name = login_session['username']
            mas_dot = session.query(BagCompanyName).all()
            mas = session.query(BagCompanyName).all()
            maes = session.query(BagName).all()
            return render_template('myhome.html', mas_dot=mas_dot,
                                   mas=mas, maes=maes, uname=name)
    except:
        return redirect(url_for('showLogin'))


# Showing Bags based on Bag Company
@app.route('/BagsBazar/<int:maid>/showBagCompany')
def showBagCompany(maid):
    mas_dot = session.query(BagCompanyName).all()
    mas = session.query(BagCompanyName).filter_by(id=maid).one()
    maes = session.query(BagName).filter_by(bagcompanynameid=maid).all()
    try:
        if login_session['username']:
            return render_template('showBagCompany.html', mas_dot=mas_dot,
                                   mas=mas, maes=maes,
                                   uname=login_session['username'])
    except:
        return render_template('showBagCompany.html',
                               mas_dot=mas_dot, mas=mas, maes=maes)

# Add New Bag Company


@app.route('/BagsBazar/addBagCompany', methods=['POST', 'GET'])
def addBagCompany():
    if 'username' not in login_session:
        flash("Please Login First")
        return redirect(url_for('showLogin'))
    if request.method == "POST":
        company = BagCompanyName(name=request.form['name'],
                                 user_id=login_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('BagsBazar'))
    else:
        return render_template('addBagCompany.html', mas_dot=mas_dot)


# Edit Bag Company
@app.route('/BagsBazar/<int:maid>/edit', methods=['POST', 'GET'])
def editBagCompany(maid):
    if 'username' not in login_session:
        flash("You cannot edit this Bag Company.")
        return redirect(url_for('showLogin'))
    editBagCompany = session.query(BagCompanyName).filter_by(id=maid).one()
    creator = getUserInfo(editBagCompany.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Bag Company."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('BagsBazar'))
    if request.method == "POST":
        if request.form['name']:
            editBagCompany.name = request.form['name']
        session.add(editBagCompany)
        session.commit()
        flash("Bag Company Edited Successfully")
        return redirect(url_for('BagsBazar'))
    else:
        # mas_dot is global variable we can them in entire application
        return render_template('editBagCompany.html',
                               ma=editBagCompany, mas_dot=mas_dot)


# Delete Bag Company
@app.route('/BagsBazar/<int:maid>/delete', methods=['POST', 'GET'])
def deleteBagCompany(maid):
    if 'username' not in login_session:
        flash("You cannot delete this Bag Company.")
        return redirect(url_for('showLogin'))
    ma = session.query(BagCompanyName).filter_by(id=maid).one()
    creator = getUserInfo(ma.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Bag Company."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('BagsBazar'))
    if request.method == "POST":
        session.delete(ma)
        session.commit()
        flash("Bag Company Deleted Successfully")
        return redirect(url_for('BagsBazar'))
    else:
        return render_template('deleteBagCompany.html', ma=ma, mas_dot=mas_dot)


# Add New Bag Company Name Details
@app.route('/BagsBazar/addBagCompany/addBagDetails/<string:maname>/add',
           methods=['GET', 'POST'])
def addBagDetails(maname):
    if 'username' not in login_session:
        flash("Please Login first.")
        return redirect(url_for('showLogin'))
    mas = session.query(BagCompanyName).filter_by(name=maname).one()
    # See if the logged in user is not the owner of bag
    creator = getUserInfo(mas.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBagCompany', maid=mas.id))
    if request.method == 'POST':
        bagname = request.form['bagname']
        color = request.form['color']
        rating = request.form['rating']
        price = request.form['price']
        bagtype = request.form['bagtype']
        bagdetails = BagName(bagname=bagname, color=color,
                             rating=rating,
                             price=price,
                             bagtype=bagtype,
                             date=datetime.datetime.now(),
                             bagcompanynameid=mas.id,
                             gmailuser_id=login_session['user_id'])
        session.add(bagdetails)
        session.commit()
        return redirect(url_for('showBagCompany', maid=mas.id))
    else:
        return render_template('addBagDetails.html',
                               maname=mas.name, mas_dot=mas_dot)


# Edit Bag details
@app.route('/BagsBazar/<int:maid>/<string:maename>/edit',
           methods=['GET', 'POST'])
def editBag(maid, maename):
    if 'username' not in login_session:
        flash("Please Login first.")
        return redirect(url_for('showLogin'))
    ma = session.query(BagCompanyName).filter_by(id=maid).one()
    bagdetails = session.query(BagName).filter_by(bagname=maename).one()
    # See if the logged in user is not the owner of bag
    creator = getUserInfo(ma.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBagCompany', maid=ma.id))
    # POST methods
    if request.method == 'POST':
        bagdetails.bagname = request.form['bagname']
        bagdetails.color = request.form['color']
        bagdetails.rating = request.form['rating']
        bagdetails.price = request.form['price']
        bagdetails.bagtype = request.form['bagtype']
        bagdetails.date = datetime.datetime.now()
        session.add(bagdetails)
        session.commit()
        flash("Bag Edited Successfully")
        return redirect(url_for('showBagCompany', maid=maid))
    else:
        return render_template(
            'editBag.html', maid=maid, bagdetails=bagdetails, mas_dot=mas_dot)


# Delete Edit
@app.route('/BagsBazar/<int:maid>/<string:maename>/delete',
           methods=['GET', 'POST'])
def deleteBag(maid, maename):
    if 'username' not in login_session:
        flash("Please Login first.")
        return redirect(url_for('showLogin'))
    ma = session.query(BagCompanyName).filter_by(id=maid).one()
    bagdetails = session.query(BagName).filter_by(bagname=maename).one()
    # See if the logged in user is not the owner of bag
    creator = getUserInfo(ma.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBagCompany', maid=ma.id))
    if request.method == "POST":
        session.delete(bagdetails)
        session.commit()
        flash("Deleted Bag Successfully")
        return redirect(url_for('showBagCompany', maid=maid))
    else:
        return render_template('deleteBag.html',
                               maid=maid,
                               bagdetails=bagdetails,
                               mas_dot=mas_dot)

# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None, headers={
            'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Json
'''
Displays all bags in all categories
To check so ..
Browse the link .. 'localhost:7867/BagsBazar/JSON'
'''


@app.route('/BagsBazar/JSON')
def allBagJSON():
    bagcompany = session.query(BagCompanyName).all()
    category_dict = [c.serialize for c in bagcompany]
    for c in range(len(category_dict)):
        bag = [i.serialize for i in session.query(
                 BagName).filter_by(
                     bagcompanynameid=category_dict[c]["id"]).all()]
        if bag:
            category_dict[c]["bag"] = bag
    return jsonify(BagCompanyName=category_dict)

'''
Displays all the available bag company details
To check so ..
Browse the link .. 'localhost:7867/BagsBazar/BagCompany/JSON'
'''


@app.route('/BagsBazar/BagCompany/JSON')
def categoriesJSON():
    bag = session.query(BagCompanyName).all()
    return jsonify(BagCompany=[c.serialize for c in bag])

'''
Displays all the  bag  details
To check so ..
Browse the link .. 'localhost:7867/BagsBazar/bag/JSON'
'''


@app.route('/BagsBazar/bag/JSON')
def itemsJSON():
    items = session.query(BagName).all()
    return jsonify(bag=[i.serialize for i in items])

'''
Displays all the bags in  specific bagcompany
To check so ..
Browse the link .. 'localhost:7867/BagsBazar/Gear/bag/JSON'
'''


@app.route('/BagsBazar/<path:bagcompany_name>/bag/JSON')
def categoryItemsJSON(bagcompany_name):
    bagCompany = session.query(
                               BagCompanyName).filter_by(
                               name=bagcompany_name).one()
    bag = session.query(BagName).filter_by(bagcompanyname=bagCompany).all()
    return jsonify(bag=[i.serialize for i in bag])

'''
Displays available bags of specific bagcompany and required bag type
To check so ..
Browse the link .. 'localhost:7867/BagsBazar/Gear/handbag/JSON'
'''


@app.route('/BagsBazar/<path:bagcompany_name>/<path:bag_type>/JSON')
def ItemJSON(bagcompany_name, bag_type):
    bagCompany = session.query(
                               BagCompanyName).filter_by(
                               name=bagcompany_name).one()
    bagEdition = session.query(BagName).filter_by(
           bagtype=bag_type, bagcompanyname=bagCompany).one()
    return jsonify(bagEdition=[bagEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=7867)
