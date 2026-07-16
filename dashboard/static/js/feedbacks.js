document.addEventListener('DOMContentLoaded', function () {
    var feedbackDetailModal = document.getElementById('feedbackDetailModal');
    feedbackDetailModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var feedbackId = button.getAttribute('data-feedback-id');
        var feedbackName = button.getAttribute('data-feedback-name');
        var feedbackEmail = button.getAttribute('data-feedback-email');
        var feedbackDescription = button.getAttribute('data-feedback-description');
        var feedbackPicture = button.getAttribute('data-feedback-picture');
        var feedbackIsApproved = button.getAttribute('data-feedback-is-approved');
        var feedbackCreatedAt = button.getAttribute('data-feedback-created-at');

        var modalFeedbackPicture = feedbackDetailModal.querySelector('#modalFeedbackPicture');
        var modalFeedbackName = feedbackDetailModal.querySelector('#modalFeedbackName');
        var modalFeedbackEmail = feedbackDetailModal.querySelector('#modalFeedbackEmail');
        var modalFeedbackDescription = feedbackDetailModal.querySelector('#modalFeedbackDescription');
        var modalFeedbackStatus = feedbackDetailModal.querySelector('#modalFeedbackStatus');
        var modalFeedbackCreatedAt = feedbackDetailModal.querySelector('#modalFeedbackCreatedAt');
        

        if (feedbackPicture && feedbackPicture !== 'https://placehold.co/400') {
            modalFeedbackPicture.src = feedbackPicture;
            
        } else {
            modalFeedbackPicture.src = 'https://placehold.co/400';
            
        }

        modalFeedbackName.textContent = feedbackName;
        modalFeedbackEmail.textContent = feedbackEmail;
        modalFeedbackDescription.textContent = feedbackDescription;
        modalFeedbackCreatedAt.textContent = feedbackCreatedAt;

        if (feedbackIsApproved === 'true') {
            modalFeedbackStatus.innerHTML = '<span class="badge badge-success">تمت الموافقة</span>';
        } else {
            modalFeedbackStatus.innerHTML = '<span class="badge bg-danger">قيد الانتظار</span>';
        }
    });

    // Handle approve button click
    document.querySelectorAll('.approve-btn').forEach(button => {
        button.addEventListener('click', function () {
            const approveUrl = this.dataset.approveUrl;
            const csrfToken = this.dataset.csrf;

            fetch(approveUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert(data.errors.join('\n'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء الموافقة على التقييم.');
            });
        });
    });

    // Handle delete modal
    var deleteModal = document.getElementById('deleteModal');
    deleteModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var deleteUrl = button.getAttribute('data-delete-url');
        var csrfToken = button.getAttribute('data-csrf');
        var deleteForm = deleteModal.querySelector('#deleteForm');
        deleteForm.action = deleteUrl;
        deleteForm.querySelector('input[name="csrfmiddlewaretoken"]').value = csrfToken;
    });
});
