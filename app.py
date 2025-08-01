import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint


app = Flask(__name__)

load_dotenv()

username = os.getenv('MYSQL_USERNAME')
password = os.getenv('MYSQL_PASSWORD')
host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DATABASE')

# ✅ MySQL connection string (using PyMySQL as the driver)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Models
# ---------------------

class Publisher(db.Model):
    __tablename__ = 'publishers'
    pubID = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(30))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(30))

class Subject(db.Model):
    __tablename__ = 'subjects'
    subID = db.Column(db.String(5), primary_key=True)
    sName = db.Column(db.String(30))

class Author(db.Model):
    __tablename__ = 'authors'
    auID = db.Column(db.Integer, primary_key=True)
    aName = db.Column(db.String(30))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(30))

class Title(db.Model):
    __tablename__ = 'titles'
    titleID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    pubID = db.Column(db.Integer)
    subID = db.Column(db.String(5))
    pubDate = db.Column(db.Date)
    cover = db.Column(db.String(10))
    price = db.Column(db.Integer)

class TitleAuthor(db.Model):
    __tablename__ = 'titleauthors'
    titleID = db.Column(db.Integer, primary_key=True)
    auID = db.Column(db.Integer, primary_key=True)
    importance = db.Column(db.Integer)

    __table_args__ = (
        PrimaryKeyConstraint('titleID', 'auID'),
    )

# ---------------------
# Routes
# ---------------------

@app.route('/')
def index():
    publishers = Publisher.query.all()
    subjects = Subject.query.all()
    return render_template('index.html', publishers=publishers, subjects=subjects)


@app.route('/publishers', methods=['GET'])
def get_publishers():
    publishers = Publisher.query.all()
    return jsonify([
        {
            'pubID': p.pubID,
            'pname': p.pname,
            'email': p.email,
            'phone': p.phone
        } for p in publishers
    ])

