from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', '__name__')

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method=='POST':
        note = request.form.get('note')

        if len(note)<1:
            flash('Note is too short', category='error')
        else:
            try:
                new_note = Note(data=note, user_id = current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added successfully.', category='success')
            except Exception as e:
                flash('Note could not be added, please try again.', category='error')
                print(str(e))
                db.session.rollback()
        
    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(int(noteId))
    if note:
        if note.user_id==current_user.id:
            try:
                db.session.delete(note)
                db.session.commit()
            except Exception as e:
                print('Exception : '+str(e))
                db.session.rollback()
        return jsonify({})
    
        