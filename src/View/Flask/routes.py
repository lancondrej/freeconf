__author__ = 'Ondřej Lanč'


from flask import session, redirect, url_for, render_template, request, flash, jsonify
from flask import current_app, Blueprint, render_template
from src.View.Flask.freeconf_view import FreeconfView

freeconf_flask=FreeconfView()

presenter=freeconf_flask.presenter
renderer=freeconf_flask.renderer

entry = Blueprint('admin', __name__, url_prefix='/admin')
main_blueprint = Blueprint('main', __name__, url_prefix='/')
package_blueprint = Blueprint('package', __name__, url_prefix='/')


@main_blueprint.route('')
def index():
    return render_default()

@main_blueprint.route('about')
def about():
    return render_default(body=render_template("about.html"))

@main_blueprint.route('setting')
def setting():
    return package_blueprint("Freeconf")

@package_blueprint.route('<package>')
def package(package):
    if presenter.load_package(package):
        session['package'] = package
        return render_default(package=presenter.package.package_name, tabs=presenter.package.tabs())
    else:
        return "error"

@package_blueprint.route('tab/<name>')
def tab(name):
    sections = presenter.package.tab(name)
    Rsection = ""
    for section in sections:
        Rsection = Rsection + renderer.entry_render(section)
    return render_default(package=presenter.package.package_name, tabs=presenter.package.tabs(), body=Rsection)

@main_blueprint.route('configure')
def configure():
    packages = presenter.config.packages_list
    return render_default(body=render_template("configure.html", packages=packages))


def render_default(package=None, tabs=None, body=""):
    return render_template('index.html', package_name=package, tabs=tabs, main=body)


@package_blueprint.route('_multiple_modal')
def multiple_modal():
    full_name = request.args.get('full_name')
    entry = presenter.entry.get_entry(full_name)
    return renderer.render_modal(entry)

@package_blueprint.route('_multiple_collapse')
def multiple_collapse():
    full_name = request.args.get('full_name')
    entry = presenter.entry.get_entry(full_name)
    return renderer.render_collapse(entry)


