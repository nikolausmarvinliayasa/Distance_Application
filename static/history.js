// Navigasi ke halaman utama (mainhome route Flask)
document.getElementById('home-btn').addEventListener('click', () => {
  window.location.href = '/mainhome';
});

// Toggle dark/light mode
const toggleTheme = document.getElementById('toggle-theme');
toggleTheme.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  toggleTheme.textContent = document.body.classList.contains('dark') ? '🌞' : '🌙';
});
