// JWT 驗證與自動登入功能

// 檢查 JWT 是否有效（簡單檢查格式與過期時間）
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

// 自動登入功能
function autoLogin() {
    const token = localStorage.getItem('jwt');
    if (isJwtValid(token)) {
        // 這裡可根據需求自動導向主頁或顯示已登入狀態
        document.body.classList.add('logged-in');
    } else {
        localStorage.removeItem('jwt');
    }
}

document.addEventListener('DOMContentLoaded', autoLogin);
