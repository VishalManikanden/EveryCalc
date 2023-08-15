from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
import datetime as dt
import math
import hashlib
import random
from forms import SignUpForm, SignInForm, SearchForm, ContactForm
from math_calculators import RectangleAreaCalculator, TriangleAreaCalculatorBaseHeight, TrapezoidAreaCalculator, \
    HexagonAreaCalculator, CircleAreaCalculator, CircleCircumferenceCalculator, RegularPolygonAreaCalculator, \
    TriangleAreaCalculatorHeron, CollatzConjectureCalculator, RectangularPrismCalculator, TriangularPrismCalculator, \
    EllipseAreaCalculator, SphereCalculator, CylinderCalculator, ArithmeticSequenceCalculator, \
    ArithmeticSeriesCalculator, GeometricSequenceCalculator, GeometricSeriesCalculator, HypotenuseCalculator, \
    PermutationsCombinationsCalculator, SlopeCalculator
from business_calculators import CompoundInterestCalculator, SimpleInterestCalculator, DepreciationCalculator, \
    ROICalculator
from other_calculators import BMICalculator, HashGenerator, DiceRoller, PasswordGenerator

app = Flask(__name__)
app.app_context().push()

load_dotenv(find_dotenv())
app.config['SECRET_KEY'] = os.getenv("SecretKey")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///EveryCalc.db")
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(1000))
    sign_in_count = db.Column(db.Integer, default=0)
    view_saved_count = db.Column(db.Integer, default=0)

    # User can have many calculations (create one-to-many relationship)
    calculations = db.relationship("UserSavedCalculations", backref="user")


class Calculator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calculator = db.Column(db.String(1000), unique=True)
    category = db.Column(db.String(1000), unique=False)


class UserSavedCalculations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calculator = db.Column(db.String(1000))
    input1 = db.Column(db.String(1000))
    input2 = db.Column(db.String(1000))
    input3 = db.Column(db.String(1000))
    input4 = db.Column(db.String(1000))
    input5 = db.Column(db.String(1000))
    input6 = db.Column(db.String(1000))
    result = db.Column(db.String(1000))
    result2 = db.Column(db.String(1000))
    result3 = db.Column(db.String(1000))
    result4 = db.Column(db.String(1000))
    date = db.Column(db.String(1000))

    # Create foreign key to link users
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # Allow each saved calculation object to be identified by the inputs and results
    def __repr__(self):
        return f'{self.calculator},{self.input1},{self.input2},{self.input3},{self.input4},{self.input5},' \
               f'{self.input6},{self.result},{self.result2},{self.result3},{self.result4},{self.date}'


# db.create_all()

now = dt.datetime.now()
year = now.year


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Create sign in required decorator
def sign_in_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not signed in then redirect to sign in page
        if not current_user.is_authenticated:
            return redirect(url_for("sign_in"))
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# Redirect to home if invalid route
@app.errorhandler(404)
def invalid_route(error):
    return redirect(url_for("home"))


@app.route("/home")
@app.route("/")
def home():
    show_saved_popup = False

    if current_user.is_authenticated:
        count = User.query.get(current_user.id)
        count.sign_in_count += 1
        db.session.commit()

        if User.query.get(current_user.id).sign_in_count <= 3 and User.query.get(current_user.id).view_saved_count == 0:
            show_saved_popup = True

    return render_template("index.html", current_user=current_user, year=year, display_other=True,
                           show_saved_popup=show_saved_popup)


# Pass search form to navbar
@app.context_processor
def navbar():
    form = SearchForm()
    return dict(form=form)


