# 导入Flask SQLAlchemy扩展
from flask_sqlalchemy import SQLAlchemy
# 导入datetime模块用于时间戳
from datetime import datetime
# 导入Flask-Login扩展用于用户会话管理
from flask_login import UserMixin
# 导入Werkzeug用于密码加密
from werkzeug.security import generate_password_hash, check_password_hash

# 创建SQLAlchemy数据库实例
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """用户模型类，用于存储用户信息和权限管理"""
    
    __tablename__ = 'users'  # 指定数据库表名
    
    # 数据库字段定义
    id = db.Column(db.Integer, primary_key=True)  # 主键，自增整数
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一且必填
    email = db.Column(db.String(120), unique=True, nullable=True)  # 邮箱，可选字段
    password_hash = db.Column(db.String(255), nullable=False)  # 密码哈希值
    full_name = db.Column(db.String(100), nullable=False)  # 真实姓名
    role = db.Column(db.String(20), nullable=False, default='data_entry')  # 用户角色
    active = db.Column(db.Boolean, nullable=False, default=True)  # 账户是否激活
    
    # 系统时间字段
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    # 关联关系：用户创建的任务
    created_tasks = db.relationship('Task', backref='creator', lazy='dynamic', foreign_keys='Task.creator_id')
    
    def __init__(self, username=None, email=None, full_name=None, role='data_entry', is_active=True, **kwargs):
        """初始化用户对象"""
        super(User, self).__init__(**kwargs)
        if username:
            self.username = username
        if email:  # 邮箱现在是可选的
            self.email = email
        if full_name:
            self.full_name = full_name
        self.role = role
        self.active = is_active
    
    @property
    def is_active(self):
        """返回用户是否激活状态（Flask-Login需要）"""
        return self.active
    
    @is_active.setter
    def is_active(self, value):
        """设置用户激活状态"""
        self.active = value
    
    # 数据库约束条件
    __table_args__ = (
        # 用户角色只能是这三个值之一：管理员、录入员、监督员
        db.CheckConstraint(role.in_(['admin', 'data_entry', 'supervisor']), name='valid_role'),
    )
    
    def __repr__(self):
        """返回对象的字符串表示"""
        return f'<User {self.username}: {self.get_role_display()}>'
    
    def set_password(self, password):
        """设置用户密码（加密存储）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证用户密码"""
        return check_password_hash(self.password_hash, password)
    
    def get_role_display(self):
        """获取用户角色的中文显示名称"""
        role_names = {
            'admin': '管理员',
            'data_entry': '录入员', 
            'supervisor': '监督员'
        }
        return role_names.get(self.role, self.role)
    
    def get_role_color(self):
        """根据用户角色获取Bootstrap颜色类"""
        role_colors = {
            'admin': 'danger',      # 管理员 - 红色
            'data_entry': 'primary', # 录入员 - 蓝色
            'supervisor': 'success'  # 监督员 - 绿色
        }
        return role_colors.get(self.role, 'secondary')
    
    def has_permission(self, permission):
        """检查用户是否有特定权限"""
        permissions = {
            'admin': ['manage_users'],  # 管理员只能管理用户
            'data_entry': ['create_task', 'edit_own_task', 'view_all_tasks'],  # 录入员可以创建和编辑自己的任务
            'supervisor': ['view_all_tasks', 'edit_all_tasks']  # 监督员可以查看和编辑所有任务
        }
        return permission in permissions.get(self.role, [])
    
    def can_edit_task(self, task):
        """检查用户是否可以编辑特定任务"""
        if self.role == 'admin':
            return False  # 管理员不能编辑任务
        elif self.role == 'data_entry':
            return task.creator_id == self.id  # 录入员只能编辑自己创建的任务
        elif self.role == 'supervisor':
            return True  # 监督员可以编辑所有任务
        return False
    
    def can_view_task(self, task):
        """检查用户是否可以查看特定任务"""
        if self.role == 'admin':
            return False  # 管理员不能查看任务
        return True  # 录入员和监督员都可以查看所有任务
    
    def to_dict(self):
        """将用户对象转换为字典，用于JSON序列化"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,  # 邮箱可能为None
            'full_name': self.full_name,
            'role': self.role,
            'role_display': self.get_role_display(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TaskCategory(db.Model):
    """任务分类模型类，用于管理任务分类"""
    
    __tablename__ = 'task_categories'  # 指定数据库表名
    
    # 数据库字段定义
    id = db.Column(db.Integer, primary_key=True)  # 主键，自增整数
    name = db.Column(db.String(50), unique=True, nullable=False)  # 分类名称（英文键值）
    display_name = db.Column(db.String(100), nullable=False)  # 分类显示名称（中文）
    description = db.Column(db.Text, nullable=True)  # 分类描述
    color = db.Column(db.String(20), nullable=False, default='secondary')  # Bootstrap颜色类
    is_active = db.Column(db.Boolean, nullable=False, default=True)  # 是否启用
    sort_order = db.Column(db.Integer, nullable=False, default=0)  # 排序顺序
    
    # 系统时间字段
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    # 关联关系：分类下的任务
    tasks = db.relationship('Task', backref='task_category', lazy='dynamic', foreign_keys='Task.category_id')
    
    def __repr__(self):
        """返回对象的字符串表示"""
        return f'<TaskCategory {self.name}: {self.display_name}>'
    
    @classmethod
    def create_category(cls, name, display_name, description=None, color='secondary', is_active=True, sort_order=0):
        """创建新分类，并进行数据验证"""
        # 验证名称不能为空
        if not name or not name.strip():
            raise ValueError("分类名称不能为空")
        
        # 验证显示名称不能为空
        if not display_name or not display_name.strip():
            raise ValueError("分类显示名称不能为空")
        
        # 验证名称格式（只允许字母、数字、下划线）
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', name.strip()):
            raise ValueError("分类名称只能包含字母、数字和下划线")
        
        # 验证颜色值
        valid_colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
        if color not in valid_colors:
            raise ValueError(f"颜色值不合法，必须是: {', '.join(valid_colors)}")
        
        # 创建分类实例
        category = cls()
        category.name = name.strip().lower()  # 转换为小写
        category.display_name = display_name.strip()
        category.description = description.strip() if description else None
        category.color = color
        category.is_active = is_active
        category.sort_order = sort_order
        
        return category
    
    def update_category(self, **kwargs):
        """更新分类信息，并进行数据验证"""
        # 更新显示名称
        if 'display_name' in kwargs:
            display_name = kwargs['display_name']
            if not display_name or not display_name.strip():
                raise ValueError("分类显示名称不能为空")
            self.display_name = display_name.strip()
        
        # 更新描述
        if 'description' in kwargs:
            description = kwargs['description']
            self.description = description.strip() if description else None
        
        # 更新颜色
        if 'color' in kwargs:
            color = kwargs['color']
            valid_colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
            if color not in valid_colors:
                raise ValueError(f"颜色值不合法，必须是: {', '.join(valid_colors)}")
            self.color = color
        
        # 更新启用状态
        if 'is_active' in kwargs:
            self.is_active = kwargs['is_active']
        
        # 更新排序顺序
        if 'sort_order' in kwargs:
            sort_order = kwargs['sort_order']
            if not isinstance(sort_order, int):
                raise ValueError("排序顺序必须是整数")
            self.sort_order = sort_order
        
        # 更新修改时间
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def get_active_categories():
        """获取所有启用的分类，按排序顺序返回"""
        return TaskCategory.query.filter_by(is_active=True).order_by(TaskCategory.sort_order.asc(), TaskCategory.display_name.asc()).all()
    
    @staticmethod
    def get_choices_for_form():
        """获取表单选择项格式的分类列表"""
        categories = TaskCategory.get_active_categories()
        return [(cat.name, cat.display_name) for cat in categories]
    
    def to_dict(self):
        """将分类对象转换为字典，用于JSON序列化"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'color': self.color,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'task_count': self.tasks.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Task(db.Model):
    """任务模型类，用于存储任务信息"""
    
    __tablename__ = 'tasks'  # 指定数据库表名
    
    # 数据库字段定义
    id = db.Column(db.Integer, primary_key=True)  # 主键，自增整数
    title = db.Column(db.String(200), nullable=False)  # 任务标题，必填字段
    description = db.Column(db.Text, nullable=True)  # 任务描述，可选字段
    status = db.Column(db.String(20), nullable=False, default='pending')  # 任务状态，默认为待处理
    progress = db.Column(db.Integer, nullable=False, default=0)  # 任务进度，默认为0%
    
    # 新增字段：时间规划
    planned_start_date = db.Column(db.Date, nullable=True)  # 计划开始日期
    planned_end_date = db.Column(db.Date, nullable=True)  # 计划完成日期
    
    # 新增字段：任务管理
    assignee = db.Column(db.String(100), nullable=True)  # 任务分配人/负责人
    category = db.Column(db.String(50), nullable=True, default='general')  # 任务分类（兼容旧数据）
    category_id = db.Column(db.Integer, db.ForeignKey('task_categories.id'), nullable=True)  # 任务分类外键
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 任务创建者ID
    
    # 系统时间字段
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    # 数据库约束条件
    __table_args__ = (
        # 状态字段只能是这三个值之一
        db.CheckConstraint(status.in_(['pending', 'in-progress', 'completed']), name='valid_status'),
        # 进度值必须在0-100之间
        db.CheckConstraint('progress >= 0 AND progress <= 100', name='valid_progress'),
    )
    
    def __repr__(self):
        """返回对象的字符串表示"""
        return f'<Task {self.id}: {self.title}>'
    

    
    @classmethod
    def create_task(cls, title, description=None, status='pending', progress=0, 
                   planned_start_date=None, planned_end_date=None, assignee=None, category=None, category_id=None, creator_id=None):
        """创建新任务，并进行数据验证"""
        # 验证标题不能为空
        if not title or not title.strip():
            raise ValueError("任务标题不能为空")
        
        # 验证状态是否合法
        if status not in ['pending', 'in-progress', 'completed']:
            raise ValueError("任务状态不合法")
        
        # 验证进度值范围
        if not isinstance(progress, int) or progress < 0 or progress > 100:
            raise ValueError("进度必须是0-100之间的整数")
        
        # 验证任务分类（支持新旧两种方式）
        if category_id:
            # 使用新的动态分类系统
            task_category = TaskCategory.query.filter_by(id=category_id, is_active=True).first()
            if not task_category:
                raise ValueError("指定的任务分类不存在或已禁用")
        elif category:
            # 兼容旧的硬编码分类系统
            valid_categories = ['general', 'development', 'design', 'testing', 'deployment', 'meeting', 'research']
            if category not in valid_categories:
                # 尝试查找对应的动态分类
                task_category = TaskCategory.query.filter_by(name=category, is_active=True).first()
                if task_category:
                    category_id = task_category.id
                else:
                    raise ValueError(f"任务分类不合法")
        else:
            # 默认使用通用任务分类
            default_category = TaskCategory.query.filter_by(name='general', is_active=True).first()
            if default_category:
                category_id = default_category.id
                category = default_category.name
            else:
                category = 'general'  # 退回到硬编码方式
        
        # 验证日期逻辑性（开始日期不能晚于结束日期）
        if planned_start_date and planned_end_date and planned_start_date > planned_end_date:
            raise ValueError("计划开始日期不能晚于计划完成日期")
        
        # 创建任务实例并显式指定参数
        task = cls()
        task.title = title.strip()
        task.description = description.strip() if description else None
        task.status = status
        task.progress = progress
        task.planned_start_date = planned_start_date
        task.planned_end_date = planned_end_date
        task.assignee = assignee.strip() if assignee else None
        task.category = category  # 保留兼容性
        task.category_id = category_id  # 新的动态分类
        task.creator_id = creator_id  # 设置任务创建者
        
        return task
    
    def update_task(self, **kwargs):
        """更新任务信息，并进行数据验证"""
        # 更新标题
        if 'title' in kwargs:
            title = kwargs['title']
            if not title or not title.strip():
                raise ValueError("任务标题不能为空")
            self.title = title.strip()
        
        # 更新描述
        if 'description' in kwargs:
            description = kwargs['description']
            self.description = description.strip() if description else None
        
        # 更新状态
        if 'status' in kwargs:
            status = kwargs['status']
            if status not in ['pending', 'in-progress', 'completed']:
                raise ValueError("任务状态不合法")
            self.status = status
        
        # 更新进度
        if 'progress' in kwargs:
            progress = kwargs['progress']
            if not isinstance(progress, int) or progress < 0 or progress > 100:
                raise ValueError("进度必须是0-100之间的整数")
            self.progress = progress
        
        # 更新计划开始日期
        if 'planned_start_date' in kwargs:
            self.planned_start_date = kwargs['planned_start_date']
        
        # 更新计划完成日期
        if 'planned_end_date' in kwargs:
            self.planned_end_date = kwargs['planned_end_date']
        
        # 验证日期逻辑性
        if self.planned_start_date and self.planned_end_date and self.planned_start_date > self.planned_end_date:
            raise ValueError("计划开始日期不能晚于计划完成日期")
        
        # 更新任务分配人
        if 'assignee' in kwargs:
            assignee = kwargs['assignee']
            self.assignee = assignee.strip() if assignee else None
        
        # 更新任务分类
        if 'category' in kwargs or 'category_id' in kwargs:
            category = kwargs.get('category')
            category_id = kwargs.get('category_id')
            
            if category_id:
                # 使用新的动态分类系统
                task_category = TaskCategory.query.filter_by(id=category_id, is_active=True).first()
                if not task_category:
                    raise ValueError("指定的任务分类不存在或已禁用")
                self.category_id = category_id
                self.category = task_category.name  # 同步更新兼容字段
            elif category:
                # 兼容旧的硬编码分类系统
                valid_categories = ['general', 'development', 'design', 'testing', 'deployment', 'meeting', 'research']
                if category in valid_categories:
                    self.category = category
                    # 尝试查找对应的动态分类
                    task_category = TaskCategory.query.filter_by(name=category, is_active=True).first()
                    if task_category:
                        self.category_id = task_category.id
                else:
                    # 尝试查找对应的动态分类
                    task_category = TaskCategory.query.filter_by(name=category, is_active=True).first()
                    if task_category:
                        self.category_id = task_category.id
                        self.category = task_category.name
                    else:
                        raise ValueError(f"任务分类不合法")
        
        # 更新修改时间
        self.updated_at = datetime.utcnow()
    
    def get_status_color(self):
        """根据任务状态获取Bootstrap颜色类"""
        status_colors = {
            'pending': 'secondary',     # 待处理 - 灰色
            'in-progress': 'warning',   # 进行中 - 黄色
            'completed': 'success'      # 已完成 - 绿色
        }
        return status_colors.get(self.status, 'secondary')
    
    def get_progress_color(self):
        """根据进度百分比获取Bootstrap进度条颜色类"""
        if self.progress == 0:
            return 'bg-secondary'    # 0% - 灰色
        elif self.progress < 30:
            return 'bg-danger'       # <30% - 红色
        elif self.progress < 70:
            return 'bg-warning'      # 30-70% - 黄色
        else:
            return 'bg-success'      # >70% - 绿色
    
    def get_category_display(self):
        """获取任务分类的中文显示名称"""
        # 优先使用动态分类
        if self.category_id and self.task_category:
            return self.task_category.display_name
        
        # 退回到硬编码分类（兼容性）
        category_names = {
            'general': '通用任务',
            'development': '开发任务',
            'design': '设计任务',
            'testing': '测试任务',
            'deployment': '部署任务',
            'meeting': '会议任务',
            'research': '研究任务'
        }
        return category_names.get(self.category, self.category or '未分类')
    
    def get_category_color(self):
        """根据任务分类获取Bootstrap颜色类"""
        # 优先使用动态分类
        if self.category_id and self.task_category:
            return self.task_category.color
        
        # 退回到硬编码分类（兼容性）
        category_colors = {
            'general': 'secondary',
            'development': 'primary',
            'design': 'info',
            'testing': 'warning',
            'deployment': 'success',
            'meeting': 'dark',
            'research': 'light'
        }
        return category_colors.get(self.category, 'secondary')
    
    def get_status_display(self):
        """获取任务状态的中文显示名称"""
        status_names = {
            'pending': '待处理',
            'in-progress': '进行中',
            'completed': '已完成'
        }
        return status_names.get(self.status, self.status)
    
    def get_assignee_display(self):
        """获取任务分配人显示，如果为空则显示"未分配"""
        return self.assignee if self.assignee else '未分配'
    
    def get_creator_display(self):
        """获取任务创建者显示名称"""
        if self.creator:
            return self.creator.full_name
        return '系统'
    
    def to_dict(self):
        """将任务对象转换为字典，用于JSON序列化"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'progress': self.progress,
            'planned_start_date': self.planned_start_date.isoformat() if self.planned_start_date else None,
            'planned_end_date': self.planned_end_date.isoformat() if self.planned_end_date else None,
            'assignee': self.assignee,
            'category': self.category,
            'creator_id': self.creator_id,
            'creator_name': self.get_creator_display(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }