from flask import render_template, request , redirect,session

from flask_app import app

from flask_app.models.order import Order

@app.route('/')
def home():
    return redirect('/cookies')

#home route from landing page via index.html
@app.route("/cookies")
def display_all():
    orders = Order.get_all()
    return render_template("cookies.html",orders=orders)


@app.route('/cookies/new')
def new_order():
    orders = Order.get_all()
    return render_template("cookies_new.html", orders = orders )


@app.route('/cookies/new', methods=["POST"])
def create_order():
    data = {
    "name": request.form["name"],
    "type" : request.form["type"],
    "num_of_boxes" : request.form["num_of_boxes"]
    }
    new_order = Order.get_last()
    if Order.order_is_valid(request.form):
        Order.save(data)
        return redirect("/cookies")

    else:
        return redirect('/cookies/new')


@app.route('/cookies/edit/<int:id>')
def edit_order(id):
    data ={
        "id":id
    }
    order = Order.get_one(data)
    Order.save(data)
    return render_template("cookies_edit.html", order=order)



@app.route('/cookies/update', methods = ['POST'])
def update():
    Order.update(request.form)
    return redirect('/cookies')

