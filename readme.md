# DevBlog — A Premium Modern Publishing Platform

![DevBlog Preview](https://img.shields.io/badge/Status-Perfected-brightgreen)
![Django](https://img.shields.io/badge/Backend-Django%204.x-092E20)
![Tailwind CSS](https://img.shields.io/badge/Frontend-Tailwind%20CSS-38B2AC)
![Lucide](https://img.shields.io/badge/Icons-Lucide-E24D2F)

**DevBlog** is a high-performance, professional blogging platform designed for digital creators, engineers, and visionaries. It merges a premium SaaS-inspired aesthetic with a robust Django backend to provide a seamless publishing experience.

Developed and perfected by **Ishwari Shinde**.

---

## ✨ Key Features & Enhancements

I have extensively customized this platform to move beyond a standard blog, implementing modern UI/UX patterns and administrative tools:

### 🎨 Modern UI/UX (Premium Feel)
- **Glassmorphism Design**: Using blurred backgrounds and sleek borders for a cutting-edge "SaaS" look.
- **Dynamic Layout Switcher**: Integrated a functional **Grid View / List View** toggle on the home page using custom JavaScript.
- **Theming**: Full dark mode support with smooth transitions.
- **Lucide Icon Integration**: Replaced standard icons with a curated, modern icon set for a professional touch.

### 🛡️ Robust Backend & Management
- **Role-Based Access Control**: Separate dashboards for **Admins, Managers, and Editors** with granular permissions.
- **Automated Data Sync**: Custom Python automation scripts (`sync_site_data.py`) to manage and lock-in site configurations (About Us, Social Links, etc.).
- **Discussion System**: Integrated nested comments with logic to ensure tags render perfectly across all devices.
- **Search Engine**: A full-text search implementation that maintains context across results.

### 📱 Responsive & Accessible
- Fully mobile-responsive design from the navbar to the deep-footer profiles.
- Accessible navigation with a persistent glassmorphism header.

---

## 🛠️ Tech Stack

- **Framework**: Django 4.2+
- **Styling**: Tailwind CSS (Modern responsive design)
- **Database**: SQLite (Development) / PostgreSQL-Ready
- **Icons**: Lucide Icons
- **Logic**: Python / Vanilla JavaScript (ES6+)

---

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/IshwariShinde8772/Devblog.git
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Synchronize Data**:
   Use my custom sync script to quickly populate the About Us and Social profiles:
   ```bash
   python sync_site_data.py
   ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

---

## 👤 Author

**Ishwari Shinde**  
*Full Stack Developer & Tech Enthusiast*

---
© 2026 DevBlog Platform. Built with passion and code.
