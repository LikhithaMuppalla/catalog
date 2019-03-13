from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from john_setup import Base, BagCompanyName, BagName, emailUser
from flask import session as devena_joice
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
APPLICATION_NAME = "Bag_store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
genesis = session.query(BagCompanyName).all()

# login code


@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    devena_joice['state'] = state
    # return "The current session state is %s" % devena_joice['state']
    genesis = session.query(BagCompanyName).all()
    adoneram_jadson = session.query(BagName).all()
    return render_template('login.html',
                           STATE=state, genesis=genesis,
                           adoneram_jadson=adoneram_jadson)
    # return render_template('myhome.html', STATE=state
    # genesis=genesis,adoneram_jadson=adoneram_jadson)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != devena_joice['state']:
        ephessians = make_response(json.dumps('Invalid state parameter.'), 401)
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        zairus = flow_from_clientsecrets('client_secrets.json', scope='')
        zairus.redirect_uri = 'postmessage'
        credentials = zairus.step2_exchange(code)
    except FlowExchangeError:
        ephessians = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians

    # Check if that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    gennesara_t = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if gennesara_t.get('error') is not None:
        ephessians = make_response(json.dumps(gennesara_t.get('error')), 500)
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if gennesara_t['user_id'] != gplus_id:
        ephessians = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians

    # Verify that the access token is valid for this app.
    if gennesara_t['issued_to'] != CLIENT_ID:
        ephessians = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians

    stored_access_token = devena_joice.get('access_token')
    stored_gplus_id = devena_joice.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        ephessians = make_response(json.dumps(
            'Current user already connected.'), 200)
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians

    # Store the access token in the session for later use.
    devena_joice['access_token'] = credentials.access_token
    devena_joice['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    devena_joice['username'] = data['name']
    devena_joice['picture'] = data['picture']
    devena_joice['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(devena_joice['email'])
    if not user_id:
        user_id = createUser(devena_joice)
    devena_joice['user_id'] = user_id

    anniejoice = ''
    anniejoice += '<h1>Welcome, '
    anniejoice += devena_joice['username']
    anniejoice += '!</h1>'
    anniejoice += '<img src="'
    anniejoice += devena_joice['picture']
    anniejoice += ' "style ="width: 300px; height:300px; border-radius:150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % devena_joice['username'])
    print ("done!")
    return anniejoice


# User Helper Functions


def createUser(devena_joice):
    calab = emailUser(name=devena_joice['username'], email=devena_joice[
                   'email'])
    session.add(calab)
    session.commit()
    user = session.query(emailUser).filter_by(
        email=devena_joice['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(emailUser).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(emailUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their devena_joice


# Home


@app.route('/')
@app.route('/home')
def home():
    genesis = session.query(BagCompanyName).all()
    return render_template('myhome.html', genesis=genesis)


# Bag Category for admins


@app.route('/Bag')
def Bag():
    '''shows home page with different bags'''
    try:
        if devena_joice['username']:
            name = devena_joice['username']
            genesis = session.query(BagCompanyName).all()
            solman = session.query(BagCompanyName).all()
            adoneram_jadson = session.query(BagName).all()
            return render_template(
                'myhome.html', genesis=genesis,
                solman=solman, adoneram_jadson=adoneram_jadson,
                uname=name)
    except:
        return redirect(url_for('showLogin'))


# Showing bags based on bag category
@app.route('/Bag/<int:saintfransis>/allBag')
def showBags(saintfransis):
    '''shows the details of bags'''
    genesis = session.query(BagCompanyName).all()
    solman = session.query(BagCompanyName).filter_by(id=saintfransis).one()
    adoneram_jadson = session.query(BagName).filter_by(
        bagcompanynameid=saintfransis).all()
    try:
        if devena_joice['username']:
            return render_template('showBags.html', genesis=genesis,
                                   solman=solman,
                                   adoneram_jadson=adoneram_jadson,
                                   uname=devena_joice['username'])
    except:
        return render_template('showBags.html',
                               genesis=genesis, solman=solman,
                               adoneram_jadson=adoneram_jadson)


# Add New Bag


@app.route('/Bag/addBagCompany', methods=['POST', 'GET'])
def addBagCompany():
    '''adding a new bag company'''
    if 'username' not in devena_joice:
        return redirect("/login")
    if request.method == 'POST':
        Bag = BagCompanyName(
            name=request.form['itemname'],
            user_id=devena_joice['user_id'])
        session.add(Bag)
        session.commit()
        return redirect(url_for('Bag'))
    else:
        return render_template('addBagCompany.html', genesis=genesis)


# Edit Bag Category


@app.route('/Bag/<int:saintfransis>/edit', methods=['POST', 'GET'])
def editBagCatagery(saintfransis):
    '''to edit the bag catagery name'''
    editBag = session.query(BagCompanyName).filter_by(id=saintfransis).one()
    creator = getUserInfo(editBag.user_id)
    user = getUserInfo(devena_joice['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != devena_joice['user_id']:
        flash("You cannot edit this Bag Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Bag'))
    if request.method == "POST":
        if request.form['name']:
            editBag.name = request.form['name']
        session.add(editBag)
        session.commit()
        flash("Bag name  Edited Successfully")
        return redirect(url_for('Bag'))
    else:
        # genesis is global variable we can them in entire application
        return render_template('editBagCatagery.html',
                               tb=editBag, genesis=genesis)


# Delete Bag Category


@app.route('/Bag/<int:saintfransis>/delete', methods=['POST', 'GET'])
def deleteBagCatagery(saintfransis):
    '''To delete the bag catagery name'''
    daniel = session.query(BagCompanyName).filter_by(id=saintfransis).one()
    creator = getUserInfo(daniel.user_id)
    user = getUserInfo(devena_joice['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != devena_joice['user_id']:
        flash("You cannot Delete this Bag."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Bag'))
    if request.method == "POST":
        session.delete(daniel)
        session.commit()
        flash("Bag name Deleted Successfully")
        return redirect(url_for('Bag'))
    else:
        return render_template(
            'deleteBagCatagery.html', daniel=daniel, genesis=genesis)


# add new item details


@app.route('/Bag/addBagCompany/addBagdetails/<string:emicarmichel>/add',
           methods=['GET', 'POST'])
def addBagdetails(emicarmichel):
    '''to add the bag details'''
    solman = session.query(BagCompanyName).filter_by(name=emicarmichel).one()
    # See if the logged in user is not the owner of bag
    creator = getUserInfo(solman.user_id)
    user = getUserInfo(devena_joice['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != devena_joice['user_id']:
        flash("You can't add new bag"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBags', saintfransis=solman.id))
    if request.method == 'POST':
        itemname = request.form['itemname']
        description = request.form['description']
        price = request.form['price']
        rating = request.form['rating']
        itemdetails = BagName(
            itemname=itemname, description=description,
            price=price, rating=rating, bagcompanynameid=solman.id,
            date=datetime.datetime.now(),
            emailuser_id=devena_joice['user_id'])
        session.add(itemdetails)
        session.commit()
        return redirect(url_for('showBags', saintfransis=solman.id))
    else:
        return render_template('addBagdetails.html',
                               emicarmichel=solman.name, genesis=genesis)


# Edit Bag details


@app.route('/Bag/<int:saintfransis>/<string:francis>/edit',
           methods=['GET', 'POST'])
def edititem(saintfransis, francis):
    tb = session.query(BagCompanyName).filter_by(id=saintfransis).one()
    itemdetails = session.query(BagName).filter_by(itemname=francis).one()
    # See if the logged in user is not the owner of bag
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(devena_joice['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != devena_joice['user_id']:
        flash("You can't edit this bag"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Bag', saintfransis=tb.id))
    # POST methods
    if request.method == 'POST':
        itemdetails.itemname = request.form['itemname']
        itemdetails.description = request.form['description']
        itemdetails.price = request.form['price']
        itemdetails.rating = request.form['rating']
        session.add(itemdetails)
        session.commit()
        flash("item Edited Successfully")
        return redirect(url_for('showBags', saintfransis=saintfransis))
    else:
        return render_template(
            'edititem.html', saintfransis=saintfransis,
            itemdetails=itemdetails, genesis=genesis)

#####
# Delete Bag item


@app.route('/Bag/<int:saintfransis>/<string:francis>/delete',
           methods=['GET', 'POST'])
def deleteitem(saintfransis, francis):
    tb = session.query(BagCompanyName).filter_by(id=saintfransis).one()
    itemdetails = session.query(BagName).filter_by(itemname=francis).one()
    # See if the logged in user is not the owner of bag
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(devena_joice['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != devena_joice['user_id']:
        flash("You can't delete this bag"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Bag', saintfransis=tb.id))
    if request.method == "POST":
        session.delete(itemdetails)
        session.commit()
        flash("Deleted item Successfully")
        return redirect(url_for('Bag', saintfransis=saintfransis))
    else:
        return render_template('deleteitem.html',
                               saintfransis=saintfransis,
                               itemdetails=itemdetails, genesis=genesis)


# Logout from current user


@app.route('/logout')
def logout():
    access_token = devena_joice['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (devena_joice['username'])
    if access_token is None:
        print ('Access Token is None')
        ephessians = make_response(
            json.dumps('Current user not connected....'), 401)
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians
    access_token = devena_joice['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    gennesara_t = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'}
                  )[0]

    print (gennesara_t['status'])
    if gennesara_t['status'] == '200':
        del devena_joice['access_token']
        del devena_joice['gplus_id']
        del devena_joice['username']
        del devena_joice['email']
        del devena_joice['picture']
        ephessians = make_response(
            json.dumps('Successfully disconnected user..'), 200)
        ephessians.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return ephessians
    else:
        ephessians = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        ephessians.headers['Content-Type'] = 'application/json'
        return ephessians


# Json


@app.route('/Bag/JSON')
def allitemJSON():
    bagcatagories = session.query(BagCompanyName).all()
    category_dict = [c.serialize for c in bagcatagories]
    for c in range(len(category_dict)):
        items = [i.serialize for i in session.query(
                 BagName).filter_by(
                     bagcompanynameid=category_dict[c]["id"]).all()]
        if items:
            category_dict[c]["item"] = items
    return jsonify(BagCompanyName=category_dict)


@app.route('/Bag/bagcatagories/JSON')
def categoriesJSON():
    items = session.query(BagCompanyName).all()
    return jsonify(bagcatagories=[c.serialize for c in items])


@app.route('/Bag/items/JSON')
def itemsJSON():
    items = session.query(BagName).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/Bag/<path:bag_name>/items/JSON')
def categoryItemsJSON(bag_name):
    bagcatagory = session.query(BagCompanyName).filter_by(
        name=bag_name).one()
    items = session.query(BagName).filter_by(bagcompanyname=bagcatagory).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/Bag/<path:item_name>/<path:edition_name>/JSON')
def ItemJSON(item_name, edition_name):
    bagcatagory = session.query(BagCompanyName).filter_by(name=item_name).one()
    item = session.query(BagName).filter_by(
           itemname=edition_name, bagcompanyname=bagcatagory).one()
    return jsonify(item=[item.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=9000)
