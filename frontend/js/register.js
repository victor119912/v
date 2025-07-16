document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const msgDiv = document.getElementById('registerMsg');
    msgDiv.textContent = '';

    // 前端驗證
    if (!email.match(/^[^@\s]+@[^@\s]+\.[^@\s]+$/)) {
        msgDiv.textContent = '請輸入正確的 Email 格式';
        msgDiv.style.color = 'red';
        return;
    }
    if (password.length < 6) {
        msgDiv.textContent = '密碼長度至少 6 碼';
        msgDiv.style.color = 'red';
        return;
    }

    try {
        const res = await fetch('/api/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (res.ok) {
            msgDiv.textContent = '註冊成功，請前往登入';
            msgDiv.style.color = 'green';
        } else {
            msgDiv.textContent = data.message || '註冊失敗';
            msgDiv.style.color = 'red';
        }
    } catch (err) {
        msgDiv.textContent = '伺服器錯誤，請稍後再試';
        msgDiv.style.color = 'red';
    }
});
