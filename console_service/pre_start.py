import constants
import os
import json

from flask import app, Flask
import backend.db.common

settings_path = os.path.join(constants.current_path, 'settings.json')
settings_base_path = os.path.join(constants.current_path, 'settings_base.json')


def run(app, login_manager):
    setup_settings()
    app.template_folder = generate_templates_dir()
    app.secret_key = constants.secret_key
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
    backend.db.common.init()
    login_manager.login_view = 'login_route'
    return app, login_manager


def generate_templates_dir():
    template_dir = os.path.join(constants.current_path, 'html')
    template_dir = os.path.join(template_dir, 'templates')
    print(template_dir)
    constants.templates_dir = template_dir
    return template_dir


def setup_settings():
    if not check_settings():
        constants.DB_SETTINGS = create_settings()['DB']
    else:
        settings = open(settings_path).read()
        constants.DB_SETTINGS = json.loads(settings)['DB']


def check_settings():
    return os.path.exists(settings_path)


def create_settings():
    file = open(settings_base_path, 'r')
    base = file.read()
    file.close()
    base = json.loads(base)
    settings = base
    for module in base:
        for setting in base[module]:
            s = input(f"please input {module}.{setting}: ")
            settings[module][setting] = s
    settings_file = open(settings_path, 'w')
    settings_file.write(json.dumps(settings))
    settings_file.close()
    return settings
