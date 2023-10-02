from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class glist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(200), nullable=False) #group name
    desc = db.Column(db.String(500), nullable=True) #description
    contact = db.Column(db.String(500), nullable=False) #group link
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self): #returns a string when we create a new element 
        return '<Group %r>' % self.i
with app.app_context():
    db.create_all()
@app.route('/')
def landing():
    return render_template('landing.html')
@app.route('/agree')
def agree():
    return render_template('agree.html')
@app.route('/index',methods=['POST','GET'])
def index():
    if request.method=='POST':
        gname=request.form['gname']
        desc=request.form['desc']
        contact=request.form['contact']
        new_grp=glist(groupname=gname,desc=desc,contact=contact)
        try:
            db.session.add(new_grp)
            db.session.commit()
            return redirect('/index')
        except:
            return 'There was an issue adding your group'
        
    else:
        groupnames = glist.query.order_by(glist.date_created).all()
        return render_template('index.html',groupnames=groupnames)
@app.route('/delete/<int:id>')
def delete(id):
    grp_to_delete=glist.query.get_or_404(id)
    try:
        db.session.delete(grp_to_delete)
        db.session.commit()
        return redirect('/index')
    except:
        return 'There was a problem deleting  the group'  

if __name__ == "__main__":
    app.run(debug=True)