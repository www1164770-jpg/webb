<template>
  <nav class="navbar">
    <div class="navbar-container">
      <h1 class="navbar-title">网址导航</h1>
      <div class="navbar-links">
        <a href="#" class="navbar-link">首页</a>
        <a href="#" class="navbar-link">管理</a>
        <div v-if="!isLoggedIn" class="navbar-auth">
          <button class="navbar-button" @click="showLoginModal = true">登录</button>
          <button class="navbar-button navbar-button-secondary" @click="showRegisterModal = true">注册</button>
        </div>
        <div v-else class="navbar-user">
          <span class="navbar-username">{{ user.username }}</span>
          <button class="navbar-button navbar-button-secondary" @click="logout">退出</button>
        </div>
      </div>
    </div>

    <!-- 登录模态框 -->
    <div v-if="showLoginModal" class="modal-overlay" @click="showLoginModal = false">
      <div class="modal-content" @click.stop>
        <h2>登录</h2>
        <form @submit.prevent="login">
          <div class="form-group">
            <label for="username">用户名</label>
            <input type="text" id="username" v-model="loginForm.username" required>
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input type="password" id="password" v-model="loginForm.password" required>
          </div>
          <button type="submit" class="form-button">登录</button>
        </form>
        <div class="login-divider">或使用以下方式登录</div>
        <div class="login-buttons">
          <button class="login-button wechat" @click="wechatLogin">微信登录</button>
          <button class="login-button qq" @click="qqLogin">QQ登录</button>
          <button class="login-button phone" @click="phoneLogin">手机号登录</button>
          <button class="login-button github" @click="githubLogin">GitHub登录</button>
        </div>
        <div class="login-divider">或</div>
        <button class="login-button guest" @click="guestLogin">游客登录</button>
        <button class="modal-close" @click="showLoginModal = false">×</button>
      </div>
    </div>

    <!-- 注册模态框 -->
    <div v-if="showRegisterModal" class="modal-overlay" @click="showRegisterModal = false">
      <div class="modal-content" @click.stop>
        <h2>注册</h2>
        <form @submit.prevent="register">
          <div class="form-group">
            <label for="reg-username">用户名</label>
            <input type="text" id="reg-username" v-model="registerForm.username" required>
          </div>
          <div class="form-group">
            <label for="reg-password">密码</label>
            <input type="password" id="reg-password" v-model="registerForm.password" required>
          </div>
          <div class="form-group">
            <label for="reg-email">邮箱</label>
            <input type="email" id="reg-email" v-model="registerForm.email" required>
          </div>
          <button type="submit" class="form-button">注册</button>
        </form>
        <button class="modal-close" @click="showRegisterModal = false">×</button>
      </div>
    </div>

    <!-- 手机号登录模态框 -->
    <div v-if="showPhoneLoginModal" class="modal-overlay" @click="showPhoneLoginModal = false">
      <div class="modal-content" @click.stop>
        <h2>手机号登录</h2>
        <form @submit.prevent="submitPhoneLogin">
          <div class="form-group">
            <label for="phone-number">手机号</label>
            <input type="tel" id="phone-number" v-model="phoneLoginForm.phone_number" required>
          </div>
          <div class="form-group">
            <label for="phone-code">验证码</label>
            <div class="code-input">
              <input type="text" id="phone-code" v-model="phoneLoginForm.code" required>
              <button type="button" class="code-button">获取验证码</button>
            </div>
          </div>
          <button type="submit" class="form-button">登录</button>
        </form>
        <button class="modal-close" @click="showPhoneLoginModal = false">×</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 状态管理
const isLoggedIn = ref(false)
const user = ref({ username: '' })
const showLoginModal = ref(false)
const showRegisterModal = ref(false)

// 登录表单
const loginForm = ref({
  username: '',
  password: ''
})

// 注册表单
const registerForm = ref({
  username: '',
  password: '',
  email: ''
})

// 检查登录状态
onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    checkLoginStatus()
  }
})

// 检查登录状态
const checkLoginStatus = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://localhost:5000/api/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    user.value = response.data
    isLoggedIn.value = true
  } catch (error) {
    localStorage.removeItem('token')
    isLoggedIn.value = false
  }
}

// 登录
const login = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/login', loginForm.value)
    localStorage.setItem('token', response.data.token)
    user.value = { username: response.data.username }
    isLoggedIn.value = true
    showLoginModal.value = false
  } catch (error) {
    alert('登录失败，请检查用户名和密码')
  }
}

// 注册
const register = async () => {
  try {
    await axios.post('http://localhost:5000/api/register', registerForm.value)
    alert('注册成功，请登录')
    showRegisterModal.value = false
    showLoginModal.value = true
  } catch (error) {
    alert('注册失败，请检查输入信息')
  }
}

