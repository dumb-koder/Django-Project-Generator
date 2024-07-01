# Django Project Generator

A Python script to quickly set up a customized Django project with multiple apps.

## Description

This tool automates the process of creating a new Django project with multiple apps. It sets up the project structure, configures settings, creates basic views, and initializes a Git repository. The script uses a graphical interface for selecting the project location and provides a command-line interface for entering project and app names.

## Features

- Create a new Django project with a custom name
- Add multiple apps to the project
- Automatically update `settings.py` to include new apps
- Set up basic URL routing for each app
- Create a simple index view for each app
- Customize the Django admin site
- Initialize a Git repository with an initial commit

## Requirements

- Python 3.x
- Django
- Git

## Usage

1. Run the script:
   ```
   python django_project_generator.py
   ```

2. Enter the project name when prompted.

3. Enter the app names, separated by commas.

4. Select the directory where you want to create the project using the file dialog.

5. The script will create the Django project and apps, and initialize a Git repository.

## Customization

You can modify the script to add more features or change the default setup:

- Add more configuration to `settings.py`
- Customize the initial views and URL patterns
- Add database setup or migrations
- Include additional files or directories in the project structure

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