@app.route('/publishers', methods=['POST'])
def add_publisher():
    data = request.get_json()

    pubID = data.get('pubID')
    pname = data.get('pname')
    email = data.get('email')
    phone = data.get('phone')

    if not pubID or not pname or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_pub = Publisher(pubID=pubID, pname=pname, email=email, phone=phone)
        db.session.add(new_pub)
        db.session.commit()
        return jsonify({'message': 'Publisher added'}), 201
    except Exception as e:
        print("❌ Error adding publisher:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/publishers/<int:pubID>', methods=['DELETE'])
def delete_publisher(pubID):
    pub = Publisher.query.get_or_404(pubID)
    db.session.delete(pub)
    db.session.commit()
    return jsonify({'message': 'Publisher deleted'})

@app.route('/publishers/<int:pubID>', methods=['PATCH'])
def update_publisher(pubID):
    publisher = Publisher.query.get_or_404(pubID)
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')

    if field not in ['pubID', 'pname', 'email', 'phone']:
        return jsonify({'error': 'Invalid field'}), 400

    setattr(publisher, field, value)
    db.session.commit()
    return jsonify({'message': 'Publisher updated'})


@app.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([
        {
            'subID': s.subID,
            'sName': s.sName
        } for s in subjects
    ])

@app.route('/subjects', methods=['POST'])
def add_subject():
    data = request.get_json()

    subID = data.get('subID')
    sName = data.get('sName')

    if not subID or not sName:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_sub = Subject(subID=subID, sName=sName)
        db.session.add(new_sub)
        db.session.commit()
        return jsonify({'message': 'Subject added'}), 201
    except Exception as e:
        print("❌ Error adding subject:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/subjects/<string:subID>', methods=['DELETE'])
def delete_subject(subID):
    subject = Subject.query.get_or_404(subID)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted'})

@app.route('/subjects/<string:subID>', methods=['PATCH'])
def update_subject(subID):
    subject = Subject.query.get_or_404(subID)
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')

    if field not in ['subID', 'sName']:
        return jsonify({'error': 'Invalid field'}), 400

    setattr(subject, field, value)
    db.session.commit()
    return jsonify({'message': 'Subject updated'})

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([
        {
            'auID': a.auID,
            'aName': a.aName,
            'email': a.email,
            'phone': a.phone
        } for a in authors
    ])

@app.route('/authors', methods=['POST'])
def add_author():
    data = request.get_json()

    auID = data.get('auID')
    aName = data.get('aName')
    email = data.get('email')
    phone = data.get('phone')

    if not auID or not aName or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_author = Author(auID=auID, aName=aName, email=email, phone=phone)
        db.session.add(new_author)
        db.session.commit()
        return jsonify({'message': 'Author added'}), 201
    except Exception as e:
        print("❌ Error adding author:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/authors/<int:auID>', methods=['DELETE'])
def delete_author(auID):
    author = Author.query.get_or_404(auID)
    db.session.delete(author)
    db.session.commit()
    return jsonify({'message': 'Author deleted'})

@app.route('/authors/<int:auID>', methods=['PATCH'])
def update_author(auID):
    author = Author.query.get_or_404(auID)
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')

    if field not in ['auID', 'aName', 'email', 'phone']:
        return jsonify({'error': 'Invalid field'}), 400

    setattr(author, field, value)
    db.session.commit()
    return jsonify({'message': 'Author updated'})

@app.route('/titles', methods=['GET'])
def get_titles():
    titles = Title.query.all()
    return jsonify([
        {
            'titleID': t.titleID,
            'title': t.title,
            'pubID': t.pubID,
            'subID': t.subID,
            'pubDate': t.pubDate.isoformat() if t.pubDate else None,
            'cover': t.cover,
            'price': t.price
        } for t in titles
    ])

@app.route('/titles', methods=['POST'])
def add_title():
    data = request.get_json()

    titleID = data.get('titleID')
    title = data.get('title')
    pubID = data.get('pubID')
    subID = data.get('subID')
    pubDate = data.get('pubDate')
    cover = data.get('cover')
    price = data.get('price')

    if not titleID or not title or not pubID or not subID:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_title = Title(
            titleID=titleID, title=title, pubID=pubID, subID=subID,
            pubDate=pubDate, cover=cover, price=price
        )
        db.session.add(new_title)
        db.session.commit()
        return jsonify({'message': 'Title added'}), 201
    except Exception as e:
        print("❌ Error adding title:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/titles/<int:titleID>', methods=['DELETE'])
def delete_title(titleID):
    title = Title.query.get_or_404(titleID)
    db.session.delete(title)
    db.session.commit()
    return jsonify({'message': 'Title deleted'})

@app.route('/titles/<int:titleID>', methods=['PATCH'])
def update_title(titleID):
    title = Title.query.get_or_404(titleID)
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')

    if field not in ['titleID', 'title', 'pubID', 'subID', 'pubDate', 'cover', 'price']:
        return jsonify({'error': 'Invalid field'}), 400

    setattr(title, field, value)
    db.session.commit()
    return jsonify({'message': 'Title updated'})

@app.route('/titleauthors', methods=['GET'])
def get_title_authors():
    title_authors = TitleAuthor.query.all()
    return jsonify([
        {
            'titleID': ta.titleID,
            'auID': ta.auID,
            'importance': ta.importance
        } for ta in title_authors
    ])

@app.route('/titleauthors', methods=['POST'])
def add_title_author():
    data = request.get_json()

    titleID = data.get('titleID')
    auID = data.get('auID')
    importance = data.get('importance')

    if not titleID or not auID:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_title_author = TitleAuthor(titleID=titleID, auID=auID, importance=importance)
        db.session.add(new_title_author)
        db.session.commit()
        return jsonify({'message': 'TitleAuthor added'}), 201
    except Exception as e:
        print("❌ Error adding title author:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/titleauthors/<int:titleID>/<int:auID>', methods=['DELETE'])
def delete_title_author(titleID, auID):
    title_author = TitleAuthor.query.filter_by(titleID=titleID, auID=auID).first_or_404()
    db.session.delete(title_author)
    db.session.commit()
    return jsonify({'message': 'TitleAuthor deleted'})

@app.route('/titleauthors/<int:titleID>/<int:auID>', methods=['PATCH'])
def update_title_author(titleID, auID):
    title_author = TitleAuthor.query.filter_by(titleID=titleID, auID=auID).first_or_404()
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')

    if field not in ['titleID', 'auID', 'importance']:
        return jsonify({'error': 'Invalid field'}), 400
    setattr(title_author, field, value)
    db.session.commit()
    return jsonify({'message': 'TitleAuthor updated'})


# Debug Info

with app.app_context():
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)


if __name__ == '__main__':
    app.run(debug=True)
