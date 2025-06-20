const form = document.getElementById('loginForm');
const email = document.getElementById('email');
const password = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');
const themeToggle = document.getElementById('toggle-theme');

// Validasi
form.addEventListener('submit', function (e) {
  let valid = true;

  // Reset error class
  [email, password].forEach(input => input.classList.remove('error'));

  if (!email.value || !email.value.includes('@')) {
    email.classList.add('error');
    valid = false;
  }

  if (!password.value) {
    password.classList.add('error');
    valid = false;
  }

  if (!valid) {
    e.preventDefault();
  }
});

// Toggle show/hide password
togglePassword.addEventListener('click', () => {
  const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
  password.setAttribute('type', type);
  togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
});

// Dark/Light mode
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  themeToggle.textContent = document.body.classList.contains('dark') ? '🌞' : '🌙';
});
