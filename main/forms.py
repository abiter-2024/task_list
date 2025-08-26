# 导入Flask-WTF扩展用于表单处理
from flask_wtf import FlaskForm
# 导入WTForms字段类型
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, IntegerField, BooleanField
# 导入WTForms验证器
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange, ValidationError
# 导入数据库模型
from models import User, TaskCategory

class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=80, message='用户名长度必须在3-80个字符之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码长度至少6个字符')
    ])

class UserRegistrationForm(FlaskForm):
    """用户注册表单（仅管理员可用）"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=80, message='用户名长度必须在3-80个字符之间')
    ])
    full_name = StringField('真实姓名', validators=[
        DataRequired(message='真实姓名不能为空'),
        Length(min=2, max=100, message='真实姓名长度必须在2-100个字符之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码长度至少6个字符')
    ])
    password_confirm = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    role = SelectField('用户角色', choices=[
        ('admin', '管理员'),
        ('data_entry', '录入员'),
        ('supervisor', '监督员')
    ], validators=[DataRequired(message='请选择用户角色')])
    is_active = BooleanField('账户激活', default=True)

    def validate_username(self, username):
        """验证用户名是否已存在"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名')

class UserEditForm(FlaskForm):
    """用户编辑表单（仅管理员可用）"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=80, message='用户名长度必须在3-80个字符之间')
    ])
    full_name = StringField('真实姓名', validators=[
        DataRequired(message='真实姓名不能为空'),
        Length(min=2, max=100, message='真实姓名长度必须在2-100个字符之间')
    ])
    role = SelectField('用户角色', choices=[
        ('admin', '管理员'),
        ('data_entry', '录入员'),
        ('supervisor', '监督员')
    ], validators=[DataRequired(message='请选择用户角色')])
    is_active = BooleanField('账户激活')
    
    def __init__(self, original_user=None, *args, **kwargs):
        """初始化表单，original_user用于编辑时排除自身的唯一性验证"""
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.original_user = original_user

    def validate_username(self, username):
        """验证用户名是否已存在（编辑时排除自身）"""
        if self.original_user and username.data == self.original_user.username:
            return
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名')

class PasswordChangeForm(FlaskForm):
    """密码修改表单（管理员重置其他用户密码）"""
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不能为空'),
        Length(min=6, message='密码长度至少6个字符')
    ])
    new_password_confirm = PasswordField('确认新密码', validators=[
        DataRequired(message='请确认新密码'),
        EqualTo('new_password', message='两次输入的密码不一致')
    ])

class TaskCategoryForm(FlaskForm):
    """任务分类表单（创建和编辑任务分类）"""
    name = StringField('分类名称（英文键值）', validators=[
        DataRequired(message='分类名称不能为空'),
        Length(min=1, max=50, message='分类名称长度必须在1-50个字符之间')
    ])
    display_name = StringField('显示名称（中文）', validators=[
        DataRequired(message='显示名称不能为空'),
        Length(min=1, max=100, message='显示名称长度必须在1-100个字符之间')
    ])
    description = TextAreaField('分类描述', validators=[
        Optional(),
        Length(max=500, message='分类描述长度不能超过500个字符')
    ])
    color = SelectField('颜色样式', choices=[
        ('primary', '主要色（蓝色）'),
        ('secondary', '次要色（灰色）'),
        ('success', '成功色（绿色）'),
        ('danger', '危险色（红色）'),
        ('warning', '警告色（黄色）'),
        ('info', '信息色（青色）'),
        ('light', '浅色'),
        ('dark', '深色')
    ], validators=[DataRequired(message='请选择颜色样式')], default='secondary')
    is_active = BooleanField('启用分类', default=True)
    sort_order = IntegerField('排序顺序', validators=[
        Optional(),
        NumberRange(min=0, max=9999, message='排序顺序必须在0-9999之间')
    ], default=0)
    
    def __init__(self, original_category=None, *args, **kwargs):
        """初始化表单，original_category用于编辑时排除自身的唯一性验证"""
        super(TaskCategoryForm, self).__init__(*args, **kwargs)
        self.original_category = original_category
    
    def validate_name(self, name):
        """验证分类名称是否已存在（编辑时排除自身）"""
        # 验证名称格式（只允许字母、数字、下划线）
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', name.data):
            raise ValidationError('分类名称只能包含字母、数字和下划线')
        
        # 检查是否与现有分类冲突
        if self.original_category and name.data.lower() == self.original_category.name:
            return
        category = TaskCategory.query.filter_by(name=name.data.lower()).first()
        if category:
            raise ValidationError('该分类名称已被使用，请选择其他名称')

class TaskForm(FlaskForm):
    """任务表单（创建和编辑任务）"""
    title = StringField('任务标题', validators=[
        DataRequired(message='任务标题不能为空'),
        Length(min=1, max=200, message='任务标题长度必须在1-200个字符之间')
    ])
    description = TextAreaField('任务描述', validators=[
        Optional(),
        Length(max=1000, message='任务描述长度不能超过1000个字符')
    ])
    category = SelectField('任务分类', validators=[DataRequired(message='请选择任务分类')])
    assignee = StringField('负责人', validators=[
        Optional(),
        Length(max=100, message='负责人姓名长度不能超过100个字符')
    ])
    planned_start_date = DateField('计划开始日期', validators=[Optional()])
    planned_end_date = DateField('计划完成日期', validators=[Optional()])
    status = SelectField('任务状态', choices=[
        ('pending', '待处理'),
        ('in-progress', '进行中'),
        ('completed', '已完成')
    ], validators=[DataRequired(message='请选择任务状态')])
    progress = IntegerField('完成进度（%）', validators=[
        Optional(),  # 允许进度为空，默认值为0
        NumberRange(min=0, max=100, message='进度必须在0-100之间')
    ], default=0)

    def __init__(self, *args, **kwargs):
        """初始化表单，动态加载任务分类选项"""
        super(TaskForm, self).__init__(*args, **kwargs)
        # 动态加载任务分类选项
        self.category.choices = TaskCategory.get_choices_for_form()
        # 如果没有分类，提供默认选项
        if not self.category.choices:
            self.category.choices = [('general', '通用任务')]

    def validate_planned_end_date(self, planned_end_date):
        """验证计划完成日期不能早于计划开始日期"""
        if self.planned_start_date.data and planned_end_date.data:
            if planned_end_date.data < self.planned_start_date.data:
                raise ValidationError('计划完成日期不能早于计划开始日期')