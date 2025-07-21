// JWT 驗證與自動登入功能

// 儲存使用者資訊
let currentUser = null;

// 檢查 JWT 是否有效（檢查格式與過期時間）
function isJwtValid(token) {
    if (!token) return false;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (!payload.exp) return false;
        const now = Math.floor(Date.now() / 1000);
        return payload.exp > now;
    } catch (e) {
        return false;
    }
}

// 取得 JWT payload
function getJwtPayload(token) {
    if (!token) return null;
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return null;
    }
}

// 取得目前使用者資訊
async function getCurrentUser() {
    const token = localStorage.getItem('jwt');
    if (!isJwtValid(token)) {
        return null;
    }

    try {
        const response = await fetch('/api/auth/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            currentUser = data.user;
            return currentUser;
        } else {
            // Token 無效，清除本地儲存
            localStorage.removeItem('jwt');
            currentUser = null;
            return null;
        }
    } catch (error) {
        console.error('取得使用者資訊失敗:', error);
        return null;
    }
}

// 登出功能
function logout() {
    localStorage.removeItem('jwt');
    currentUser = null;
    document.body.classList.remove('logged-in');
    
    // 如果在需要登入的頁面，重導向到登入頁
    const currentPage = window.location.pathname;
    if (currentPage !== '/login.html' && currentPage !== '/register.html' && currentPage !== '/index.html') {
        window.location.href = 'login.html';
    }
}

// 更新 UI 顯示登入狀態
function updateLoginStatus() {
    const token = localStorage.getItem('jwt');
    const isLoggedIn = isJwtValid(token);
    
    if (isLoggedIn) {
        document.body.classList.add('logged-in');
        
        // 顯示使用者資訊
        if (currentUser) {
            updateUserInfo();
        }
    } else {
        document.body.classList.remove('logged-in');
        currentUser = null;
    }
}

// 更新頁面上的使用者資訊
function updateUserInfo() {
    if (!currentUser) return;
    
    // 尋找並更新使用者名稱顯示元素
    const userNameElements = document.querySelectorAll('.user-name');
    userNameElements.forEach(element => {
        element.textContent = currentUser.name || currentUser.email;
    });
    
    // 尋找並更新使用者 email 顯示元素
    const userEmailElements = document.querySelectorAll('.user-email');
    userEmailElements.forEach(element => {
        element.textContent = currentUser.email;
    });
}

// 自動登入功能
async function autoLogin() {
    const token = localStorage.getItem('jwt');
    
    if (isJwtValid(token)) {
        // 取得使用者資訊
        await getCurrentUser();
        updateLoginStatus();
        
        // 如果在登入或註冊頁面且已登入，導向主頁
        const currentPage = window.location.pathname;
        if (currentPage.includes('login.html') || currentPage.includes('register.html')) {
            console.log('已登入，重導向到主頁...');
            // 可選：自動重導向到主頁
            // window.location.href = 'index.html';
        }
    } else {
        // Token 無效或不存在
        localStorage.removeItem('jwt');
        updateLoginStatus();
    }
}

// 頁面載入完成後執行自動登入
document.addEventListener('DOMContentLoaded', autoLogin);

// 提供全域函數供其他檔案使用
window.jwtUtils = {
    isJwtValid,
    getJwtPayload,
    getCurrentUser,
    logout,
    updateLoginStatus,
    autoLogin
};
