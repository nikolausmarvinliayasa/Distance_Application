// Upload form submission
document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('file-upload');
    if (fileInput.files.length === 0) {
        alert("Please select an image before uploading.");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            showModal({
                imageUrl: URL.createObjectURL(fileInput.files[0]),
                foodName: result.foodName,
                caloriesPerGram: result.caloriesPerGram,
                dietSuitability: result.dietSuitability,
            });
        } else {
            alert("Failed to upload the image. Please try again.");
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        alert("An error occurred. Please try again.");
    }
});

// Sample image click
document.querySelectorAll('.sample-image').forEach(image => {
    image.addEventListener('click', async function () {
        const imageUrl = this.src;
        await uploadImageToAI(imageUrl);
    });
});

// Upload sample image from URL
async function uploadImageToAI(imageUrl) {
    try {
        const blob = await (await fetch(imageUrl)).blob();
        const file = new File([blob], 'sample-image.jpg', { type: blob.type });

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            showModal({
                imageUrl: imageUrl,
                foodName: result.foodName,
                caloriesPerGram: result.caloriesPerGram,
                dietSuitability: result.dietSuitability,
            });
        } else {
            alert("Failed to process the sample image. Please try again.");
        }
    } catch (error) {
        console.error('Error uploading sample image:', error);
        alert("An error occurred while processing the sample image.");
    }
}

// Show and close modal
function showModal(data) {
    document.getElementById('foodImage').src = data.imageUrl;
    document.getElementById('foodName').textContent = data.foodName;
    document.getElementById('calories').textContent = data.caloriesPerGram;
    document.getElementById('dietSuitability').textContent = data.dietSuitability;
    document.getElementById('resultModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('resultModal').style.display = 'none';
}

// Hamburger menu
function toggleMenu() {
    const navLinks = document.getElementById('nav-links');
    navLinks.classList.toggle('open');
    if (navLinks.style.display === 'flex') {
        navLinks.style.display = 'none';
    } else {
        navLinks.style.display = 'flex';
    }
}

// === DARK MODE TOGGLE ===
document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("theme-toggle");
    const body = document.body;

    // Load saved theme
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark");
        if (toggle) toggle.textContent = "🌞";
    }

    if (toggle) {
        toggle.addEventListener("click", () => {
            body.classList.toggle("dark");
            if (body.classList.contains("dark")) {
                localStorage.setItem("theme", "dark");
                toggle.textContent = "🌞";
            } else {
                localStorage.setItem("theme", "light");
                toggle.textContent = "🌙";
            }
        });
    }
});
    
document.addEventListener('click', function (event) {
    const navLinks = document.getElementById('nav-links');
    const hamburger = document.querySelector('.hamburger');
    if (!navLinks.contains(event.target) && !hamburger.contains(event.target)) {
        navLinks.classList.remove('open');
    }
});