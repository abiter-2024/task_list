# 任务进度管理系统

一个基于Python Flask的现代化任务进度管理系统，支持多用户角色权限管理和完整的任务生命周期管理。

## 📋 项目简介

本项目是一个功能完整的任务进度管理系统，采用Flask框架构建，提供了用户认证、角色权限管理、任务创建编辑、进度跟踪等核心功能。系统采用响应式设计，支持桌面端和移动端访问。

### 目标用户
- 项目经理：管理团队任务和进度监控
- 团队负责人：分配和跟踪团队任务
- 团队成员：创建和更新个人任务
- 系统管理员：用户和系统管理

### 核心解决问题
- 分散的任务跟踪方法效率低下
- 缺乏实时进度更新和监控
- 缺少集中化的任务管理仪表板
- 权限管理和数据安全控制

## ✨ 功能特色

### 🔐 用户认证与权限管理
- ✅ 用户登录/登出系统
- 👥 三级角色权限控制（管理员/录入员/监督员）
- 🔒 基于角色的功能访问控制
- 🛡️ 任务创建者权限保护
- 📊 用户管理和状态控制

### 📝 任务管理功能
- ✅ 任务创建与编辑
- 📊 实时进度更新（0-100%）
- 📈 可视化进度展示
- 🔍 多条件任务筛选
- 🏷️ 任务分类管理
- 📅 计划时间管理
- 👤 负责人分配

### 🎨 界面与体验
- 🎨 现代化响应式界面设计
- 📱 移动端友好适配
- 🚀 实时表单验证
- 💫 流畅的交互动画
- 🌈 彩色进度条和状态指示
- ⚡ 快捷操作按钮

### 📊 数据统计
- 📈 任务统计仪表板
- 📊 进度可视化图表
- 🔢 实时数据更新
- 📋 任务状态分布

## 🛠️ 技术栈

### 后端技术
- **框架**: Python Flask 2.3.3
- **ORM**: Flask-SQLAlchemy 3.1.1
- **数据库**: SQLite
- **认证**: Flask-Login 0.6.3
- **表单**: Flask-WTF + WTForms
- **模板引擎**: Jinja2 3.1.2

### 前端技术
- **UI框架**: Bootstrap 5.3.0
- **图标**: Bootstrap Icons 1.10.0
- **JavaScript**: 原生ES6+
- **样式**: 自定义CSS + Bootstrap主题

### 开发工具
- **Python版本**: 3.7+
- **包管理**: pip
- **代码规范**: PEP8

## 🚀 安装与运行

### 环境要求
- Python 3.7 或更高版本
- pip 包管理器

### 安装步骤

1. **克隆项目**（如适用）
   ```bash
   git clone [项目地址]
   cd 任务进度情况
   ```

2. **安装Python依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用程序**
   ```bash
   python app.py
   ```

4. **访问应用**
   - 网站界面：http://localhost:5000
   - API接口：http://localhost:5000/api

### 初始账户信息

系统会自动创建以下默认账户：

| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 管理员 | admin | admin123 | 用户管理权限 |
| 录入员 | data_entry1 | 123456 | 任务创建编辑 |
| 监督员 | supervisor1 | 123456 | 任务查看监督 |

⚠️ **生产环境部署时请务必修改默认密码！**

## 👥 用户角色与权限

### 🔴 管理员 (Admin)
- ✅ 用户管理（创建、编辑、删除、重置密码）
- ✅ 任务分类管理
- ✅ 系统配置管理
- ❌ 不能操作任务（创建、编辑、删除）

### 🔵 录入员 (Data Entry)
- ✅ 创建新任务
- ✅ 编辑自己创建的任务
- ✅ 查看所有任务（只读）
- ❌ 不能编辑他人创建的任务
- ❌ 不能管理用户

### 🟢 监督员 (Supervisor)
- ✅ 查看所有任务
- ✅ 编辑所有任务
- ✅ 创建新任务
- ❌ 不能管理用户
- ❌ 不能删除任务（需要管理员权限）

## 📁 项目结构

