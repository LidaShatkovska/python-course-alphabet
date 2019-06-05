from flask import Blueprint, render_template, request

fruits = Blueprint('fruits_page', __name__, template_folder='templates')
fruits_list = ['Mango', 'Mangosteen', 'Marionberry', 'Melon']


@fruits.route("/fruits")
def fruits_page():
    return render_template("fruits.html", values=fruits_list)


@fruits.route('/change_fruits')
@fruits.route('/change_fruits/<string:value>', methods=['GET', 'POST', 'DELETE'])
def change_fruits(value=None):
    if request.method == 'POST':
        do_post(value)
        print(fruits_list)
        return "Successfully added a new value"
    if request.method == 'DELETE':
        do_delete(value)
        return "Successfully deleted the value"
    else:
        return do_get()


def do_post(value):
    return fruits_list.append(value)


def do_delete(value):
    for item in fruits_list:
        if item == value:
            fruits_list.remove(item)
            print(fruits_list)


def do_get():
    return render_template('change_fruits.html', values=fruits_list)
