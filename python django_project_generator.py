import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def run_command(command):
  # Runs a command and returns the result.
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def initialize_git_repo(project_location):
    # Initializes a Git repository and makes the first commit.
    os.chdir(project_location)
    run_command(['git', 'init'])
    run_command(['git', 'add', '.'])
    run_command(['git', 'commit', '-m', 'Initial commit'])

def create_django_project(project_name, apps, location):
    try:
        # Set up the project location
        project_location = os.path.join(location, project_name)
        os.makedirs(project_location, exist_ok=True)

        # Create Django project
        run_command(f'django-admin startproject {project_name} {project_location}')

        # Navigate into the project directory
        os.chdir(project_location)

        for app_name in apps:
            # Create Django app
            run_command(f'python manage.py startapp {app_name}')

        # Update settings.py to include the new apps
        settings_path = os.path.join(project_location, project_name, 'settings.py')
        with open(settings_path, 'r') as settings_file:
            settings_content = settings_file.read()

        installed_apps_index = settings_content.find('INSTALLED_APPS = [')
        if installed_apps_index != -1:
            end_index = settings_content.find(']', installed_apps_index)
            new_apps = "".join([f"    '{app_name}',\n" for app_name in apps])
            settings_content = settings_content[:end_index] + new_apps + settings_content[end_index:]

        with open(settings_path, 'w') as settings_file:
            settings_file.write(settings_content)

        # Set up URLs
        urls_path = os.path.join(project_location, project_name, 'urls.py')
        with open(urls_path, 'r') as urls_file:
            urls_content = urls_file.read()

        new_import = "from django.urls import include, path\n"
        new_urlpatterns = "".join([f"    path('{app_name}/', include('{app_name}.urls')),\n" for app_name in apps])

        if 'urlpatterns = [' in urls_content:
            urls_content = urls_content.replace('urlpatterns = [', f'{new_import}urlpatterns = [\n{new_urlpatterns}')
        else:
            urls_content = f"{new_import}\nurlpatterns = [\n{new_urlpatterns}]\n"

        with open(urls_path, 'w') as urls_file:
            urls_file.write(urls_content)

        for app_name in apps:
            # Create urls.py in the new app
            app_urls_path = os.path.join(project_location, app_name, 'urls.py')
            with open(app_urls_path, 'w') as app_urls_file:
                app_urls_file.write(
                    "from django.urls import path\n"
                    "from . import views\n\n"
                    "urlpatterns = [\n"
                    "    path('', views.index, name='index'),\n"
                    "]\n"
                )

            # Create a basic view in the new app
            views_path = os.path.join(project_location, app_name, 'views.py')
            with open(views_path, 'a') as views_file:
                views_file.write(
                    "\nfrom django.http import HttpResponse\n\n"
                    "def index(request):\n"
                    "    return HttpResponse('Hello, world! This is the index view of the app.')\n"
                )

        # Customize the admin site
        admin_path = os.path.join(project_location, project_name, 'urls.py')
        with open(admin_path, 'a') as admin_file:
            admin_file.write(
                "\nfrom django.contrib import admin\n"
                "admin.site.site_header = 'My Custom Admin'\n"
                "admin.site.site_title = 'Admin Portal'\n"
                "admin.site.index_title = 'Welcome to the Admin Portal'\n"
            )

        # Initialize Git repository
        initialize_git_repo(project_location)

        print(f"Django project '{project_name}' with apps {', '.join(apps)} created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    if not directory:
        messagebox.showerror("Error", "No directory selected. Exiting...")
    return directory

if __name__ == "__main__":
    project_name = input("Enter the project name: ")
    app_names = input("Enter the app names (comma separated): ").split(',')

    # Strip any whitespace from the app names
    app_names = [app_name.strip() for app_name in app_names]

    print("Please select the directory where the project should be created:")
    location = select_directory()

    if location:
        create_django_project(project_name, app_names, location)
    else:
        print("No directory selected. Exiting...")
