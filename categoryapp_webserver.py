from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from category_database_setup import Base, Category, StockItem
from flask import session as login_session
import random
import string
import json
from flask import make_response
import requests

# Imports for Login
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2



app = Flask(__name__)

# Removes the native functionality of sorting JSON results.
app.config['JSON_SORT_KEYS'] = False

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Category Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///categorylist.db')
Base.metadata.bind = engine

login_required_message = 'You need to be logged in to access this page.'


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return state


# CONNECT - Generate a current user's token and their login_session
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
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

    login_session['username'] = data.get('name', '')
    login_session['picture'] = data.get('picture', '')
    login_session['email'] = data.get('email', '')

    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()

    # Add logged in user to the DB
    # TODO: It might be more efficient to simply use the login_session variable rather than write to the DB
    #       The logged in users are removed form the Db and each created item has the creator's email address.
    #       So when a user logs in, just check the current login_session value if it matches creator value.
    # session.add(UserTable(email = data['email']))

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # DBSession = sessionmaker(bind=engine)
        # session = DBSession()
        # userToDelete = session.query(UserTable).filter_by(email=login_session['email']).one()
        # session.delete(userToDelete)
        # session.commit()

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Check the current login status
@app.route('/checkLoginState')
def checkLoginStatus():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Current user is connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response


# Add login status variable to be read in templates
@app.context_processor
def templateLoginStatus():
    access_token = login_session.get('access_token')
    if access_token is None:
        return dict(loginStatus=False)
    else:
        return dict(loginStatus=True)

# Show home page.
@app.route('/')
def showLandingPage():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()  
    categories = session.query(Category).all()
    stockItem = session.query(StockItem).order_by(desc(StockItem.id)).limit(9).all()
    return render_template('content_area.html', categories=categories, stockItem=stockItem)


# Output JSON Feed.
@app.route('/catalog/JSON')
def categoriesJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# WORKS - http://localhost:8000/catalog/Baseball/items/Bat/JSON
# Case sensitive on the stock and category names.
@app.route('/catalog/<string:category_name>/items/<string:stock_name>/JSON')
def stockItemJSON(category_name, stock_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    stock_item = session.query(StockItem).filter_by(name=stock_name).one()
    return jsonify(single_stock_item=stock_item.serialize)


# Show all categories
@app.route('/catalog/')
def showCategories():
    # Check the user is logged in to access this page
    if 'username' not in login_session:
        return login_required_message

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories=categories)


# Show items that belong to a category
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showCategoryItems(category_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    categories = session.query(Category)
    stockItems = session.query(StockItem).filter_by(category_name=category_name).all()
    currentCategory = session.query(Category).filter_by(name=category_name).one()
    stockItemsNum = len(stockItems)
    loginStatus = templateLoginStatus()
    return render_template('content_area_items.html', categories=categories, stockItems=stockItems, currentCategory=currentCategory, stockItemsNum=stockItemsNum, loginStatus=loginStatus)


# Show a category item
@app.route('/catalog/<string:category_name>/<string:stockItem_name>')
def showStockItem(category_name, stockItem_name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    stockItem = session.query(StockItem).filter_by(
        name=stockItem_name)
    currentCategory = session.query(Category).filter_by(name=category_name).one()
    loginStatus = templateLoginStatus()
    return render_template('item_content.html', stockItem=stockItem, loginStatus=loginStatus, currentCategory=currentCategory)


# Create a new stock item
@app.route('/catalog/items/new/', methods=['GET', 'POST'])
def newStockItem():
    # Check the user is logged in to access this page
    if 'username' not in login_session:
        return login_required_message

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if request.method == 'POST':
        if request.form['select_value']:
            category_name = request.form['select_value']
            category = session.query(Category).filter_by(name=category_name).one()
            newItem = StockItem(name=request.form['name'], description=request.form['description'], created_by=login_session['email'], category=category)
            session.add(newItem)
            session.commit()
            return redirect(url_for('showCategoryItems', category_name=category_name))
        else:
            return "sorry"
    else:
        categories = session.query(Category).all()
        return render_template('newStockItem.html', categories=categories)


# Edit a stock item
@app.route('/catalog/<string:stock_name>/edit', methods=['GET', 'POST'])
def editStockItem(stock_name):
    # Check the user is logged in to access this page
    if 'username' not in login_session:
        return login_required_message

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    editedItem = session.query(StockItem).filter_by(name=stock_name).one()
    category = session.query(Category).filter_by(name=editedItem.category_name).one()
    createdBy = editedItem.created_by
    if request.method == 'POST':
        if login_session['email'] == createdBy:
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            if request.form['select_value']:

                ##### REFACTOR THIS!!!!!!!! IT MIGHT NOT WORK!
                editedItem.price = request.form['select_value']
            session.add(editedItem)
            session.commit()
            return redirect(url_for('showCategoryItems', category_name=editedItem.category_name))
        else:
            return 'Sorry, only the user that created this item can edit it.'
    else:
        categories = session.query(Category).all()
        return render_template('editStockitem.html', stock_name=stock_name, stock_item=editedItem, categories=categories)


# Delete a stock item
@app.route('/catalog/<string:stock_name>/delete', methods=['GET', 'POST'])
def deleteStockItem(stock_name):
    # Check the user is logged in to access this page
    if 'username' not in login_session:
        return login_required_message

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    itemToDelete = session.query(StockItem).filter_by(name=stock_name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        print "deleted!"
        category = session.query(Category).filter_by(name=itemToDelete.category_name).one()
        return redirect(url_for('showCategoryItems', category_name=itemToDelete.category_name))
    else:
        return render_template('deleteStockItem.html', stock_name=stock_name)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

