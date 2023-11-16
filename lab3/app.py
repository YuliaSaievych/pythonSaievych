from flask import Flask, render_template, url_for
import os
from datetime import datetime

app = Flask(__name__)

# List of skills
my_skills = ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript', 'SQL']

@app.route('/')
def home():
    os_info = os.name  # Adjust based on your use case
    user_agent = "Sample User Agent"  # You may use request.user_agent to get the actual user agent
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('base.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/skills')
@app.route('/skills/<int:id>')
def display_skills(id=None):
    if id is not None:
        # Display a specific skill based on the provided id
        if 0 <= id < len(my_skills):
            skill = my_skills[id]
            return f"Skill {id + 1}: {skill}"
        else:
            return "Invalid skill ID"
    else:
        # Display all skills and their total count
        skills_count = len(my_skills)
        return render_template('page_skills.html', skills=my_skills, skills_count=skills_count)

if __name__ == '__main__':
    app.run(debug=True)