```
任务进度情况/
├── app.py                    # Flask主应用程序和路由
├── models.py                 # 数据库模型定义
├── forms.py                  # 表单验证逻辑
├── auth_decorators.py        # 认证装饰器和权限控制
├── requirements.txt          # Python依赖包列表
├── README.md                 # 项目说明文档
├── task_progress.db          # SQLite数据库文件（自动生成）
├── templates/                # Jinja2 HTML模板
│   ├── base.html            # 基础模板布局
│   ├── index.html           # 仪表板首页
│   ├── login.html           # 用户登录页面
│   ├── tasks.html           # 任务列表页面
│   ├── add_task.html        # 添加任务表单
│   ├── edit_task.html       # 编辑任务表单
│   ├── 404.html             # 404错误页面
│   ├── 500.html             # 500错误页面
│   └── admin/               # 管理员模板目录
│       ├── users.html       # 用户管理页面
│       ├── add_user.html    # 添加用户表单
│       ├── edit_user.html   # 编辑用户表单
│       └── categories.html  # 分类管理页面
├── static/                   # 静态资源目录
│   ├── css/
│   │   └── style.css        # 自定义样式文件
│   └── js/
│       └── main.js          # JavaScript功能脚本
└── instance/                 # 实例配置目录（自动生成）
```

## 🔌 API接口文档

### 任务管理API

#### 获取任务列表
```http
GET /api/tasks
GET /api/tasks?status=pending
```
**响应示例**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "任务标题",
      "description": "任务描述",
      "status": "in-progress",
      "progress": 75,
      "category": "development",
      "assignee": "张三",
      "creator_id": 2,
      "planned_start_date": "2024-01-01",
      "planned_end_date": "2024-01-15",
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-10T15:30:00"
    }
  ],
  "count": 1
}
```

#### 创建新任务
```http
POST /api/tasks
Content-Type: application/json

{
  "title": "新任务",
  "description": "任务描述",
  "status": "pending",
  "progress": 0,
  "category": "general",
  "assignee": "负责人",
  "planned_start_date": "2024-01-01",
  "planned_end_date": "2024-01-15"
}
```

#### 更新任务
```http
PUT /api/tasks/<id>
Content-Type: application/json

