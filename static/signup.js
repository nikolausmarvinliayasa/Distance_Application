const form = document.getElementById('signupForm');
const name = document.getElementById('name');
const email = document.getElementById('email');
const password = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');
const themeToggle = document.getElementById('toggle-theme');

form.addEventListener('submit', function (e) {
  // Validasi input secara client-side
  let valid = true;

  [name, email, password].forEach(input => input.classList.remove('error'));

  if (!name.value.trim()) {
    name.classList.add('error');
    valid = false;
  }

  if (!email.value.includes('@')) {
    email.classList.add('error');
    valid = false;
  }

  if (!password.value.trim()) {
    password.classList.add('error');
    valid = false;
  }

  if (!valid) {
    e.preventDefault(); // cegah hanya jika tidak valid
  }

  // Jika valid, biarkan submit dilakukan ke Flask (tidak ada redirect manual!)
});

// Toggle show/hide password
togglePassword.addEventListener('click', () => {
  const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
  password.setAttribute('type', type);
  togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
});

// Dark/Light mode toggle
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  themeToggle.textContent = document.body.classList.contains('dark') ? '🌞' : '🌙';
});