@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        calculator_searched = form.search.data

        if calculator_searched == "":
            return redirect(url_for("home"))
        else:
            results = Calculator.query.filter(Calculator.calculator.like("%" + calculator_searched + "%"))
            results = results.order_by(Calculator.calculator).all()
            return render_template("search.html", form=form, calculator_searched=calculator_searched, results=results,
                                   year=year, display_other=False)

    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = SignUpForm()

    if form.validate_on_submit():
        # If chosen username already exists
        if User.query.filter_by(username=form.username.data).first():
            # Send flash message
            flash("This username already exists, please choose a different one")
            return redirect(url_for('sign_up'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=12
        )
        new_user = User()
        new_user.username = form.username.data
        new_user.password = hash_and_salted_password
        new_user.sign_in_count = 0

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home'))

    return render_template("sign_up.html", form=form, current_user=current_user, year=year, display_other=True)


@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = SignInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        # Email doesn't exist
        if not user:
            flash("That username does not exist, please try again.")
            return redirect(url_for('sign_in'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('sign_in'))
        # Email exists and password correct
        else:
            login_user(user)

            # Update the sign-in count
            count = User.query.get(current_user.id)
            count.sign_in_count += 1
            db.session.commit()
            return redirect(url_for('home'))

    return render_template("sign_in.html", form=form, current_user=current_user, year=year, display_other=True)


@app.route("/sign-out")
def sign_out():
    count = User.query.get(current_user.id)
    count.sign_in_count -= 1
    db.session.commit()

    logout_user()
    return redirect(url_for('home'))


@app.route("/contact", methods=["GET", "POST"])
@sign_in_required
def contact():
    form = ContactForm(request.form)

    if form.validate_on_submit():
        name = form.name.data
        message = form.message.data
        return redirect(f"mailto:everycalc.calculators@gmail.com?body={message}")

    return render_template("contact.html", form=form, year=year, display_other=True)


@app.route("/saved-calculations", methods=["GET", "POST"])
@sign_in_required
def saved_calculations():
    if current_user.is_authenticated:
        count = User.query.get(current_user.id)
        count.view_saved_count += 1
        db.session.commit()

    calculations = db.session.query(UserSavedCalculations).all()
    list_calculations = []

    for calculation in calculations:
        if calculation.user.id == current_user.id:
            list_calculations.append(str(calculation).split(","))

    list_calculations = [list(filter(lambda x: x != 'None' and x != "", sublist)) for sublist in list_calculations]
    list_calculations.reverse()

    if request.method == "POST":
        for calc in range(1, len(calculations) + 1):
            if calculations[calc - 1].user_id == current_user.id:
                delete_calculation = UserSavedCalculations.query.get(calc)
                db.session.delete(delete_calculation)
                db.session.commit()

        return redirect(url_for("saved_calculations"))

    return render_template("saved_calculations.html", year=year, display_other=True, current_user=current_user,
                           calculations=calculations, list_calculations=list_calculations,
                           date=now.date().strftime("%m/%d/%Y"))


# Math calculators
@app.route("/collatz-conjecture-calculator", methods=["GET", "POST"])
def collatz_conjecture_calculator():
    form = CollatzConjectureCalculator()

    if form.validate_on_submit():
        original_number = int(form.number.data)
        steps = "The number you inputted was too large"
        number = original_number

        try:
            number / 2
        except OverflowError:
            pass
        else:
            steps = 0

            while number != 1:
                if number % 2 == 0:
                    number = number / 2
                else:
                    number = (3 * number) + 1

                steps += 1

            if current_user.is_authenticated:
                calculation = UserSavedCalculations(calculator="Collatz conjecture calculator", input1=original_number,
                                                    input2=None, input3=None, input4=None, input5=None, input6=None,
                                                    result=steps, result2=None, result3=None, result4=None,
                                                    user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
                db.session.add(calculation)
                db.session.commit()

        return render_template("collatz_conjecture_calculator.html", original_number=original_number, steps=steps,
                               year=year, form=form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("collatz_conjecture_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route('/permutations-combinations-calculator', methods=["GET", "POST"])
def permutations_and_combinations_calculator():
    form = PermutationsCombinationsCalculator()

    if form.validate_on_submit():
        calculator_type = form.calculator_type.data
        n = int(form.n.data)
        r = int(form.r.data)
        result = "The number you inputted was too large"

        try:
            math.factorial(n) and math.factorial(r)
        except OverflowError:
            pass
        else:
            try:
                math.factorial(n) / math.factorial(n - r)
            except ValueError:
                result = "Number of objects being chosen cannot be greater than the number of objects"
            else:
                if calculator_type == "Permutation":
                    result = math.factorial(n) / math.factorial(n - r)
                elif calculator_type == "Combination":
                    result = math.factorial(n) / (math.factorial(r) * math.factorial(n - r))

                if current_user.is_authenticated:
                    calculation = UserSavedCalculations(calculator="Permutations and combinations calculator",
                                                        input1=calculator_type, input2=n, input3=r, input4=None,
                                                        input5=None, input6=None, result=result, result2=None,
                                                        result3=None, result4=None, user_id=current_user.id,
                                                        date=now.date().strftime("%m/%d/%Y"))
                    db.session.add(calculation)
                    db.session.commit()

        return render_template("permutations_combinations_calculator.html", result=result, year=year, form=form,
                               calculator_type=calculator_type, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("permutations_combinations_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/arithmetic-sequence-calculator", methods=["GET", "POST"])
def arithmetic_sequence_calculator():
    n_form = ArithmeticSequenceCalculator()
    sum_form = ArithmeticSeriesCalculator()

    if sum_form.validate_on_submit():
        initial_term = float(sum_form.initial_term.data)
        n = float(sum_form.n.data)
        number_of_terms = int(sum_form.number_of_terms.data)
        series_sum = round(number_of_terms * ((initial_term + n) / 2), 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Arithmetic sequence calculator", input1="Series",
                                                input2=initial_term, input3=n, input4=number_of_terms, input5=None,
                                                input6=None,
                                                result=series_sum, result2=None, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("arithmetic_sequence_calculator.html", series_sum=series_sum, year=year,
                               sum_form=sum_form, n_form=n_form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    if n_form.validate_on_submit():
        a = float(n_form.a.data)
        term_number = float(n_form.term_number.data)
        d = float(n_form.d.data)
        number = round(a + (term_number - 1) * d, 5)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Arithmetic sequence calculator", input1="Sequence",
                                                input2=a, input3=term_number, input4=d, input5=None, input6=None,
                                                result=number,
                                                result2=None, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("arithmetic_sequence_calculator.html", number=number, sum_form=sum_form, n_form=n_form,
                               year=year, display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("arithmetic_sequence_calculator.html", n_form=n_form, sum_form=sum_form, year=year,
                           display_other=True, sign_in_recommended=current_user.is_authenticated)


@app.route("/geometric-sequence-calculator", methods=["GET", "POST"])
def geometric_sequence_calculator():
    n_form = GeometricSequenceCalculator()
    sum_form = GeometricSeriesCalculator()

    if sum_form.validate_on_submit():
        first_term = float(sum_form.first_term.data)
        number_of_terms = float(sum_form.number_of_terms.data)
        ratio = float(sum_form.ratio.data)
        series_sum = round((first_term * (1 - ratio ** number_of_terms)) / (1 - ratio), 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Geometric sequence calculator", input1="Series",
                                                input2=first_term, input3=number_of_terms, input4=ratio, input5=None,
                                                input6=None, result=series_sum, result2=None, result3=None,
                                                result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("geometric_sequence_calculator.html", series_sum=series_sum, year=year,
                               sum_form=sum_form, n_form=n_form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    if n_form.validate_on_submit():
        initial_term = float(n_form.initial_term.data)
        term_number = int(n_form.term_number.data)
        common_ratio = float(n_form.common_ratio.data)
        number = round(initial_term * common_ratio ** (term_number - 1), 5)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Geometric sequence calculator", input1="Sequence",
                                                input2=initial_term, input3=term_number, input4=common_ratio,
                                                input5=None, input6=None, result=number,
                                                result2=None, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("geometric_sequence_calculator.html", number=number, sum_form=sum_form, n_form=n_form,
                               year=year, display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("geometric_sequence_calculator.html", n_form=n_form, sum_form=sum_form, year=year,
                           display_other=True, sign_in_recommended=current_user.is_authenticated)


@app.route("/slope-calculator", methods=["GET", "POST"])
def slope_calculator():
    form = SlopeCalculator()

    if form.validate_on_submit():
        x1 = float(form.x1.data)
        x2 = float(form.x2.data)
        y1 = float(form.y1.data)
        y2 = float(form.y2.data)
        slope = "undefined"

        try:
            ((y2 - y1) / (x2 - x1))
        except ZeroDivisionError:
            pass
        else:
            slope = round(((y2 - y1) / (x2 - x1)), 2)

        if current_user.is_authenticated and (x1, y1) != (x2, y2):
            calculation = UserSavedCalculations(calculator="Slope calculator", input1=x1, input2=y1,
                                                input3=x2, input4=y2, input5=None, input6=None, result=slope,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("slope_calculator.html", slope=slope, y1=y1, y2=y2, x1=x1, x2=x2, year=year, form=form,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("slope_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/rectangle-area-calculator", methods=["GET", "POST"])
def rectangle_area_calculator():
    form = RectangleAreaCalculator()

    if form.validate_on_submit():
        length = float(form.length.data)
        width = float(form.width.data)
        area = round(length * width, 10)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Rectangle area calculator", input1=length, input2=width,
                                                input3=None, input4=None, input5=None, input6=None, result=area,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("rectangle_area_calculator.html", area=area, year=year, form=form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("rectangle_area_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/rectangular-prism-calculator", methods=["GET", "POST"])
def rectangular_prism_calculator():
    form = RectangularPrismCalculator()

    if form.validate_on_submit():
        length = float(form.length.data)
        width = float(form.width.data)
        height = float(form.height.data)
        surface_area = round(length * height * 2 + length * width * 2 + width * height * 2, 2)
        volume = round(length * width * height, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Rectangular prism calculator", input1=length, input2=width,
                                                input3=height, input4=None, input5=None, input6=None,
                                                result=surface_area,
                                                result2=volume, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("rectangular_prism_calculator.html", surface_area=surface_area, volume=volume, year=year,
                               form=form, display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("rectangular_prism_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/triangle-area-calculator", methods=["GET", "POST"])
def triangle_area_calculator():
    base_height_form = TriangleAreaCalculatorBaseHeight()
    heron_form = TriangleAreaCalculatorHeron()

    if heron_form.validate_on_submit():
        a = float(heron_form.a.data)
        b = float(heron_form.b.data)
        c = float(heron_form.c.data)
        s = (a + b + c) / 2

        try:
            round(math.sqrt(s * (s - a) * (s - b) * (s - c)), 2)
        except ValueError:
            area_heron = "The side lengths you provided cannot make a triangle"
        else:
            if (a + b <= c) or (b + c <= a) or (a + c <= b):
                area_heron = "The side lengths you provided cannot make a triangle"
            else:
                area_heron = round(math.sqrt(s * (s - a) * (s - b) * (s - c)), 2)

                if current_user.is_authenticated:
                    calculation = UserSavedCalculations(calculator="Triangle area calculator", input1="heron", input2=a,
                                                        input3=b, input4=c, input5=None, input6=None, result=area_heron,
                                                        result2=None, result3=None, result4=None,
                                                        user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
                    db.session.add(calculation)
                    db.session.commit()

        return render_template("triangle_area_calculator.html", area_heron=area_heron, year=year,
                               heron_form=heron_form, base_height_form=base_height_form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    if base_height_form.validate_on_submit():
        base = float(base_height_form.base.data)
        height = float(base_height_form.height.data)
        area_base_height = round(0.5 * base * height, 10)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Triangle area calculator", input1="base height",
                                                input2=base,
                                                input3=height, input4=None, input5=None, input6=None,
                                                result=area_base_height,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("triangle_area_calculator.html", area_base_height=area_base_height,
                               base_height_form=base_height_form, heron_form=heron_form, year=year,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("triangle_area_calculator.html", heron_form=heron_form, base_height_form=base_height_form,
                           year=year, display_other=True, sign_in_recommended=current_user.is_authenticated)


@app.route("/hypotenuse-calculator", methods=["GET", "POST"])
def hypotenuse_calculator():
    form = HypotenuseCalculator()

    if form.validate_on_submit():
        a = float(form.a.data)
        b = float(form.b.data)
        hypotenuse = round(math.sqrt(a ** 2 + b ** 2), 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Hypotenuse calculator", input1=a, input2=b,
                                                input3=None, input4=None, input5=None, input6=None, result=hypotenuse,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("hypotenuse_calculator.html", hypotenuse=hypotenuse, year=year, form=form,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("hypotenuse_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/triangular-prism-calculator", methods=["GET", "POST"])
def triangular_prism_calculator():
    form = TriangularPrismCalculator()

    if form.validate_on_submit():
        a = float(form.a.data)
        b = float(form.b.data)
        c = float(form.c.data)
        s = (a + b + c) / 2
        height = float(form.height.data)

        try:
            round(math.sqrt(s * (s - a) * (s - b) * (s - c)), 2)
        except ValueError:
            volume = "The side lengths you provided cannot make a triangle"
            surface_area = None
        else:
            if (a + b <= c) or (b + c <= a) or (a + c <= b):
                volume = "The side lengths you provided cannot make a triangle"
                surface_area = None
            else:
                surface_area = round(2 * math.sqrt(s * (s - a) * (s - b) * (s - c)) + height * (a + b + c), 2)
                volume = round(math.sqrt(s * (s - a) * (s - b) * (s - c)) * height, 2)

                if current_user.is_authenticated:
                    calculation = UserSavedCalculations(calculator="Triangular prism calculator", input1=a, input2=b,
                                                        input3=c, input4=height, input5=None, input6=None,
                                                        result=surface_area, result2=volume, result3=None, result4=None,
                                                        user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
                    db.session.add(calculation)
                    db.session.commit()

        return render_template("triangular_prism_calculator.html", surface_area=surface_area, volume=volume, form=form,
                               year=year, display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("triangular_prism_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/trapezoid-area-calculator", methods=["GET", "POST"])
def trapezoid_area_calculator():
    form = TrapezoidAreaCalculator()

    if form.validate_on_submit():
        a = float(form.a.data)
        b = float(form.b.data)
        height = float(form.height.data)
        area = round(height * ((a + b) / 2), 10)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Trapezoid area calculator", input1=a, input2=b,
                                                input3=height, input4=None, input5=None, input6=None, result=area,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("trapezoid_area_calculator.html", area=area, year=year, form=form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("trapezoid_area_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/hexagon-area-calculator", methods=["GET", "POST"])
def hexagon_area_calculator():
    form = HexagonAreaCalculator()

    if form.validate_on_submit():
        side = float(form.side.data)
        area = round((side ** 2) * (3 * (3 ** 0.5)) / 2, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Hexagon area calculator", input1=side, input2=None,
                                                input3=None, input4=None, input5=None, input6=None, result=area,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("hexagon_area_calculator.html", area=area, year=year, form=form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("hexagon_area_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/circle-calculator", methods=["GET", "POST"])
def circle_calculator():
    area_form = CircleAreaCalculator()
    circumference_form = CircleCircumferenceCalculator()

    if circumference_form.validate_on_submit():
        diameter = float(circumference_form.diameter.data)
        circumference = round(diameter * math.pi, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Circle calculator", input1="circumference", input2=diameter,
                                                input3=None, input4=None, input5=None, input6=None,
                                                result=circumference,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("circle_calculator.html", circumference=circumference, year=year,
                               circumference_form=circumference_form, area_form=area_form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    elif area_form.validate_on_submit():
        radius = float(area_form.radius.data)
        area = round((radius ** 2) * math.pi, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Circle calculator", input1="area", input2=radius,
                                                input3=None, input4=None, input5=None, input6=None, result=area,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("circle_calculator.html", area=area, year=year,
                               circumference_form=circumference_form, area_form=area_form, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("circle_calculator.html", area_form=area_form, circumference_form=circumference_form,
                           year=year, display_other=True, sign_in_recommended=current_user.is_authenticated)


@app.route("/ellipse-area-calculator", methods=["GET", "POST"])
def ellipse_area_calculator():
    form = EllipseAreaCalculator()

    if form.validate_on_submit():
        a = float(form.a.data)
        b = float(form.b.data)
        area = round(math.pi * a * b, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Ellipse area calculator", input1=a,
                                                input2=b, input3=None, input4=None, input5=None, input6=None,
                                                result=area,
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("ellipse_area_calculator.html", area=area, year=year, form=form,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("ellipse_area_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/sphere-calculator", methods=["GET", "POST"])
def sphere_calculator():
    form = SphereCalculator()

    if form.validate_on_submit():
        radius = float(form.radius.data)
        surface_area = round(4 * math.pi * radius ** 2, 2)
        volume = round((4 / 3) * math.pi * radius ** 3, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Sphere calculator", input1=radius,
                                                input2=None, input3=None, input4=None, input5=None, input6=None,
                                                result=surface_area,
                                                result2=volume, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("sphere_calculator.html", surface_area=surface_area, volume=volume, year=year, form=form,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("sphere_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/cylinder-calculator", methods=["GET", "POST"])
def cylinder_calculator():
    form = CylinderCalculator()

    if form.validate_on_submit():
        radius = float(form.radius.data)
        height = float(form.height.data)
        surface_area = round(2 * math.pi * radius ** 2 + 2 * radius * math.pi * height, 2)
        volume = round(math.pi * height * radius ** 2, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Cylinder calculator", input1=radius,
                                                input2=height, input3=None, input4=None, input5=None, input6=None,
                                                result=surface_area, result2=volume, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("cylinder_calculator.html", surface_area=surface_area, volume=volume, year=year,
                               form=form, display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("cylinder_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/regular-polygon-area-calculator", methods=["GET", "POST"])
def regular_polygon_area_calculator():
    form = RegularPolygonAreaCalculator()

    if form.validate_on_submit():
        side_number = float(form.side_number.data)
        side_length = float(form.side_length.data)
        apothem = float(form.apothem.data)
        area = round(0.5 * apothem * side_length * side_number, 2)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Regular polygon area calculator", input1=side_number,
                                                input2=side_length, input3=apothem, input4=None, input5=None,
                                                input6=None, result=area, result2=None, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("regular_polygon_area_calculator.html", area=area, year=year, form=form,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("regular_polygon_area_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


# Business calculators
@app.route("/simple-interest-calculator", methods=["GET", "POST"])
def simple_interest_calculator():
    form = SimpleInterestCalculator()

    if form.validate_on_submit():
        principal = float(form.principal.data)
        interest_rate = float(form.interest_rate.data)
        time = int(form.time.data)
        final_amount = round(principal * (1 + (interest_rate / 100) * time), 2)
        interest_per_year = interest_rate / 100 * principal
        yearly_amount = [amount_year * interest_per_year + principal for amount_year in range(time + 1)]
        yearly_amount = [round(rounded_amount, 2) for rounded_amount in yearly_amount]
        years = [interest_year for interest_year in range(time + 1)]

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Simple interest calculator", input1=principal,
                                                input2=interest_rate, input3=time, input4=None, input5=None,
                                                input6=None, result=f"${final_amount}",
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("simple_interest_calculator.html", final_amount=final_amount, year=year, form=form,
                               yearly_amount=yearly_amount, years=years, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("simple_interest_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/compound-interest-calculator", methods=["GET", "POST"])
def compound_interest_calculator():
    form = CompoundInterestCalculator()

    if form.validate_on_submit():
        principal = float(form.principal.data)
        interest_rate = float(form.interest_rate.data)
        time = int(form.time.data)
        times_period = form.times_period.data
        times_period_number = 0
        if times_period == "Daily":
            times_period_number = 365
        elif times_period == "Monthly":
            times_period_number = 12
        elif times_period == "Quarterly":
            times_period_number = 4
        elif times_period == "Semiannually":
            times_period_number = 2
        elif times_period == "Annually":
            times_period_number = 1

        final_amount = round(
            principal * (1 + ((interest_rate / 100) / times_period_number)) ** (time * times_period_number), 2)

        yearly_amount_complete = [principal]

        for i in range(1, (time + 1) * times_period_number - 1):
            yearly_amount_complete.append(
                yearly_amount_complete[i - 1] * (1 + ((interest_rate / 100) / times_period_number)))

        if times_period == "Annually":
            yearly_amount = yearly_amount_complete
            yearly_amount.append(yearly_amount_complete[-1] * (1 + ((interest_rate / 100) / times_period_number)))
        else:
            yearly_amount = []
            for amount in yearly_amount_complete:
                if (yearly_amount_complete.index(amount)) % times_period_number == 0:
                    yearly_amount.append(amount)

        yearly_amount = [round(rounded_amount, 2) for rounded_amount in yearly_amount]

        years = [interest_year for interest_year in range(time + 1)]

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Compound interest calculator", input1=principal,
                                                input2=interest_rate, input3=times_period, input4=time, input5=None,
                                                input6=None, result=f"${final_amount}",
                                                result2=None, result3=None, result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("compound_interest_calculator.html", final_amount=final_amount, year=year, years=years,
                               yearly_amount=yearly_amount, frequency=times_period.lower(), form=form,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("compound_interest_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/depreciation-calculator", methods=["GET", "POST"])
def depreciation_calculator():
    form = DepreciationCalculator()

    if form.validate_on_submit():
        asset_cost = float(form.asset_cost.data)
        salvage_value = float(form.salvage_value.data)
        useful_life = float(form.useful_life.data)
        final_amount = round((asset_cost - salvage_value) / useful_life, 2)

        if final_amount == 0.0:
            final_amount = 0.00

        if current_user.is_authenticated:
            if final_amount != 0.0:
                calculation = UserSavedCalculations(calculator="Depreciation calculator", input1=asset_cost,
                                                    input2=salvage_value,
                                                    input3=useful_life, input4=None, input5=None, input6=None,
                                                    result=f"${final_amount}",
                                                    result2=None, result3=None, result4=None, user_id=current_user.id,
                                                    date=now.date().strftime("%m/%d/%Y"))
                db.session.add(calculation)
                db.session.commit()
            else:
                calculation = UserSavedCalculations(calculator="Depreciation calculator", input1=asset_cost,
                                                    input2=salvage_value, input3=useful_life, input4=None, input5=None,
                                                    input6=None,
                                                    result="$0.00", result2=None, result3=None, result4=None,
                                                    user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
                db.session.add(calculation)
                db.session.commit()

        return render_template("depreciation_calculator.html", asset_cost=asset_cost, salvage_value=salvage_value,
                               final_amount=final_amount, form=form, year=year, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("depreciation_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/roi-calculator", methods=["GET", "POST"])
def roi_calculator():
    form = ROICalculator()

    if form.validate_on_submit():
        initial_value = float(form.initial_value.data)
        final_value = float(form.final_value.data)
        cost = float(form.cost.data)
        roi = round(((final_value - initial_value) / cost) * 100, 1)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="ROI calculator", input1=initial_value,
                                                input2=final_value, input3=cost, input4=None, input5=None, input6=None,
                                                result=roi, result2=None, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("roi_calculator.html", roi=roi, form=form, year=year, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("roi_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


# Other calculators
@app.route("/bmi-calculator", methods=["GET", "POST"])
def bmi_calculator():
    form = BMICalculator()

    if form.validate_on_submit():
        feet = float(form.feet.data)
        inches = float(form.inches.data)
        weight = float(form.weight.data)
        bmi = round((weight / (feet * 12 + inches) ** 2) * 703, 1)

        if bmi < 18.5:
            result = "underweight"
        elif 18.5 <= bmi <= 24.9:
            result = "healthy weight"
        elif 25 <= bmi <= 29.9:
            result = "overweight"
        else:
            result = "obese"

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="BMI calculator", input1=feet, input2=inches,
                                                input3=weight, input4=None, input5=None, input6=None, result=bmi,
                                                result2=f"Your BMI falls into the {result} category", result3=None,
                                                result4=None, user_id=current_user.id,
                                                date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("bmi_calculator.html", bmi=bmi, result=result, form=form, year=year, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("bmi_calculator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/dice-roller", methods=["GET", "POST"])
def dice_roller():
    form = DiceRoller()

    if form.validate_on_submit():
        sides = int(form.sides.data)
        result = random.randint(1, sides)

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Dice roller", input1=sides,
                                                input2=None, input3=None, input4=None, input5=None, input6=None,
                                                result=result, result2=None, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("dice_roller.html", sides=sides, result=result, form=form, year=year,
                               display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("dice_roller.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/hash-generator", methods=["GET", "POST"])
def hash_generator():
    form = HashGenerator()

    if form.validate_on_submit():
        hash_type = form.hash_type.data
        string = form.string.data
        hashed_string = ""

        if hash_type == "MD5":
            hashed_string = hashlib.md5(string.encode()).hexdigest()
        elif hash_type == "SHA256":
            hashed_string = hashlib.sha256(string.encode()).hexdigest()
        elif hash_type == "SHA1":
            hashed_string = hashlib.sha1(string.encode()).hexdigest()
        elif hash_type == "SHA224":
            hashed_string = hashlib.sha224(string.encode()).hexdigest()
        elif hash_type == "SHA384":
            hashed_string = hashlib.sha384(string.encode()).hexdigest()
        elif hash_type == "SHA512":
            hashed_string = hashlib.sha512(string.encode()).hexdigest()
        elif hash_type == "BLAKE2B":
            hashed_string = hashlib.blake2b(string.encode()).hexdigest()
        elif hash_type == "BLAKE2S":
            hashed_string = hashlib.blake2s(string.encode()).hexdigest()

        if current_user.is_authenticated:
            calculation = UserSavedCalculations(calculator="Hash generator", input1=hash_type, input2=string,
                                                input3=None, input4=None, input5=None, input6=None,
                                                result=hashed_string, result2=None, result3=None, result4=None,
                                                user_id=current_user.id, date=now.date().strftime("%m/%d/%Y"))
            db.session.add(calculation)
            db.session.commit()

        return render_template("hash_generator.html", hash_type=hash_type, hashed_string=hashed_string, form=form,
                               year=year, display_other=True, sign_in_recommended=current_user.is_authenticated)

    return render_template("hash_generator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


@app.route("/password-generator", methods=["GET", "POST"])
def password_generator():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
    capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                       'U', 'V', 'W', 'X', 'Y', 'Z']
    special_characters = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', "'",
                          '|', "]", '[', ':', '>', '<', ';', "'", '/', '.', ]

    form = PasswordGenerator()

    if form.validate_on_submit():
        password_length = int(form.password_length.data)
        include_capital_letters = form.include_capital_letters.data
        include_numbers = form.include_numbers.data
        include_special_characters = form.include_special_characters.data
        character_set = lowercase_letters

        if include_numbers:
            character_set += numbers

        if include_capital_letters:
            character_set += capital_letters

        if include_special_characters:
            character_set += special_characters

        password = ""

        for character in range(password_length):
            password += str(random.choice(character_set))

        return render_template("password_generator.html", form=form, password=password, include_numbers=include_numbers,
                               include_capital_letters=include_capital_letters,
                               include_special_characters=include_special_characters, year=year, display_other=True,
                               sign_in_recommended=current_user.is_authenticated)

    return render_template("password_generator.html", form=form, year=year, display_other=True,
                           sign_in_recommended=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=False)
