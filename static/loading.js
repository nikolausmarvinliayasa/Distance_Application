// Placeholder interactivity
console.log("Landing page loaded.");

function toggleMenu() {
  const menu = document.getElementById("dropdownMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function toggleTheme() {
  const isDark = document.body.classList.toggle("dark-mode");
  localStorage.setItem("theme", isDark ? "dark" : "light");

  const toggleBtn = document.getElementById("themeToggle");
  if (toggleBtn) {
    toggleBtn.textContent = isDark ? "🌞" : "🌙";
  }
}

// Load saved theme on start
window.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    const toggleBtn = document.getElementById("themeToggle");
    if (toggleBtn) {
      toggleBtn.textContent = "🌞";
    }
  }
});

// Optional: Klik di luar menutup menu
document.addEventListener("click", function (e) {
  const menu = document.getElementById("dropdownMenu");
  const hamburger = document.querySelector(".hamburger");

  if (!menu.contains(e.target) && !hamburger.contains(e.target)) {
    menu.style.display = "none";
  }
});