{
  "title": "更新的任务标题",
  "progress": 50,
  "status": "in-progress"
}
```

#### 获取单个任务
```http
GET /api/tasks/<id>
```

### 认证要求
所有API接口都需要用户登录认证，需要有效的会话cookie。

## 📊 数据库模型

### 用户表 (User)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String(80) | 用户名（唯一） |
| email | String(120) | 邮箱（可选，唯一） |
| password_hash | String(128) | 密码哈希 |
| full_name | String(100) | 真实姓名 |
| role | String(20) | 用户角色 |
| is_active | Boolean | 账户状态 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 任务表 (Task)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| title | String(200) | 任务标题（必填） |
| description | Text | 任务描述（可选） |
| status | String(20) | 任务状态 |
| progress | Integer | 进度百分比（0-100） |
| category | String(50) | 任务分类 |
| assignee | String(100) | 负责人 |
| creator_id | Integer | 创建者ID（外键） |
| planned_start_date | Date | 计划开始日期 |
| planned_end_date | Date | 计划完成日期 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 任务分类表 (TaskCategory)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String(50) | 分类名称（英文键值） |
| display_name | String(100) | 显示名称（中文） |
| description | Text | 分类描述 |
| color | String(20) | 颜色样式 |
| is_active | Boolean | 启用状态 |
| sort_order | Integer | 排序顺序 |

## 🎯 主要功能详解

### 1. 用户认证系统
- **登录/登出**: 基于Flask-Login的会话管理
- **密码安全**: Werkzeug密码哈希加密
- **会话保护**: CSRF令牌防护
- **权限控制**: 装饰器实现的路由权限控制

### 2. 任务生命周期管理
- **创建阶段**: 表单验证、分类选择、时间规划
- **执行阶段**: 进度更新、状态变更、负责人管理
- **完成阶段**: 自动状态更新、完成时间记录
- **监控阶段**: 实时统计、进度可视化

### 3. 权限控制机制
- **路由级保护**: 装饰器控制页面访问
- **数据级权限**: 基于创建者ID的数据访问控制
- **UI级控制**: 模板中的条件渲染
- **API级保护**: 接口权限验证

### 4. 响应式界面设计
- **自适应布局**: Bootstrap栅格系统
- **移动端优化**: 触控友好的交互设计
- **进度可视化**: 彩色进度条和图表
- **实时反馈**: Ajax异步操作和即时验证

## 📱 界面功能说明

### 仪表板页面
- **统计概览**: 任务总数、完成率、状态分布
- **最近任务**: 最新创建和更新的任务
- **快速操作**: 直接跳转到常用功能
- **图表展示**: 直观的数据可视化

### 任务管理页面
- **列表视图**: 卡片式任务展示
- **筛选功能**: 按状态、分类、负责人筛选
- **搜索功能**: 关键词搜索任务
- **批量操作**: 选择多个任务进行操作

### 表单页面
- **智能验证**: 实时输入验证和错误提示
- **进度预览**: 实时显示设置的进度
- **日期选择**: 友好的日期选择器
- **自动保存**: 防止数据丢失的自动保存

## 🔧 配置说明

### 开发环境配置
```python
# app.py 中的开发配置
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_progress.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
```

### 生产环境配置
⚠️ **生产环境部署前必须修改的配置**:

1. **SECRET_KEY**: 使用强随机密钥
```python
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)
```

2. **数据库**: 考虑使用PostgreSQL或MySQL
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

3. **HTTPS**: 启用HTTPS和安全头
4. **错误日志**: 配置日志记录系统
5. **性能优化**: 启用缓存和压缩

## 🚨 安全考虑

### 认证安全
- ✅ 密码哈希存储（Werkzeug）
- ✅ 会话管理（Flask-Login）
- ✅ CSRF保护（Flask-WTF）
- ✅ SQL注入防护（SQLAlchemy ORM）
- ✅ XSS防护（Jinja2自动转义）

### 权限安全
- ✅ 基于角色的访问控制（RBAC）
- ✅ 任务所有权验证
- ✅ API接口权限验证
- ✅ 敏感操作确认机制

### 数据安全
- ✅ 输入验证和清理
- ✅ 数据库约束检查
- ✅ 错误信息过滤
- ✅ 日志记录（开发中）

## 🧪 测试说明

### 功能测试建议
1. **用户认证测试**
   - 登录/登出功能
   - 权限控制验证
   - 密码安全测试

2. **任务管理测试**
   - CRUD操作测试
   - 表单验证测试
   - 权限边界测试

3. **界面兼容性测试**
   - 不同浏览器测试
   - 移动端响应式测试
   - 性能压力测试

## 🐛 故障排除

### 常见问题

**Q: 启动时提示模块找不到**
A: 确保已安装所有依赖包：`pip install -r requirements.txt`

**Q: 数据库连接错误**
A: 检查SQLite数据库文件权限，确保应用有读写权限

**Q: 登录后页面空白**
A: 检查用户角色配置，确保角色名称正确

**Q: 静态文件加载失败**
A: 确认static目录结构完整，检查文件路径

### 调试模式
开发时启用调试模式获取详细错误信息：
```python
if __name__ == '__main__':
    app.run(debug=True)
```

## 🔄 版本更新

### 当前版本功能
- ✅ 用户认证和权限管理
- ✅ 任务CRUD操作
- ✅ 进度跟踪和可视化
- ✅ 响应式界面设计
- ✅ API接口支持

### 计划功能（Future Roadmap）
- 📧 邮件通知系统
- 📂 文件附件支持
- 🌐 多语言国际化
- 📊 高级报表系统
- 🔗 第三方集成（钉钉、企业微信）
- 🗂️ 项目分组管理

## 🤝 贡献指南

### 代码规范
- 遵循PEP8 Python编码规范
- 使用有意义的变量和函数命名
- 添加充分的中文注释
- 保持代码简洁和可读性

### 提交规范
- 使用清晰的提交信息
- 单次提交包含单一功能
- 测试后再提交代码

## 📄 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 📞 技术支持

如有问题或建议，请通过以下方式联系：
- 创建 Issue 报告问题
- 提交 Pull Request 贡献代码
- 发送邮件至技术支持邮箱

---

**任务进度管理系统** - 基于Flask框架的现代化任务管理解决方案

🔗 **相关链接**
- [Flask官方文档](https://flask.palletsprojects.com/)
- [Bootstrap官方文档](https://getbootstrap.com/)
- [SQLAlchemy文档](https://www.sqlalchemy.org/)

📅 **最后更新**: 2024年1月