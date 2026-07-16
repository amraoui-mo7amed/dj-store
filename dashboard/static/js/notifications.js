document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    const userId = sidebar.dataset.userId;
    if (!userId) return;

    const notifList = document.querySelector('.notif-list');
    const notifBadge = document.querySelector('.notif-badge');
    const notifCount = document.querySelector('.notif-count');

    const updateBadge = () => {
        const unread = notifList.querySelectorAll('.notif-item.unread').length;
        if (notifBadge) {
            notifBadge.textContent = unread;
            notifBadge.style.display = unread > 0 ? '' : 'none';
        }
        if (notifCount) {
            notifCount.textContent = `${unread} جديد`;
        }
    };

    const showToast = (data) => {
        if (typeof Swal === 'undefined') return;
        Swal.fire({
            toast: true,
            position: 'top-start',
            iconHtml: `<i class="${data.icon}" style="color: var(--coral-500); font-size: 1.2rem;"></i>`,
            title: data.message,
            showConfirmButton: false,
            timer: 5000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.addEventListener('click', () => {
                    if (data.url) window.location.href = data.url;
                });
            }
        });
    };

    const renderItem = (data) => {
        const emptyItem = notifList.querySelector('.notif-empty');
        if (emptyItem) emptyItem.remove();

        let inner = `<div class="notif-icon"><i class="${data.icon}"></i></div>
                     <div><p class="mb-0 small">${data.message}</p>`;
        if (data.url) {
            inner += `<a href="${data.url}" class="small" style="color: var(--coral-500); font-weight: 600;">عرض التفاصيل</a>`;
        } else {
            inner += `<span class="small" style="opacity:0.5;">${data.created_at || 'الآن'}</span>`;
        }
        inner += '</div>';

        const item = document.createElement('li');
        item.className = 'notif-item unread';
        item.innerHTML = inner;
        notifList.prepend(item);
        updateBadge();
    };

    const es = new EventSource(`/dashboard/sse/?channel=user:${userId}`);

    es.addEventListener('notification', (e) => {
        const data = JSON.parse(e.data);
        showToast(data);
        renderItem(data);
    });

    es.onerror = () => {};

    const fetchUnread = async () => {
        try {
            const res = await fetch(`/dashboard/api/notifications/unread/${userId}/`);
            const data = await res.json();
            if (!data.success) return;

            notifList.innerHTML = '';
            if (data.notifications.length === 0) {
                notifList.innerHTML = '<li class="notif-item notif-empty"><span>لا توجد إشعارات جديدة</span></li>';
            } else {
                data.notifications.forEach(n => renderItem(n));
            }
            updateBadge();
        } catch (err) {
            console.error('Fetch error:', err);
        }
    };

    const markAllRead = async () => {
        try {
            const res = await fetch(`/dashboard/api/notifications/mark-all-read/${userId}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });
            const data = await res.json();
            if (data.success) {
                notifList.querySelectorAll('.notif-item.unread').forEach(i => i.classList.remove('unread'));
                updateBadge();
            }
        } catch (err) {
            console.error('Mark read error:', err);
        }
    };

    function getCookie(name) {
        let value = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(c => {
                const trimmed = c.trim();
                if (trimmed.startsWith(name + '=')) value = decodeURIComponent(trimmed.substring(name.length + 1));
            });
        }
        return value;
    }

    fetchUnread();
    document.getElementById('mark-all-read-btn')?.addEventListener('click', e => {
        e.preventDefault();
        markAllRead();
    });
});
