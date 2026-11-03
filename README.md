# Personal--Portfolio--Python--Project

My Python Mini Project

Personal Portfolio Website Using Python

Project Overview
Personal Portfolio Website Using Python is a mini project that generates
a responsive personal portfolio website from a single JSON data file.
The portfolio presents a person's introduction, skills, projects,
education, achievements, and contact details.

Instead of editing HTML content manually, the project reads information
from profile.json, validates it, creates a skills chart using Pandas
and Matplotlib, and generates a static website using a Jinja2 HTML
template.
Important: The sample profile contains placeholder information.
Replace it with your own accurate details before publishing the
website.

Objectives
- Store portfolio information in one JSON file.
- Validate required fields, skill levels, email addresses, and links.
- Use Pandas to organize skills by category.
- Create a skills chart using Matplotlib.
- Generate a responsive static website with Python and Jinja2.
- Test the portfolio generator using Python's unittest framework.
  
Technologies Used
- Programming language: Python 3
- Templating: Jinja2
- Data handling: Pandas
- Visualization: Matplotlib
- Front end: HTML5 and CSS3
- Data format: JSON
- Testing: Python unittest

Project Structure
Personal-Portfolio-Website/
├── build_portfolio.py
├── profile.json
├── test_portfolio.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── site/
    ├── index.html
    ├── style.css
    └── assets/
        └── skills.png
The site/ folder is generated when the build script runs. Your exact
folder structure may differ slightly depending on the supplied project
files.

Features
- Personal introduction and About section
- Skills grouped by category
- Automatically generated skills chart
- Project descriptions and optional project links
- Education and achievements section
- Contact section with an email link
- Responsive layout for smaller screens
- Input validation and safe link checking
- Automated unit tests

How It Works
1. The program reads portfolio details from profile.json.
2. It checks required information, skill levels, email address, and
   links.
3. Pandas organizes the skills into categories.
4. Matplotlib creates a skills chart.
5. Jinja2 combines the profile data with the HTML template.
6. The generated website files are saved in the site/ folder.
7. The website can be opened in a browser or published using static
   hosting.
Installation and Setup
1. Install Python
Install Python 3 on your computer.
2. Open the project folder
Open the project folder in VS Code or a terminal.
3. Install dependencies
pip install -r requirements.txt
4. Generate the portfolio website
python build_portfolio.py
5. Run the automated tests
python -m unittest -v
6. View the website
Open site/index.html in a web browser.

Alternatively, open a terminal inside the site folder and run:
python -m http.server
Then visit http://localhost:8000 in your browser.
Customizing Your Portfolio
Edit profile.json to add your own: - Name, title, tagline, and
location - About information - Skills, categories, and skill levels -
Project titles, descriptions, tags, and links - Education and
achievements - Email address and contact links

Skill levels must be between 0 and 100. Use only safe link types
supported by the project, such as https://, http://, and mailto:.

Do not publish private information such as your home address, identity
numbers, passwords, or other sensitive details.


Output and Results
The project generates a static website containing the following
sections: - Home/header - About - Skills - Projects - Education and
achievements - Contact - Footer

The sample run reported 8 skills across 4 categories, 3 projects, 2
education entries, 2 achievements, and 2 contact links. It also reported
that all 11 automated tests passed. These results relate to the sample
project data and test run.

Advantages
- Portfolio information is maintained in one file.
- Updates can be made without manually editing multiple HTML sections.
- Validation helps catch missing or invalid information.
- Static output can be hosted using a static hosting service.
- The project demonstrates Python data handling, visualization,
  templating, and testing.

Limitations
- The website is a single static page.
- It does not include a database, login system, or content management
  system.
- The contact section uses an email link rather than a message-storage
  form.
- Sample profile details must be replaced before publishing.
- Skill levels are self-assessed.

Future Scope
- Add a mobile navigation menu.
- Add separate pages for individual projects.
- Generate a downloadable PDF resume from the same profile data.
- Automate publishing through GitHub Pages.
- Add accessibility and performance checks.
- Add a suitable contact form service.

Privacy and Ethical Considerations
Publish only information that you are comfortable sharing publicly. Use
honest descriptions of your skills and projects, credit third-party
images and resources, and do not publish private customer or personal
data. Make the website accessible with readable text, sufficient
contrast, and alternative text for images.

Conclusion
This project demonstrates how Python can generate a responsive personal
portfolio website from structured JSON data. It combines data
validation, Pandas, Matplotlib, Jinja2, HTML, and CSS to create a
website that is easier to maintain and update. The generated site should
be reviewed in modern browsers, and all sample placeholders should be
replaced with accurate information before publication.

Author
Balpreet Kaur
B.Sc. Computer Science
Mini Project
