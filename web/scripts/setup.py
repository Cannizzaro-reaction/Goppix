import os
import sys
from importlib import import_module
from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)
with app.app_context():
    db.create_all()

def run_scripts():
    scripts_dir = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(scripts_dir):
        print("The scripts directory does not exist.")
        return

    script_files = [f for f in os.listdir(scripts_dir) if f.endswith('.py')]

    if not script_files:
        print("No scripts found in the scripts directory.")
        return

    print(f"Found {len(script_files)} script(s): {script_files}")
    
    with app.app_context():
        for script in script_files:
            script_path = os.path.join(scripts_dir, script)
            module_name = f"scripts.{os.path.splitext(script)[0]}"
            try:
                print(f"Running script: {script}")
                module = import_module(module_name)
                if hasattr(module, 'run'):
                    module.run()
                else:
                    print(f"Script {script} does not have a 'run' function. Skipping.")
            except Exception as e:
                print(f"Error while running script {script}: {e}")

if __name__ == '__main__':
    print("Starting setup...")
    run_scripts()
    print("Setup completed.")