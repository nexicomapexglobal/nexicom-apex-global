NEXICOM APEX GLOBAL — LAUNCH-READY WEBSITE + ADMIN CMS

Main features
- Premium black-and-gold responsive corporate design
- Scroll, card, counter and popup animations
- Team cards with full profile popup details
- Admin-controlled services, team, reviews and jobs
- Online job applications with resume upload
- Candidate application status tracking
- Contact enquiry CRM inbox
- Website branding, hero, statistics, colors, visibility and SEO controls
- WhatsApp button, sitemap.xml and robots.txt
- GoDaddy cPanel/VPS and Render deployment files

Local setup (Windows PowerShell)
1. Open this project folder in VS Code.
2. Run: py -m venv venv
3. Run: .\venv\Scripts\Activate.ps1
4. Run: pip install -r requirements.txt
5. Copy .env.example to .env and update the password and secret key.
6. Run: python app.py
7. Website: http://127.0.0.1:5000
8. Admin: http://127.0.0.1:5000/admin/login

Default credentials are read from .env. Never launch with the sample password.

Before public launch
- Add the real phone, email and WhatsApp number.
- Add real team members and approved reviews.
- Change the admin password.
- Confirm your GoDaddy plan supports Python/Flask.
- Enable HTTPS/SSL.

See GODADDY_LAUNCH_GUIDE.txt for hosting steps.
