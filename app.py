from flask import Flask, render_template, redirect, flash, jsonify
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"


connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def pets_list():
    """List of all pets"""

    pets = Pet.query.all()
    return render_template("pet-list.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """display add pet form and handle adding a pet"""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)

        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect("/")
    else:
        return render_template("pet-add-form.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Handle editing a pet"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data

        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect("/")
    else:
        return render_template("pet-edit-form.html", form=form, pet=pet)


@app.route("/pet/<int:pet_id>")
def show_pet(pet_id):
    """Display details of a specific pet"""

    pet = Pet.query.get_or_404(pet_id)

    return render_template("pet-details-form.html", pet=pet)


