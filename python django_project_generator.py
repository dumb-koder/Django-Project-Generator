import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import re

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd=cwd, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        raise

def initialize_git_repo(project_location):
    """Initialize a Git repository and make the first commit."""
    try:
        run_command('git init', cwd=project_location)
        run_command('git add .', cwd=project_location)
        run_command('git commit -m "Initial commit"', cwd=project_location)
        print("Git repository initialized successfully.")
    except subprocess.CalledProcessError:
        print("Failed to initialize Git repository. Please check if Git is installed and try again.")

def create_django_project(project_name, apps, location):
    try:
        project_location = os.path.join(location, project_name)
        os.makedirs(project_location, exist_ok=True)

        print("Installing Django...")
        run_command('pip install django', cwd=project_location)

        print(f"Creating Django project: {project_name}")
        run_command(f'django-admin startproject {project_name} .', cwd=project_location)

        for app_name in apps:
            print(f"Creating app: {app_name}")
            run_command(f'python manage.py startapp {app_name}', cwd=project_location)

        update_settings(project_location, project_name, apps)
        update_urls(project_location, project_name, apps)
        create_app_files(project_location, apps)

        create_requirements_file(project_location)
        initialize_git_repo(project_location)

        print(f"Django project '{project_name}' with apps {', '.join(apps)} created successfully!")
        print(f"Project location: {project_location}")
        print("Next steps:")
        print("1. Review and adjust the settings in settings.py")
        print("2. Run migrations: python manage.py migrate")
        print("3. Create a superuser: python manage.py createsuperuser")
        print("4. Run the development server: python manage.py runserver")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def update_settings(project_location, project_name, apps):
    settings_path = os.path.join(project_location, project_name, 'settings.py')
    with open(settings_path, 'r') as file:
        settings_content = file.read()

    # Update INSTALLED_APPS
    installed_apps_pattern = r'INSTALLED_APPS = \[(.*?)\]'
    existing_apps = re.search(installed_apps_pattern, settings_content, re.DOTALL).group(1)
    new_apps = "".join([f"    '{app}',\n" for app in apps])
    updated_apps = f"{existing_apps}\n{new_apps}"
    
    settings_content = re.sub(
        installed_apps_pattern,
        f"INSTALLED_APPS = [{updated_apps}]",
        settings_content,
        flags=re.DOTALL
    )

    with open(settings_path, 'w') as file:
        file.write(settings_content)

def update_urls(project_location, project_name, apps):
    urls_path = os.path.join(project_location, project_name, 'urls.py')
    with open(urls_path, 'r') as file:
        urls_content = file.read()

    # Ensure admin import and URL are present
    if 'from django.contrib import admin' not in urls_content:
        urls_content = urls_content.replace(
            'from django.urls import path',
            'from django.contrib import admin\nfrom django.urls import path, include'
        )
    else:
        urls_content = urls_content.replace(
            'from django.urls import path',
            'from django.urls import path, include'
        )

    # Update urlpatterns
    urlpatterns_pattern = r'urlpatterns = \[(.*?)\]'
    existing_patterns = re.search(urlpatterns_pattern, urls_content, re.DOTALL).group(1)
    new_patterns = "".join([f"    path('{app}/', include('{app}.urls')),\n" for app in apps])
    
    if 'path(\'admin/\'' not in existing_patterns:
        new_patterns = "    path('admin/', admin.site.urls),\n" + new_patterns

    updated_patterns = f"{existing_patterns}\n{new_patterns}"
    
    urls_content = re.sub(
        urlpatterns_pattern,
        f"urlpatterns = [{updated_patterns}]",
        urls_content,
        flags=re.DOTALL
    )

    with open(urls_path, 'w') as file:
        file.write(urls_content)

def create_app_files(project_location, apps):
    for app in apps:
        # Create urls.py
        app_urls_path = os.path.join(project_location, app, 'urls.py')
        with open(app_urls_path, 'w') as file:
            file.write(
                "from django.urls import path\n"
                "from . import views\n\n"
                "urlpatterns = [\n"
                "    path('', views.index, name='index'),\n"
                "]\n"
            )

        # Update views.py
        views_path = os.path.join(project_location, app, 'views.py')
        with open(views_path, 'a') as file:
            file.write(
                "\n\n"
                "def index(request):\n"
                f"    return render(request, '{app}/index.html')\n"
            )

        # Create a basic template
        os.makedirs(os.path.join(project_location, app, 'templates', app), exist_ok=True)
        template_path = os.path.join(project_location, app, 'templates', app, 'index.html')
        with open(template_path, 'w') as file:
            file.write(
                "<!DOCTYPE html>\n"
                "<html lang='en'>\n"
                "<head>\n"
                "    <meta charset='UTF-8'>\n"
                "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
                f"    <title>{app.capitalize()} Index</title>\n"
                "</head>\n"
                "<body>\n"
                f"    <h1>Welcome to the {app.capitalize()} app!</h1>\n"
                "</body>\n"
                "</html>\n"
            )

def create_requirements_file(project_location):
    run_command('pip freeze > requirements.txt', cwd=project_location)

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    if not directory:
        raise ValueError("No directory selected. Exiting...")
    return directory

if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    app_names = input("Enter the app names (comma separated): ").split(',')
    app_names = [app_name.strip() for app_name in app_names]

    print("Please select the directory where the project should be created:")
    location = select_directory()

    create_django_project(project_name, app_names, location)
