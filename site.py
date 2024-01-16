from flask import Blueprint, render_template, request, abort

site = Blueprint('site', __name__)


@site.route('/site')
def main():
    return render_template('main_page.html')