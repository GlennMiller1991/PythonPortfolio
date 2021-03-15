from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from project.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UserFileForm(FlaskForm):
    submit_file = SubmitField('Лови!')
    choose_file = FileField('Выберите файл',
                         validators=[FileRequired(),
                                     FileAllowed(['xlsx'],
                                                 '.xlsx files only!'),
                                     ]
                         )

class SwopForm(FlaskForm):
    submit_text = SubmitField('Сменить раскладку')
    text_to_swop = StringField('Текст', validators=[DataRequired()])
    language_choice = SelectField('Язык ввода', choices=[('0', 'русский'),
                                                         ('1', 'английский')])

class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя уже используется')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Эта почта уже используется')

class EditProfileForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Выберите другое имя')

class PostForm(FlaskForm):
    header = StringField('Заголовок? 100 символов',
                         validators=[DataRequired(),
                                     Length(min=1, max=100)])
    post = TextAreaField('Новый пост? 100000 символов',
                         validators=[DataRequired(),
                                     Length(min=1, max=100000)])
    submit = SubmitField('Опубликовать')
    paragraph = SubmitField('paragraph')
    bold = SubmitField('bold')
    italic = SubmitField('italic')
    strike = SubmitField('strike')
    details = SubmitField('details')
    code = SubmitField('code')
    pre = SubmitField('pre')
