document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('id_avatar');
  if (!input) return;

  input.addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (ev) => {
      const preview = document.getElementById('avatarPreview');
      const placeholder = document.getElementById('avatarPlaceholder');
      preview.src = ev.target.result;
      preview.classList.remove('d-none');
      if (placeholder) placeholder.classList.add('d-none');
    };
    reader.readAsDataURL(file);
  });
});
