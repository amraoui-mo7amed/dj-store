document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.querySelector('.sidebar');
  const toggleBtn = document.querySelector('.sidebar-toggle');
  const backdrop = document.getElementById('dashBackdrop');

  function closeSidebar() {
    sidebar?.classList.add('hidden');
    backdrop?.classList.remove('show');
  }
  function openSidebar() {
    sidebar?.classList.remove('hidden');
    backdrop?.classList.add('show');
  }

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      if (sidebar.classList.contains('hidden')) {
        openSidebar();
      } else {
        closeSidebar();
      }
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', closeSidebar);
  }

  document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 992) closeSidebar();
    });
  });

  document.querySelectorAll(".delete_button").forEach(button => {
    button.addEventListener("click", () => {
      const deleteUrl = button.dataset.deleteUrl;
      const csrfToken = button.dataset.csrfToken;

      Swal.fire({
        title: "هل أنت متأكد؟",
        text: "لن تتمكن من التراجع عن هذا!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "نعم، احذف",
        cancelButtonText: "إلغاء",
        buttonsStyling: false,
        customClass: {
          confirmButton: "btn btn-danger mx-2",
          cancelButton: "btn btn-secondary"
        }
      }).then((result) => {
        if (result.isConfirmed) {
          fetch(deleteUrl, {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfToken,
              "X-Requested-With": "XMLHttpRequest",
              "Content-Type": "application/json"
            },
            body: JSON.stringify({})
          })
            .then(response => response.json())
            .then(data => {
              Swal.fire({
                title: data.message || "تم تنفيذ العملية",
                icon: data.success ? "success" : "error"
              }).then(() => {
                if (data.success) {
                  location.reload();
                }
              });
            })
            .catch(() => {
              Swal.fire({
                title: "حدث خطأ في الاتصال بالخادم",
                icon: "error"
              });
            });
        }
      });
    });
  });

  function setActiveNavLink() {
    const links = document.querySelectorAll(".sidebar-link");
    const currentUrl = window.location.pathname;

    links.forEach(link => {
      link.classList.remove("active");
      if (link.getAttribute("href") === currentUrl) {
        link.classList.add("active");
      }
    });
  }

  setActiveNavLink();

});


// Filtering table via data attributes
document.addEventListener('input', function(e) {
    var input = e.target.closest('[data-table-id]');
    if (input) {
        filterTable(input.dataset.tableId, input.value);
    }
});

function filterTable(tableId, query) {
  const container = document.getElementById(tableId);
  if (!container) return;

  const filter = query.toLowerCase();
  const rows = container.querySelectorAll('tbody tr');
  const cards = container.querySelectorAll('.col-12');

  if (rows.length) {
    rows.forEach(row => {
      row.style.display = filter === '' || row.innerText.toLowerCase().includes(filter) ? '' : 'none';
    });
  } else if (cards.length) {
    cards.forEach(col => {
      col.style.display = filter === '' || col.innerText.toLowerCase().includes(filter) ? '' : 'none';
    });
  }
}
