document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const msgDiv = document.getElementById('loginMsg');
    const submitButton = document.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    
    // 清除之前的訊息
    msgDiv.textContent = '';
    msgDiv.className = '';

    // 前端驗證
    if (!email.match(/^[^@\s]+@[^@\s]+\.[^@\s]+$/)) {
        showMessage('請輸入正確的 Email 格式', 'error');
        return;
    }
    if (password.length < 6) {
        showMessage('密碼長度至少 6 碼', 'error');
        return;
    }

    // 顯示 loading 狀態
    setLoading(true);

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok && data.token) {
            // 儲存 JWT token
            localStorage.setItem('jwt', data.token);
            
            // 驗證 token 是否有效
            if (window.jwtUtils && !window.jwtUtils.isJwtValid(data.token)) {
                showMessage('Token 無效，請重新登入', 'error');
                localStorage.removeItem('jwt');
                return;
            }
            
            showMessage('登入成功，正在跳轉...', 'success');
            
            // 更新登入狀態
            if (window.jwtUtils) {
                await window.jwtUtils.getCurrentUser();
                window.jwtUtils.updateLoginStatus();
            }
            
            // 延遲跳轉到主頁
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1500);
            
        } else {
            // 顯示錯誤訊息
            const errorMessage = data.message || '登入失敗，請檢查您的帳號密碼';
            showMessage(errorMessage, 'error');
        }
        
    } catch (error) {
        console.error('登入請求失敗:', error);
        showMessage('網路連線錯誤，請稍後再試', 'error');
    } finally {
        setLoading(false);
    }

    // 顯示訊息的輔助函數
    function showMessage(message, type) {
        msgDiv.textContent = message;
        msgDiv.className = `message ${type}`;
        
        // 舊版相容性
        if (type === 'error') {
            msgDiv.style.color = 'red';
        } else if (type === 'success') {
            msgDiv.style.color = 'green';
        }
    }

    // 設定 loading 狀態的輔助函數
    function setLoading(isLoading) {
        if (isLoading) {
            submitButton.textContent = '登入中...';
            submitButton.disabled = true;
            document.getElementById('email').disabled = true;
            document.getElementById('password').disabled = true;
        } else {
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
            document.getElementById('email').disabled = false;
            document.getElementById('password').disabled = false;
        }
    }
});