// 退出登录
const logout = () => {
  localStorage.removeItem('token')
  isLoggedIn.value = false
  user.value = { username: '' }
}

// 微信登录
const wechatLogin = async () => {
  try {
    // 这里需要替换为真实的微信登录逻辑
    // 例如使用微信JS-SDK或跳转微信授权页面
    // 这里简化处理，模拟微信登录
    const response = await axios.post('http://localhost:5000/api/login/wechat', {
      code: 'mock-wechat-code'
    })
    localStorage.setItem('token', response.data.token)
    user.value = { username: response.data.username }
    isLoggedIn.value = true
    showLoginModal.value = false
  } catch (error) {
    alert('微信登录失败，请稍后重试')
  }
}

// QQ登录
const qqLogin = async () => {
  try {
    // 这里需要替换为真实的QQ登录逻辑
    // 例如跳转QQ授权页面
    // 这里简化处理，模拟QQ登录
    const response = await axios.post('http://localhost:5000/api/login/qq', {
      code: 'mock-qq-code'
    })
    localStorage.setItem('token', response.data.token)
    user.value = { username: response.data.username }
    isLoggedIn.value = true
    showLoginModal.value = false
  } catch (error) {
    alert('QQ登录失败，请稍后重试')
  }
}

// 手机号登录
const showPhoneLoginModal = ref(false)
const phoneLoginForm = ref({
  phone_number: '',
  code: ''
})

const phoneLogin = () => {
  showPhoneLoginModal.value = true
}

const submitPhoneLogin = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/login/phone', phoneLoginForm.value)
    localStorage.setItem('token', response.data.token)
    user.value = { username: response.data.username }
    isLoggedIn.value = true
    showPhoneLoginModal.value = false
    showLoginModal.value = false
  } catch (error) {
    alert('手机号登录失败，请稍后重试')
  }
}

// GitHub登录
const githubLogin = async () => {
  try {
    // 这里需要替换为真实的GitHub登录逻辑
    // 例如跳转GitHub授权页面
    // 这里简化处理，模拟GitHub登录
    const response = await axios.post('http://localhost:5000/api/login/github', {
      code: 'mock-github-code'
    })
    localStorage.setItem('token', response.data.token)
    user.value = { username: response.data.username }
    isLoggedIn.value = true
    showLoginModal.value = false
  } catch (error) {
    alert('GitHub登录失败，请稍后重试')
  }
}

// 游客登录
const guestLogin = () => {
  // 游客登录不需要调用后端API
  // 只需要在前端设置游客状态
  localStorage.removeItem('token')
  user.value = { username: '游客' }
  isLoggedIn.value = true
  showLoginModal.value = false
}
</script>

<style scoped>
.navbar {
  background-color: #333;
  color: white;
  padding: 10px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.navbar-link {
  color: white;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.navbar-auth {
  display: flex;
  gap: 10px;
}

.navbar-user {
  display: flex;
  gap: 10px;
  align-items: center;
}

.navbar-username {
  font-weight: bold;
}

.navbar-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.navbar-button:hover {
  background-color: #45a049;
}

.navbar-button-secondary {
  background-color: #666;
}

.navbar-button-secondary:hover {
  background-color: #555;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  position: relative;
}

.modal-content h2 {
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.form-button:hover {
  background-color: #45a049;
}

.code-input {
  display: flex;
  gap: 10px;
}

.code-input input {
  flex: 1;
}

.code-button {
  background-color: #666;
  color: white;
  border: none;
  padding: 0 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.code-button:hover {
  background-color: #555;
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-close:hover {
  color: #333;
}

/* 登录分割线 */
.login-divider {
  text-align: center;
  margin: 20px 0;
  color: #999;
  position: relative;
}

.login-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #ddd;
  z-index: 1;
}

.login-divider::after {
  content: '或使用以下方式登录';
  position: relative;
  background-color: white;
  padding: 0 10px;
  z-index: 2;
}

/* 登录按钮 */
.login-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 20px;
}

.login-button {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.login-button:hover {
  background-color: #f5f5f5;
}

.login-button.wechat {
  color: #07C160;
  border-color: #07C160;
}

.login-button.qq {
  color: #12B7F5;
  border-color: #12B7F5;
}

.login-button.phone {
  color: #FF6B6B;
  border-color: #FF6B6B;
}

.login-button.github {
  color: #333;
  border-color: #333;
}

.login-button.guest {
  color: #666;
  border-color: #666;
  margin-top: 10px;
  width: 100%;
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 10px;
  }
  
  .navbar-links {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .login-buttons {
    grid-template-columns: 1fr;
  }
}
</style>
