document.addEventListener('DOMContentLoaded', function() {
    const orderDetailsModal = new bootstrap.Modal(document.getElementById('orderDetailsModal'));
    const customerName = document.getElementById('customerName');
    const customerPhone = document.getElementById('customerPhone');
    const customerAddress = document.getElementById('customerAddress');
    const customerWilaya = document.getElementById('customerWilaya');
    const customerCommune = document.getElementById('customerCommune');
    const productName = document.getElementById('productName');
    const productQuantity = document.getElementById('productQuantity');
    const productPrice = document.getElementById('productPrice');
    const productSize = document.getElementById('productSize');
    const productColor = document.getElementById('productColor');
    const orderStatus = document.getElementById('orderStatus');
    const orderDate = document.getElementById('orderDate');
    const orderIdSpan = document.getElementById('orderId');
    console.log("fetching details");
    

    document.querySelectorAll('.view-order-btn').forEach(button => {
        button.addEventListener('click', function() {
            const orderId = this.dataset.orderId;
            orderIdSpan.textContent = orderId;

            fetch(`/dashboard/get_order_details/${orderId}/`)
                .then(response => response.json())
                .then(data => {
                    customerName.textContent = data.name;
                    customerPhone.textContent = data.phone;
                    customerAddress.textContent = data.address;
                    customerWilaya.textContent = data.wilaya;
                    customerCommune.textContent = data.commune;
                    productName.textContent = data.product_name;
                    productQuantity.textContent = data.quantity;
                    productPrice.textContent = data.price;
                    productSize.textContent = data.selected_size || 'N/A';
                    productColor.textContent = data.selected_color || 'N/A';
                    orderStatus.textContent = data.status_display;
                    orderDate.textContent = new Date(data.created_at).toLocaleDateString();

                    orderDetailsModal.show();
                })
                .catch(error => {
                    console.error('Error fetching order details:', error);
                    alert('Failed to load order details.');
                });
        });
    });

    document.querySelectorAll('.order-status-select').forEach(selectElement => {
        selectElement.addEventListener('change', function() {
            const orderId = this.dataset.orderId;
            const newStatus = this.value;

            fetch(`/dashboard/update_order_status/${orderId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ status: newStatus })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'تم التحديث',
                        text: 'تم تحديث حالة الطلبية بنجاح!',
                        confirmButtonText: 'حسناً'
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'خطأ',
                        text: 'فشل في تحديث حالة الطلبية: ' + data.error,
                        confirmButtonText: 'حسناً'
                    });
                }
            })
            .catch(error => {
                console.error('Error updating order status:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'خطأ',
                    text: 'فشل في تحديث حالة الطلبية.',
                    confirmButtonText: 'حسناً'
                });
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
