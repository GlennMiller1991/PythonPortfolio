import time, json

from datetime import datetime
from flask import render_template, request, escape, redirect, \
                       url_for, flash, send_from_directory, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from jinja2 import Markup

from project.forms import LoginForm, UserFileForm, SwopForm,  RegistrationForm,\
                          EditProfileForm, PostForm
from project.utils import swoper_logic, clear_instance_path
from project import app, os, db
from project.models import User, IP_field, Post
from project.file_proc import file_proc_errors, exl_file_proc, template_file_proc
from config import localhost


##################################################################
# dictionaryOfProjects
##################################################################

# Словарь требует жесткого задания адреса, так как функция url_for
# это функция контекста выполнения, и вне кнтекста сгенерировать url
# она, как оказалось, не в состоянии
dictionaryOfProjects = {'Главная': '/',
                        'PythonPortfolio Blog': '/blog',
                        'Смена раскладки': '/swoper',
                        'Статистика': '/statistics',
                        'Шаблон обработки файлов': '/file_proc_template',
                        'Обработка файла Excel': '/file_proc',
                        }

from project import errors
##################################################################


##################################################################
# before and after requests
##################################################################
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
##################################################################

@app.route('/edit_post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.author == current_user:
        form = PostForm()
        if form.validate_on_submit():
            print(form.header.data, '\n', form.post.data)
            if post.header == form.header.data:
                if post.body != form.post.data:
                    post.body = form.post.data
            else:
                post.header = form.header.data
            db.session.add(post)
            db.session.commit()
            flash('Пост отредактирован')
        else:
            form.header.data = post.header
            form.post.data = post.body
            return render_template('edit_post.html',
                                   the_title='Редактирование поста',
                                   dictionaryOfProjects=dictionaryOfProjects,
                                   form = form,
                                   )
    else:
        flash('Недостаточно прав для редактирования поста')
    return redirect(url_for('posts', id=id))

@app.route('/posts/<id>')
def posts(id):
    post = Post.query.get_or_404(id)
    body = Markup(post.body.replace('\r\n', '<br>'))
    header = post.header
    return render_template('post.html',
                           the_title='Пост',
                           dictionaryOfProjects=dictionaryOfProjects,
                           header=header,
                           body=body,
                           )

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           the_title='Редактирование профиля',
                           dictionaryOfProjects=dictionaryOfProjects,
                           form=form)
                           

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.last_seen = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash('Пользователь {} был зарегистрирован'.format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html',
                           the_title='Регистрация',
                           form=form,
                           dictionaryOfProjects=dictionaryOfProjects,
                           )

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    avatar = user.avatar()
    posts = user.posts.all()
    if current_user.username == username and current_user.priveleges:
        form = PostForm()
        if form.validate_on_submit():
            post = Post(header=form.header.data, body=form.post.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Пост опубликован')
            return redirect(url_for('main_page'))
    else:
        form = None
    return render_template('user.html',
                           the_title='Профиль',
                           user=user,
                           posts=posts,
                           dictionaryOfProjects=dictionaryOfProjects,
                           avatar=url_for('static', filename=avatar),
                           form=form,
                           )


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    return render_template('base.html',
                           dictionaryOfProjects=dictionaryOfProjects,
                           the_title='Блог',
                           )
    
@app.route('/file_proc_template', methods=['POST', 'GET'])
def file_proc_template():
    # используется та же форма, что и для функции file_proc
    # несущей полезную нагрузку, равно как и html файл для render_template
    # потому что почему бы и нет
    # просто хочу показать максимум, без возможности грузить абы что на сервер
    # хотя там вроде все и безопасно
    # ход возможной дальнейшей обработки смотрите на gitHub'е
    user_file_form = UserFileForm()
    if user_file_form.validate_on_submit():
        user_file = user_file_form.choose_file.data
        user_file_secure_name = secure_filename(user_file.filename)
        user_file.save(os.path.join(app.instance_path, user_file_secure_name))
        user_file_secure_name, status_code = template_file_proc(user_file_secure_name)
        flash(file_proc_errors[status_code])
        if not status_code:
            return redirect(url_for('file_proc', filename=user_file_secure_name))
        clear_instance_path()
    return render_template('file_proc.html',
                           the_title='Обработка файлов',
                           form=user_file_form,
                           dictionaryOfProjects=dictionaryOfProjects,
                           filename=request.args.get('filename') if request.args.get('filename') else None,
                           )

@app.route('/file_proc', methods=['POST', 'GET'])
@login_required
def file_proc():
    if current_user.priveleges:
        # на PythonAnywhere функционал этой функции несет полезную нагрузку
        # Некоторые данные для быстроты написания были жостко вшиты в код
        # Данные эти могут содержать информацию не для посторонних глаз
        # Поэтому страница, на которой используется эта функция, была защищена паролем
        user_file_form = UserFileForm()
        if user_file_form.validate_on_submit():
            user_file = user_file_form.choose_file.data
            user_file_secure_name = secure_filename(user_file.filename)
            user_file.save(os.path.join(app.instance_path, user_file_secure_name))
            user_file_secure_name, status_code = exl_file_proc(user_file_secure_name)
            flash(file_proc_errors[status_code])
            if not status_code:
                return redirect(url_for('file_proc', filename=user_file_secure_name))
        return render_template('file_proc.html',
                               the_title='Обработка файлов',
                               form=user_file_form,
                               dictionaryOfProjects=dictionaryOfProjects,
                               filename=request.args.get('filename') if request.args.get('filename') else None,
                               )
    else:
        flash('В доступе отказано. Не хватает прав')
        return redirect(url_for('main_page'))

@app.route('/index')
@app.route('/default')
@app.route('/', methods=['POST', 'GET'])
def main_page() -> 'html':
    return render_template( 'main.html', 
                            the_title='PythonPortfolio', 
                            dictionaryOfProjects=dictionaryOfProjects,
                            )

@app.route('/swoper', methods=['POST', 'GET'])
def swoper_page() -> 'html':
    text_to_swop = SwopForm()
    if text_to_swop.validate_on_submit():
        language = int(text_to_swop.language_choice.data)
        text = text_to_swop.text_to_swop.data
        swoper_result = swoper_logic(text, language)
        return render_template('swoper_results.html',
                               dictionaryOfProjects=dictionaryOfProjects,
                               the_title='Результат смены раскладки',
                               form=text_to_swop,
                               language=language,
                               swoper_result=swoper_result,
                               )
    return render_template('swoper.html',
                            dictionaryOfProjects=dictionaryOfProjects,
                            the_title='change the keyboard layout',
                            form = text_to_swop,
                            )

@app.route('/statistics')
def get_stat() -> 'html':
    address = request.remote_addr if localhost else request.headers['X-Real-IP']
    browser = request.user_agent.string
    entry = IP_field.query.filter_by(address=address).first()
    if not entry:
        entry = IP_field(address=address)
    entry.last_visit = datetime.utcnow()
    entry.browser = browser
    db.session.add(entry)
    db.session.commit()
    return render_template('statistics.html',
                           the_title='Статистика сайта',
                           dictionaryOfProjects=dictionaryOfProjects,
                           uniqueIP=db.session.query(IP_field).count(),
                           table=IP_field,
                           )

@app.route('/login', methods=['GET', 'POST'])
def login() -> 'html':
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Некорректные логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main_page')
        return redirect(next_page)
    return render_template('login.html',
                           the_title='Вход',
                           form=form,
                           dictionaryOfProjects=dictionaryOfProjects,
                           )
   
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))

###################################################################
# Blueprints
###################################################################


# File_proc blueprint
###################################################################
file_proc_bp = Blueprint('file_proc_bp', __name__)

# для поддеражания директории чистой реализован декоратор шаблонов
# after_request.
# В случае, если по этой ссылке не будет ни одного перехода,
# то директория не будет переполнена - в худшем случае в папке будет лишь один
# или два файла c жестко фиксированным именем (в зависимости от реализации
# самой функции обработки - я пока не определился как удобнее),
# поэтому каждый раз они будут перезаписываться.
@file_proc_bp.after_request
def after_request_file_proc(response):
    clear_instance_path()
    return response
    

@file_proc_bp.route('/download')
@login_required
def download():
    if current_user.priveleges:
        filename = secure_filename(request.args.get('filename'))
        return send_from_directory(app.instance_path, filename, as_attachment=True)
    else:
        flash('В доступе отказано. Не хватает прав')
        return redirect(url_for('main_page'))
