const form = document.getElementById('resetForm');
const newPassword = document.getElementById('newPassword');
const confirmPassword = document.getElementById('confirmPassword');
const messageBox = document.getElementById('messageBox');
const themeToggle = document.getElementById('toggle-theme');

form.addEventListener('submit', function (e) {
  e.preventDefault();

  newPassword.classList.remove('error');
  confirmPassword.classList.remove('error');

  if (!newPassword.value || !confirmPassword.value) {
    messageBox.textContent = 'Please fill in both fields.';
    messageBox.style.color = '#e53935';
    newPassword.classList.add('error');
    confirmPassword.classList.add('error');
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    messageBox.textContent = 'Passwords do not match.';
    messageBox.style.color = '#e53935';
    confirmPassword.classList.add('error');
    return;
  }

  // Tampilkan pesan sukses
  messageBox.textContent = 'Your password has been successfully updated.';
  messageBox.style.color = '#2e7d32';

  // Bersihkan input
  newPassword.value = '';
  confirmPassword.value = '';

  // Redirect ke login.html setelah 2 detik
  setTimeout(() => {
    window.location.href = "/login";
  }, 2000); 
});

// Toggle Dark/Light Mode
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  themeToggle.textContent = document.body.classList.contains('dark') ? '🌞' : '🌙';
});

