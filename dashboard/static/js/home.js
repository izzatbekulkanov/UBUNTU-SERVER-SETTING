function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return null;
}

document.getElementById('updateButton').addEventListener('click', function () {
    const progressBarContainer = document.getElementById('progressBarContainer');
    const progressBar = document.getElementById('progressBar');
    const logTableBody = document.getElementById('logTableBody');

    progressBarContainer.classList.remove('d-none');
    progressBar.style.width = '0%';
    progressBar.textContent = '0%';

    axios.post('/update/', {}, {
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    }).then(() => {
        const interval = setInterval(() => {
            axios.get('/update-status/').then(res => {
                const progress = res.data.progress;
                progressBar.style.width = `${progress}%`;
                progressBar.textContent = `${progress}%`;

                if (progress >= 100) {
                    clearInterval(interval);
                    progressBarContainer.classList.add('d-none');
                    loadLogs();
                    showToast('Yangilash muvaffaqiyatli yakunlandi!');
                }
            }).catch(() => {
                clearInterval(interval);
                showToast('Yangilash jarayonida xatolik yuz berdi!', true);
            });
        }, 2000);
    }).catch(() => {
        showToast('Yangilashni boshlashda xatolik yuz berdi!', true);
    });
});

function loadLogs() {
    axios.get('/get-logs/').then(res => {
        const logs = res.data.logs;
        const logTableBody = document.getElementById('logTableBody');
        logTableBody.innerHTML = '';
        logs.forEach((log, index) => {
            logTableBody.innerHTML += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${log.timestamp}</td>
                    <td>${log.status}</td>
                </tr>
            `;
        });
    });
}

function showToast(message, isError = false) {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${isError ? 'danger' : 'success'} border-0 position-fixed bottom-0 end-0 m-3`;
    toast.style.minWidth = '250px';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Yopish"></button>
        </div>
    `;
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    setTimeout(() => toast.remove(), 5000);
}

const matrixContainer = document.querySelector('.matrix');
const createMatrixEffect = () => {
    const span = document.createElement('span');
    span.textContent = Math.random() > 0.5 ? '0' : '1';
    span.style.left = `${Math.random() * 100}vw`;
    span.style.animationDuration = `${Math.random() * 2 + 1}s`;
    matrixContainer.appendChild(span);
    setTimeout(() => span.remove(), 3000);
};
setInterval(createMatrixEffect, 100);