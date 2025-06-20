# Distance_Application

AI-powered web app for meal classification and personalized dietary tips, leveraging a TensorFlow model trained on 101 food categories. 🎯

✨ Features
🔍 Instant Meal Recognition: Upload a photo and identify meals across 101 classes in seconds.
📊 Tailored Recommendations: Receive nutrition guidelines based on recognized meal type.
🌐 Responsive UI: Built with Flask, HTML5, CSS3, and vanilla JavaScript.
🚀 Production-ready: Deploy seamlessly using Gunicorn.
📁 Repository Structure
project/
├── app.py                          # Flask application entrypoint
├── model/
│   └── model_trained_101class.h5   # Pre-trained TensorFlow model
├── static/                         # Public assets
│   ├── styles.css                  # Main stylesheet
│   ├── styles2.css                 # Secondary stylesheet
│   ├── script.js                   # Client-side logic
│   ├── sample1.jpg ──┐             # Sample meal images
│   └── sample4.jpg ──┘
└── templates/                      # Jinja2 templates
    └── index.html                  # Main UI template
🤝 Contributing
Contributions, issues, and feature requests are welcome!

Fork the project
Create your feature branch (git checkout -b feature/YourFeature)
Commit your changes (git commit -m 'Add your feature')
Push to the branch (git push origin feature/YourFeature)
Open a pull request
