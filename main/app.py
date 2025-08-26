# 导入Flask核心模块
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
# 导入Flask-Login用户认证
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# 导入数据库模型
from models import db, Task, User, TaskCategory
# 导入表单
from forms import LoginForm, UserRegistrationForm, UserEditForm, PasswordChangeForm, TaskForm, TaskCategoryForm
# 导入权限装饰器
from auth_decorators import admin_required, data_entry_required, role_required, check_task_edit_permission, check_task_view_permission, check_task_delete_permission, get_permission_denied_message
import os
# 导入日期时间处理模块
from datetime import datetime, date

def create_app():
    """应用工厂模式，创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 应用配置
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # 密钥，生产环境需更改
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_progress.db'  # SQLite数据库路径
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭修改跟踪，提升性能
    app.config['WTF_CSRF_ENABLED'] = True  # 启用CSRF保护
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # type: ignore  # 未登录用户重定向的登录页面
    login_manager.login_message = '请先登录才能访问此页面。'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        """加载用户回调函数"""
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()  # 创建所有数据库表
        
        # 创建默认管理员账户（如果不存在）
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                full_name='系统管理员',
                role='admin',
                is_active=True
            )
            admin_user.set_password('admin123')  # 默认密码，生产环境需修改
            db.session.add(admin_user)
            db.session.commit()
        
        # 创建默认任务分类（如果不存在）
        if TaskCategory.query.count() == 0:
            default_categories = [
                TaskCategory.create_category('general', '通用任务', '默认的通用任务分类', 'secondary', True, 0),
                TaskCategory.create_category('development', '开发任务', '软件开发相关任务', 'primary', True, 1),
                TaskCategory.create_category('design', '设计任务', 'UI/UX设计相关任务', 'info', True, 2),
                TaskCategory.create_category('testing', '测试任务', '软件测试相关任务', 'warning', True, 3),
                TaskCategory.create_category('deployment', '部署任务', '系统部署相关任务', 'success', True, 4),
                TaskCategory.create_category('meeting', '会议任务', '会议和沟通相关任务', 'dark', True, 5),
                TaskCategory.create_category('research', '研究任务', '研究和调研相关任务', 'light', True, 6)
            ]
            
            for category in default_categories:
                db.session.add(category)
            
            db.session.commit()
        
        # 如果数据库为空，添加示例数据
        if Task.query.count() == 0:
            # 创建示例用户
            sample_users = [
                User(
                    username='data_entry1',
                    full_name='录入员一',
                    role='data_entry',
                    is_active=True
                ),
                User(
                    username='supervisor1',
                    full_name='监督员一',
                    role='supervisor',
                    is_active=True
                )
            ]
            
            for user in sample_users:
                user.set_password('123456')  # 默认密码
                db.session.add(user)
            
            db.session.commit()
            
            # 获取创建的用户ID
            data_entry_user = User.query.filter_by(username='data_entry1').first()
            
            # 确保用户存在
            if not data_entry_user:
                raise Exception('无法创建示例任务：找不到data_entry1用户')
            
            sample_tasks = [
                Task.create_task(
                    title="搭建开发环境", 
                    description="安装Python、Flask和相关依赖包，配置开发环境", 
                    status="completed", 
                    progress=100,
                    planned_start_date=date(2024, 1, 1), 
                    planned_end_date=date(2024, 1, 5),
                    assignee="张三", 
                    category="development",
                    creator_id=data_entry_user.id
                ),
                Task.create_task(
                    title="设计数据库架构", 
                    description="创建SQLAlchemy数据模型，设计任务管理数据表结构", 
                    status="completed", 
                    progress=100,
                    planned_start_date=date(2024, 1, 6), 
                    planned_end_date=date(2024, 1, 10),
                    assignee="李四", 
                    category="development",
                    creator_id=data_entry_user.id
                ),
                Task.create_task(
                    title="实现后端API接口", 
                    description="开发Flask路由和RESTful API接口，实现CRUD操作", 
                    status="in-progress", 
                    progress=75,
                    planned_start_date=date(2024, 1, 11), 
                    planned_end_date=date(2024, 1, 20),
                    assignee="王五", 
                    category="development",
                    creator_id=data_entry_user.id
                ),
                Task.create_task(
                    title="创建前端页面模板", 
                    description="使用Bootstrap设计响应式HTML模板和用户界面", 
                    status="pending", 
                    progress=0,
                    planned_start_date=date(2024, 1, 21), 
                    planned_end_date=date(2024, 1, 30),
                    assignee="赵六", 
                    category="design",
                    creator_id=data_entry_user.id
                ),
                Task.create_task(
                    title="添加用户认证系统", 
                    description="实现用户登录、注册和权限管理功能模块", 
                    status="pending", 
                    progress=0,
                    planned_start_date=date(2024, 2, 1), 
                    planned_end_date=date(2024, 2, 15),
                    assignee="钱七", 
                    category="development",
                    creator_id=data_entry_user.id
                )
            ]
            
            # 将示例任务添加到数据库
            for task in sample_tasks:
                db.session.add(task)
            
            db.session.commit()  # 提交数据库事务
    
    return app

# 创建Flask应用实例
app = create_app()

# ========== 认证路由 (用户登录、注册、管理) ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录页面"""
    if current_user.is_authenticated:
        # 如果用户已登录，根据角色重定向
        if current_user.role == 'admin':
            return redirect(url_for('admin_users'))
        else:
            return redirect(url_for('tasks'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('您的账户已被禁用，请联系管理员', 'danger')
                return render_template('login.html', form=form)
            
            login_user(user)
            flash(f'欢迎，{user.full_name}!', 'success')
            
            # 根据用户角色重定向到适当的页面
            if user.role == 'admin':
                return redirect(url_for('admin_users'))
            else:
                return redirect(url_for('tasks'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('login'))

@app.route('/admin/users')
@admin_required
def admin_users():
    """管理员 - 用户管理页面"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@admin_required
def admin_add_user():
    """管理员 - 添加新用户"""
    form = UserRegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                full_name=form.full_name.data,
                role=form.role.data,
                is_active=form.is_active.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'用户 {user.full_name} 创建成功！', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            flash('创建用户时发生错误', 'danger')
            db.session.rollback()
    
    return render_template('admin/add_user.html', form=form)

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    """管理员 - 编辑用户信息"""
    user = User.query.get_or_404(user_id)
    form = UserEditForm(original_user=user, obj=user)
    
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.full_name = form.full_name.data
            user.role = form.role.data
            user.is_active = form.is_active.data
            user.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash(f'用户 {user.full_name} 信息更新成功！', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            flash('更新用户信息时发生错误', 'danger')
            db.session.rollback()
    
    return render_template('admin/edit_user.html', form=form, user=user)

@app.route('/admin/users/<int:user_id>/reset_password', methods=['GET', 'POST'])
@admin_required
def admin_reset_password(user_id):
    """管理员 - 重置用户密码"""
    user = User.query.get_or_404(user_id)
    form = PasswordChangeForm()
    
    if form.validate_on_submit():
        try:
            user.set_password(form.new_password.data)
            user.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash(f'用户 {user.full_name} 的密码重置成功！', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            flash('重置密码时发生错误', 'danger')
            db.session.rollback()
    
    return render_template('admin/reset_password.html', form=form, user=user)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """管理员 - 删除用户"""
    user = User.query.get_or_404(user_id)
    
    # 不能删除自己
    if user.id == current_user.id:
        flash('不能删除自己的账户', 'danger')
        return redirect(url_for('admin_users'))
    
    try:
        # 删除用户时，其创建的任务的creator_id设置为None
        tasks = Task.query.filter_by(creator_id=user.id).all()
        for task in tasks:
            task.creator_id = None
        
        db.session.delete(user)
        db.session.commit()
        
        flash(f'用户 {user.full_name} 已被删除', 'success')
    except Exception as e:
        flash('删除用户时发生错误', 'danger')
        db.session.rollback()
    
    return redirect(url_for('admin_users'))

# ========== 任务分类管理路由 ==========

@app.route('/admin/categories')
@admin_required
def admin_categories():
    """管理员 - 任务分类管理页面"""
    categories = TaskCategory.query.order_by(TaskCategory.sort_order.asc(), TaskCategory.display_name.asc()).all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@admin_required
def admin_add_category():
    """管理员 - 添加新任务分类"""
    form = TaskCategoryForm()
    if form.validate_on_submit():
        try:
            category = TaskCategory.create_category(
                name=form.name.data,
                display_name=form.display_name.data,
                description=form.description.data,
                color=form.color.data,
                is_active=form.is_active.data,
                sort_order=form.sort_order.data or 0
            )
            
            db.session.add(category)
            db.session.commit()
            
            flash(f'任务分类 "{category.display_name}" 创建成功！', 'success')
            return redirect(url_for('admin_categories'))
            
        except ValueError as e:
            flash(f'创建分类时发生错误：{str(e)}', 'danger')
            db.session.rollback()
        except Exception as e:
            flash('创建分类时发生错误', 'danger')
            db.session.rollback()
    
    return render_template('admin/add_category.html', form=form)

@app.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_category(category_id):
    """管理员 - 编辑任务分类"""
    category = TaskCategory.query.get_or_404(category_id)
    form = TaskCategoryForm(original_category=category, obj=category)
    
    if form.validate_on_submit():
        try:
            category.update_category(
                display_name=form.display_name.data,
                description=form.description.data,
                color=form.color.data,
                is_active=form.is_active.data,
                sort_order=form.sort_order.data or 0
            )
            
            db.session.commit()
            flash(f'任务分类 "{category.display_name}" 更新成功！', 'success')
            return redirect(url_for('admin_categories'))
            
        except ValueError as e:
            flash(f'更新分类时发生错误：{str(e)}', 'danger')
            db.session.rollback()
        except Exception as e:
            flash('更新分类时发生错误', 'danger')
            db.session.rollback()
    
    return render_template('admin/edit_category.html', form=form, category=category)

@app.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    """管理员 - 删除任务分类"""
    category = TaskCategory.query.get_or_404(category_id)
    
    # 检查是否有任务使用该分类
    task_count = category.tasks.count()
    if task_count > 0:
        flash(f'无法删除分类 "{category.display_name}"，还有 {task_count} 个任务使用该分类', 'danger')
        return redirect(url_for('admin_categories'))
    
    try:
        db.session.delete(category)
        db.session.commit()
        
        flash(f'任务分类 "{category.display_name}" 已被删除', 'success')
    except Exception as e:
        flash('删除分类时发生错误', 'danger')
        db.session.rollback()
    
    return redirect(url_for('admin_categories'))

# ========== Web路由 (HTML页面) ==========

@app.route('/')
@login_required
def index():
    """主页，显示任务概览和统计信息"""
    # 管理员重定向到用户管理页面
    if current_user.role == 'admin':
        return redirect(url_for('admin_users'))
    
    # 获取当前用户可以查看的任务
    if current_user.role == 'data_entry':
        # 录入员可以查看所有任务，但只能编辑自己创建的
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    elif current_user.role == 'supervisor':
        # 监督员可以查看所有任务
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    else:
        tasks = []
    
    # 计算任务统计数据
    total_tasks = len(tasks)  # 总任务数
    completed_tasks = len([t for t in tasks if t.status == 'completed'])  # 已完成任务数
    in_progress_tasks = len([t for t in tasks if t.status == 'in-progress'])  # 进行中任务数
    pending_tasks = len([t for t in tasks if t.status == 'pending'])  # 待处理任务数
    
    # 计算完成率
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # 组织统计数据
    stats = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': round(completion_rate, 1)
    }
    
    return render_template('index.html', tasks=tasks, stats=stats)

@app.route('/tasks')
@role_required('data_entry', 'supervisor')
def tasks():
    """任务管理页面，支持按状态筛选"""
    # 获取筛选参数，默认显示所有任务
    filter_status = request.args.get('status', 'all')
    
    if filter_status == 'all':
        # 获取所有任务
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    else:
        # 按指定状态筛选任务
        tasks = Task.query.filter_by(status=filter_status).order_by(Task.created_at.desc()).all()
    
    return render_template('tasks.html', tasks=tasks, current_filter=filter_status)

@app.route('/add_task', methods=['GET', 'POST'])
@role_required('data_entry', 'supervisor')
def add_task():
    """添加新任务页面，支持GET显示表单和POST提交数据"""
    form = TaskForm()
    
    if form.validate_on_submit():
        try:
            # 从表单获取数据
            progress_value = form.progress.data
            # 如果进度为None或空，默认为0
            if progress_value is None or progress_value == '':
                progress_value = 0
            
            task = Task.create_task(
                title=form.title.data,
                description=form.description.data,
                status=form.status.data,
                progress=int(progress_value),  # 确保进度是整数
                planned_start_date=form.planned_start_date.data,
                planned_end_date=form.planned_end_date.data,
                assignee=form.assignee.data,
                category=form.category.data,
                creator_id=current_user.id  # 设置任务创建者
            )
            
            db.session.add(task)
            db.session.commit()
            
            # 显示成功消息并重定向到任务列表
            flash('任务添加成功！', 'success')
            return redirect(url_for('tasks'))
            
        except ValueError as e:
            # 数据验证错误
            flash(f'错误： {str(e)}', 'error')
        except Exception as e:
            # 其他错误
            flash('添加任务时发生错误。', 'error')
            db.session.rollback()  # 回滚数据库事务
    else:
        # 表单验证失败时显示错误信息
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'error')
    
    return render_template('add_task.html', form=form)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@role_required('data_entry', 'supervisor')
def edit_task(task_id):
    """编辑任务页面，支持修改现有任务信息"""
    # 查找任务，如果不存在则返回404错误
    task = Task.query.get_or_404(task_id)
    
    # 检查编辑权限
    if not check_task_edit_permission(task):
        # 使用助手函数生成详细的权限提示信息
        error_message = get_permission_denied_message(task, '编辑')
        flash_category = 'warning' if current_user.role == 'data_entry' and task.creator_id and task.creator_id != current_user.id else 'danger'
        flash(error_message, flash_category)
        return redirect(url_for('tasks'))
    
    form = TaskForm(obj=task)
    
    if form.validate_on_submit():
        try:
            # 更新任务信息
            progress_value = form.progress.data
            # 如果进度为None或空，默认为0
            if progress_value is None or progress_value == '':
                progress_value = 0
                
            task.update_task(
                title=form.title.data,
                description=form.description.data,
                status=form.status.data,
                progress=int(progress_value),  # 确保进度是整数
                planned_start_date=form.planned_start_date.data,
                planned_end_date=form.planned_end_date.data,
                assignee=form.assignee.data,
                category=form.category.data
            )
            
            db.session.commit()
            flash('任务更新成功！', 'success')
            return redirect(url_for('tasks'))
            
        except ValueError as e:
            flash(f'错误： {str(e)}', 'error')
        except Exception as e:
            flash('更新任务时发生错误。', 'error')
            db.session.rollback()
    else:
        # 表单验证失败时显示错误信息
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'error')
    
    return render_template('edit_task.html', task=task, form=form)

# ========== API路由 (JSON接口) ==========

@app.route('/api/tasks', methods=['GET'])
@role_required('data_entry', 'supervisor')
def api_get_tasks():
    """获取所有任务或按状态筛选任务的API接口"""
    filter_status = request.args.get('status')
    
    if filter_status:
        # 按状态筛选
        tasks = Task.query.filter_by(status=filter_status).order_by(Task.created_at.desc()).all()
    else:
        # 获取所有任务
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'count': len(tasks)
    })

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
@role_required('data_entry', 'supervisor')
def api_get_task(task_id):
    """获取单个任务的API接口"""
    task = Task.query.get_or_404(task_id)
    return jsonify({'task': task.to_dict()})

@app.route('/api/tasks', methods=['POST'])
@role_required('data_entry', 'supervisor')
def api_create_task():
    """创建新任务API"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '没有提供数据'}), 400
        
        title = data.get('title')
        description = data.get('description')
        status = data.get('status', 'pending')
        progress = data.get('progress', 0)
        planned_start_date = data.get('planned_start_date')
        planned_end_date = data.get('planned_end_date')
        assignee = data.get('assignee')
        category = data.get('category')
        category_id = data.get('category_id')
        
        # 创建任务并设置创建者ID
        task = Task.create_task(
            title=title, 
            description=description, 
            status=status, 
            progress=progress,
            planned_start_date=planned_start_date,
            planned_end_date=planned_end_date,
            assignee=assignee,
            category=category,
            category_id=category_id,
            creator_id=current_user.id  # 设置当前用户为创建者
        )
        db.session.add(task)
        db.session.commit()
        
        return jsonify({'task': task.to_dict()}), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建任务时发生错误'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@role_required('data_entry', 'supervisor')
def api_update_task(task_id):
    """Update task"""
    try:
        task = Task.query.get_or_404(task_id)
        
        # 检查编辑权限
        if not check_task_edit_permission(task):
            # 使用助手函数生成详细的权限提示信息
            error_message = get_permission_denied_message(task, '修改')
            return jsonify({'error': error_message}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update only provided fields
        update_fields = {}
        for field in ['title', 'description', 'status', 'progress']:
            if field in data:
                update_fields[field] = data[field]
        
        if update_fields:
            task.update_task(**update_fields)
            db.session.commit()
        
        return jsonify({'task': task.to_dict()})
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the task'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@role_required('data_entry', 'supervisor')
def api_delete_task(task_id):
    """删除任务API"""
    try:
        task = Task.query.get_or_404(task_id)
        
        # 检查删除权限
        if not check_task_delete_permission(task):
            # 使用助手函数生成详细的权限提示信息
            error_message = get_permission_denied_message(task, '删除')
            return jsonify({'error': error_message}), 403
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': '任务删除成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除任务时发生错误'}), 500

@app.route('/api/tasks/<int:task_id>/progress', methods=['PUT'])
@role_required('data_entry', 'supervisor')
def api_update_progress(task_id):
    """更新任务进度API"""
    try:
        task = Task.query.get_or_404(task_id)
        
        # 检查编辑权限
        if not check_task_edit_permission(task):
            # 使用助手函数生成详细的权限提示信息
            error_message = get_permission_denied_message(task, '修改')
            return jsonify({'error': error_message}), 403
        
        data = request.get_json()
        
        if not data or 'progress' not in data:
            return jsonify({'error': '进度值是必需的'}), 400
        
        progress = data['progress']
        task.update_task(progress=progress)
        
        # 根据进度自动更新状态
        if progress == 100:
            task.status = 'completed'
        elif progress > 0:
            task.status = 'in-progress'
        
        db.session.commit()
        
        return jsonify({'task': task.to_dict()})
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新进度时发生错误'}), 500

@app.route('/api/stats')
def api_get_stats():
    """Get task statistics"""
    tasks = Task.query.all()
    
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == 'completed'])
    in_progress_tasks = len([t for t in tasks if t.status == 'in-progress'])
    pending_tasks = len([t for t in tasks if t.status == 'pending'])
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': round(completion_rate, 1)
    })

# Error handlers

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Resource not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)