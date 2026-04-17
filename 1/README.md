# 我的导航

一个简洁的网址导航页面，支持分类浏览、搜索、添加和删除网站。

## 快速开始

### 第一步：安装环境（只需做一次）

**1. 安装 Python**
- 下载地址：https://www.python.org/downloads/
- 安装时务必勾选 **"Add Python to PATH"**

**2. 安装 MySQL**
- 下载地址：https://dev.mysql.com/downloads/installer/
- 安装过程中设置 root 用户密码并记住它

### 第二步：启动项目

双击根目录下的 **`启动.bat`**，按照提示输入 MySQL 密码，浏览器会自动打开。

访问地址：http://localhost:5000

> 注意：关闭启动窗口会停止服务。

---

## 常见问题

**Q: 提示"未检测到 Python"**  
重新安装 Python，安装时勾选"Add Python to PATH"，然后重启电脑。

**Q: 提示"数据库连接失败"**  
- 检查 MySQL 服务是否启动：按 `Win+R` 输入 `services.msc`，找到 MySQL 并启动
- 检查密码是否正确

**Q: 浏览器打开后显示"无法访问"**  
等待几秒后刷新，服务启动需要一点时间。

**Q: 端口被占用**  
在 cmd 中运行 `taskkill /IM python.exe /F`，然后重新双击启动。

---

## 技术栈

- 后端：Flask + SQLAlchemy + MySQL
- 前端：Vue 3 + Axios
