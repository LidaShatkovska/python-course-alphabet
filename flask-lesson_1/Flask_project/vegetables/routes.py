from flask import Blueprint, render_template, request

vegetables = Blueprint('vegetables_page', __name__, template_folder='templates')
vegetables_list = ['bean sprouts', 'black-eyed peas', 'borlotti bean', 'broad beans']


@vegetables.route("/vegetables")
def fvegetables_page():
    return render_template("vegetables.html", values=vegetables_list)


@vegetables.route('/change_vegetables')
@vegetables.route('/change_vegetables/<string:value>', methods=['GET', 'POST', 'DELETE'])
def change_vegetables(value=None):
    if request.method == 'POST':
        do_post(value)
        print(vegetables_list)
        return "Successfully added a new value"
    if request.method == 'DELETE':
        do_delete(value)
        return "Successfully deleted the value"
    else:
        return do_get()


def do_post(value):
    return vegetables_list.append(value)


def do_delete(value):
    for item in vegetables_list:
        if item == value:
            vegetables_list.remove(item)
            print(vegetables_list)


def do_get():
    return render_template('change_vegetables.html', values=vegetables_list)
