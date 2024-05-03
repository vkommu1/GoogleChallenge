# IntegrAIty


# Description
My web application gives the ability for users to test Gemini’s results for bias in their application domain. For example, a sociologist may look for the data like race and ethnic distribution in the generated data and study patterns of inquality, discrimination, and social impacts of biases.

# Details
Creator: Veena Kommu

# Installation Instructions
*Note: requires Python3.*
<ol>
  <li>Clone this repository to a local directory: <code>git clone https://github.com/vkommu1/GoogleChallenge.git</code>
  <li><code>cd</code> into the project directory</li>
  <li>Install the required packages: <code>python -m pip install -r requirements.txt</code>
    <ul>
      <li>Optional: Create a virtual environment before installing.</li>
    </ul>
  <li>Setup: 
    <ul>
      <li><code>python manage.py makemigrations</code></li>
      <li><code>python manage.py migrate</code></li>
    </ul>
</ol>
Run <code>python manage.py runserver</code> to start a development server on your local machine (default: <code>127.0.0.1:8000</code>).

Use API keys in your .env file
