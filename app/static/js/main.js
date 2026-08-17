// Adds a spinner + disables the button on submit for any form with
// class "loading-form", giving the "Loading Buttons" UX requirement.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('form.loading-form').forEach(function (form) {
    form.addEventListener('submit', function () {
      const btn = form.querySelector('button[type="submit"]');
      if (btn && !btn.disabled) {
        btn.dataset.originalText = btn.innerHTML;
        btn.disabled = true;
        btn.classList.add('btn-loading');
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Please wait...';
      }
    });
  });

  // Bootstrap client-side validation styling
  const forms = document.querySelectorAll('.needs-validation');
  Array.from(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
});
