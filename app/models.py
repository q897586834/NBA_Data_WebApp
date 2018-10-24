# -*- coding: utf-8 -*-

from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Roles(db.Model):
    '''

        用户的角色类，
        不同的角色对应于不同的权限

    '''
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    # 对于一个Role实例，users属性返回与角色关联的用户组成的列表
    # backref在Users中定义一个role属性，可替代role_id访问Role模型
    users = db.relationship('Users', backref='role', lazy='dynamic')
    default_user = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Users(db.Model):
    '''

        用户类

    '''
    __tablename__ = 'Users'     # 对应表的名称
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    pwd = db.Column(db.String(32), nullable=False)
    # 建立外键关系
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        # super(Users, self).__init__(**kwargs)
        if self.role is None:
            self.role = Roles.query.filter_by(default_user=True).first()
        # self.role_id = 1

    def to_json(self):
        return '''{
            "id": self.id,
            "name": self.name,
            "pwd": self.pwd,
            "role_id": self.role_id,
            "confirmed": self.confirmed
        }'''

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        '''

            真实用户return Flase

        '''
        return False

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'confirm': self.id}).decode('utf-8')

    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True

    # def generate_reset_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'reset': self.id}).decode('utf-8')

    # @staticmethod
    # def reset_password(token, new_password):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     user = User.query.get(data.get('reset'))
    #     if user is None:
    #         return False
    #     user.password = new_password
    #     db.session.add(user)
    #     return True

    # def generate_email_change_token(self, new_email, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps(
    #         {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    # def change_email(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     if data.get('change_email') != self.id:
    #         return False
    #     new_email = data.get('new_email')
    #     if new_email is None:
    #         return False
    #     if self.query.filter_by(email=new_email).first() is not None:
    #         return False
    #     self.email = new_email
    #     db.session.add(self)
    #     return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def is_authenticated(self):
        # 未登录时默认为AnonymousUser，返回False
        return False

login_manager.anonymous_user = AnonymousUser



#
#
#    8张生产数据表对应的8个类
#
#

class Player(db.Model):
    '''

        球员类

    '''
    __tablename__ = 'player_info'
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_name = db.Column(db.String(30), nullable=False)
    year_start = db.Column(db.Integer)
    year_end = db.Column(db.Integer)
    position = db.Column(db.String(10))
    height = db.Column(db.String(10))
    weight = db.Column(db.Float)
    birth_year = db.Column(db.Integer)
    college = db.Column(db.String(64))

    player_data = db.relationship('Player_Data', backref='player', lazy='dynamic')
    # 表示relationship需要to_json吗？？
    player_contract = db.relationship('Player_Contract', backref='player', lazy='dynamic')

    def __init__(self, **kwargs):
        pass

    def to_json(self):
        return {
            'player_id': self.player_id,
            'player_name': self.player_name,
            'year_start': self.year_start,
            'year_end': self.year_end,
            'position': self.position,
            'height': self.height,
            'weight': self.weight,
            'birth_year': self.birth_year,
            'college': self.college
        }

class Player_Data(db.Model):
    '''

        球员数据类

    '''
    __tablename__ = 'player_data'
    player_id = db.Column(db.Integer, db.ForeignKey('player_info.player_id'), primary_key=True)
    season = db.Column(db.String(10), primary_key=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team_info.team_id'), primary_key=True)
    attri_value = db.Column(db.String(20))
    attri_id = db.Column(db.Integer, db.ForeignKey('attribute_type.attri_id'), primary_key=True)

    def __init__(self, player_id, season, team_id, attri_value, attri_id, **kwargs):
        self.player_id = player_id
        self.season = season
        self.team_id = team_id
        self.attri_value = attri_value
        self.attri_id = attri_id

    def to_json(self):
        return {
            'player_id': self.player_id,
            'season': self.season,
            'team_id': self.team_id,
            'attri_value': self.attri_value,
            'attri_id': self.attri_id
        }


class Team(db.Model):
    '''

        球队类

    '''
    __tablename__ = 'team_info'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(5), nullable=False)
    team_city = db.Column(db.String(20))
    team_year = db.Column(db.Integer)

    player_data = db.relationship('Player_Data', backref='team', lazy='dynamic')
    player_contract = db.relationship('Player_Contract', backref='team', lazy='dynamic')
    team_data = db.relationship('Team_Data', backref='team', lazy='dynamic')

    def __init__(self, **kwargs):
        pass

    def to_json(self):
        return {
            'team_id': self.team_id,
            'team_name': self.team_name,
            'team_city': self.team_city,
            'team_year': self.team_year
        }

class Team_Data(db.Model):
    '''

        球队数据类

    '''
    __tablename__ = 'team_data'
    team_id = db.Column(db.Integer, db.ForeignKey('team_info.team_id'), primary_key=True)
    season = db.Column(db.String(10), primary_key=True, nullable=False)
    attri_value = db.Column(db.String(20))
    attri_id = db.Column(db.Integer, db.ForeignKey('attribute_type.attri_id'), primary_key=True)

    def __init__(self, team_id, season, attri_value, attri_id, **kwargs):
        self.team_id = team_id
        self.season = season
        self.attri_value = attri_value
        self.attri_id = attri_id

    def to_json(self):
        pass

class Coach(db.Model):
    '''

        教练类

    '''
    __tablename__ = 'coach_info'
    coach_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coach_name = db.Column(db.String(30), nullable=False)
    coach_data = db.relationship('Coach_Data', backref='coach', lazy='dynamic')

    def __init__(self, **kwargs):
        pass

    def to_json(self):
        return {
            'coach_id': self.coach_id,
            'coach_name': self.coach_name
        }

class Coach_Data(db.Model):
    '''

        教练数据类

    '''
    __tablename__ = 'coach_data'
    coach_id = db.Column(db.Integer, db.ForeignKey('coach_info.coach_id'), primary_key=True)
    season = db.Column(db.String(10), primary_key=True, nullable=False)
    win = db.Column(db.Integer)
    loss = db.Column(db.Integer)

    def __init__(self, coach_id, season, win, loss, **kwargs):
        self.coach_id = coach_id
        self.season = season
        self.win = win
        self.loss = loss

class Player_Contract(db.Model):
    '''

        球员合同类

    '''
    __tablename__ = 'player_contract'
    player_id = db.Column(db.Integer, db.ForeignKey('player_info.player_id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team_info.team_id'), primary_key=True)
    season = db.Column(db.String(10), primary_key=True, nullable=False)
    salary = db.Column(db.Integer)

    def __init__(self, player_id, team_id, season, salary, **kwargs):
        self.player_id = player_id
        self.team_id = team_id
        self.season = season
        self.salary = salary

    def to_json(self):
        pass

class Attribute_Type(db.Model):
    '''

        数据类型类

    '''
    __tablename__ = 'attribute_type'
    attri_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attri_name = db.Column(db.String(20), nullable=False)

    # player_data = db.relationship('Player_Data', backref='attribute_type', lazy='dynamic')
    team_data = db.relationship('Team_Data', backref='attribute_type', lazy='dynamic')

    def __init__(self, attri_id, attri_name, **kwargs):
        self.attri_id = attri_id
        self.attri_name = attri_name

    def to_json(self):
        return {
            'attri_id': self.attri_id,
            'attri_name': self.attri_name
        }




# 加载用户的回调函数
# 返回user_id对应的user对象
@login_manager.user_loader
def load_user(user_id):
    # from ..models import Users
    return Users.query.get(int(user_id))
