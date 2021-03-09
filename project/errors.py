from flask import render_template

from project import app, db
from project.routes import dictionaryOfProjects

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html',
                           the_title='404',
                           dictionaryOfProjects=dictionaryOfProjects), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html',
                           the_title='Обработка файлов',
                           dictionaryOfProjects=dictionaryOfProjects), 500
