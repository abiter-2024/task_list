# 权限装饰器模块 - 用于基于角色的访问控制
from functools import wraps
from flask import abort, redirect, url_for, flash, request
from flask_login import current_user, login_required

def role_required(*roles):
    """
    角色权限装饰器
    参数: roles - 允许访问的角色列表
    用法: @role_required('admin', 'supervisor')
    """
    def decorator(f):
        @wraps(f)
        @login_required  # 确保用户已登录
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('请先登录', 'warning')
                return redirect(url_for('login'))
            
            if current_user.role not in roles:
                flash('您没有权限访问此页面', 'danger')
                abort(403)
            
            if not current_user.is_active:
                flash('您的账户已被禁用，请联系管理员', 'danger')
                return redirect(url_for('login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """
    管理员权限装饰器
    仅管理员可以访问的页面使用
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        
        if current_user.role != 'admin':
            flash('仅管理员可以访问此页面', 'danger')
            abort(403)
        
        if not current_user.is_active:
            flash('您的账户已被禁用，请联系管理员', 'danger')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def data_entry_required(f):
    """
    录入员权限装饰器
    录入员和监督员可以访问的页面使用
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        
        if current_user.role not in ['data_entry', 'supervisor']:
            flash('您没有权限访问此页面', 'danger')
            abort(403)
        
        if not current_user.is_active:
            flash('您的账户已被禁用，请联系管理员', 'danger')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def supervisor_required(f):
    """
    监督员权限装饰器
    仅监督员可以访问的页面使用
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        
        if current_user.role != 'supervisor':
            flash('仅监督员可以访问此页面', 'danger')
            abort(403)
        
        if not current_user.is_active:
            flash('您的账户已被禁用，请联系管理员', 'danger')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def task_permission_required(permission_type):
    """
    任务权限装饰器
    用于检查用户是否有权限对特定任务进行操作
    permission_type: 'view', 'edit', 'delete'
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('请先登录', 'warning')
                return redirect(url_for('login'))
            
            if not current_user.is_active:
                flash('您的账户已被禁用，请联系管理员', 'danger')
                return redirect(url_for('login'))
            
            # 管理员不能访问任务相关页面
            if current_user.role == 'admin':
                flash('管理员不能访问任务管理页面', 'danger')
                abort(403)
            
            # 对于需要任务ID的操作，在函数内部进行具体权限检查
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def check_task_edit_permission(task):
    """
    检查用户是否有权限编辑特定任务
    参数: task - 任务对象
    返回: True/False
    """
    if not current_user.is_authenticated or not current_user.is_active:
        return False
    
    # 管理员不能编辑任务
    if current_user.role == 'admin':
        return False
    
    # 录入员只能编辑自己创建的任务
    if current_user.role == 'data_entry':
        return task.creator_id == current_user.id
    
    # 监督员可以编辑所有任务
    if current_user.role == 'supervisor':
        return True
    
    return False

def check_task_view_permission(task):
    """
    检查用户是否有权限查看特定任务
    参数: task - 任务对象
    返回: True/False
    """
    if not current_user.is_authenticated or not current_user.is_active:
        return False
    
    # 管理员不能查看任务
    if current_user.role == 'admin':
        return False
    
    # 录入员和监督员都可以查看所有任务
    if current_user.role in ['data_entry', 'supervisor']:
        return True
    
    return False

def check_task_delete_permission(task):
    """
    检查用户是否有权限删除特定任务
    参数: task - 任务对象
    返回: True/False
    """
    if not current_user.is_authenticated or not current_user.is_active:
        return False
    
    # 管理员不能删除任务
    if current_user.role == 'admin':
        return False
    
    # 录入员只能删除自己创建的任务
    if current_user.role == 'data_entry':
        return task.creator_id == current_user.id
    
    # 监督员可以删除所有任务
    if current_user.role == 'supervisor':
        return True
    
    return False

def get_permission_denied_message(task, operation='编辑'):
    """
    生成权限被拒绝时的详细提示信息
    参数: 
        task - 任务对象
        operation - 操作类型 ('编辑', '删除', '修改')
    返回: 错误信息字符串
    """
    if current_user.role == 'data_entry':
        creator_name = task.get_creator_display()
        if task.creator_id and task.creator_id != current_user.id:
            return f'您没有权限{operation}此任务。此任务由 {creator_name} 创建，录入员只能{operation}自己创建的任务。'
        else:
            return f'您没有权限{operation}此任务'
    else:
        return f'您没有权限{operation}此任务'