from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import InputRequired


class CollatzConjectureCalculator(FlaskForm):
    number = StringField("Positive integer", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_number(self, number):
        try:
            float(number.data)
        except ValueError:
            raise ValidationError("Value must be a number")

        try:
            int(number.data)
        except ValueError:
            raise ValidationError("Value must be a positive integer")

        if float(number.data) <= 0:
            raise ValidationError("Value must be a positive integer")


class ArithmeticSequenceCalculator(FlaskForm):
    a = StringField("Initial term (a₁)", default="",  validators=[InputRequired()])
    term_number = StringField("Term number (n)", default="",  validators=[InputRequired()])
    d = StringField("Common difference (d)", default="",  validators=[InputRequired()])

    def validate_a(self, a):
        try:
            float(a.data)
        except ValueError:
            raise ValidationError("Initial term must be a number")

    def validate_term_number(self, term_number):
        try:
            float(term_number.data)
        except ValueError:
            raise ValidationError("Term number must be a number")

        try:
            int(term_number.data)
        except ValueError:
            raise ValidationError("Term number must be a positive integer")

        if float(term_number.data) <= 0:
            raise ValidationError("Term number must be a positive integer")

    def validate_d(self, d):
        try:
            float(d.data)
        except ValueError:
            raise ValidationError("Common difference must be a number")

        if float(d.data) == 0:
            raise ValidationError("Common difference cannot be 0")


class ArithmeticSeriesCalculator(FlaskForm):
    number_of_terms = StringField("Number of terms (n)", default="",  validators=[InputRequired()])
    initial_term = StringField("Initial term (a₁)", default="",  validators=[InputRequired()])
    n = StringField("Last term (aₙ)", default="",  validators=[InputRequired()])

    def validate_number_of_terms(self, number_of_terms):
        try:
            float(number_of_terms.data)
        except ValueError:
            raise ValidationError("Number of terms must be a number")

        try:
            int(number_of_terms.data)
        except ValueError:
            raise ValidationError("Number of terms must be a positive integer")

        if float(number_of_terms.data) <= 0:
            raise ValidationError("Number of terms must be a positive integer")

    def validate_initial_term(self, initial_term):
        try:
            float(initial_term.data)
        except ValueError:
            raise ValidationError("Initial term must be a number")

    def validate_n(self, n):
        try:
            float(n.data)
        except ValueError:
            raise ValidationError("Last term must be a number")


class GeometricSequenceCalculator(FlaskForm):
    initial_term = StringField("Initial term (a₁)", default="",  validators=[InputRequired()])
    term_number = StringField("Term number (term to be found)", default="",  validators=[InputRequired()])
    common_ratio = StringField("Common ratio (r)", default="",  validators=[InputRequired()])

    def validate_initial_term(self, initial_term):
        try:
            float(initial_term.data)
        except ValueError:
            raise ValidationError("Initial term must be a number")

    def validate_term_number(self, term_number):
        try:
            float(term_number.data)
        except ValueError:
            raise ValidationError("Term number must be a number")

        try:
            int(term_number.data)
        except ValueError:
            raise ValidationError("Term number must be a positive integer")

        if float(term_number.data) <= 0:
            raise ValidationError("Term number must be a positive integer")

    def validate_common_ratio(self, common_ratio):
        try:
            float(common_ratio.data)
        except ValueError:
            raise ValidationError("Common ratio must be a number")

        if float(common_ratio.data) == 0:
            raise ValidationError("Common ratio cannot be 0")


class GeometricSeriesCalculator(FlaskForm):
    first_term = StringField("Initial term (a₁)", default="",  validators=[InputRequired()])
    number_of_terms = StringField("Number of terms (n)", default="",  validators=[InputRequired()])
    ratio = StringField("Common ratio (r)", default="",  validators=[InputRequired()])

    def validate_first_term(self, first_term):
        try:
            float(first_term.data)
        except ValueError:
            raise ValidationError("Value must be a number")

    def validate_number_of_terms(self, number_of_terms):
        try:
            float(number_of_terms.data)
        except ValueError:
            raise ValidationError("Number of terms must be a number")

        try:
            int(number_of_terms.data)
        except ValueError:
            raise ValidationError("Number of terms must be a positive integer")

        if float(number_of_terms.data) <= 0:
            raise ValidationError("Number of terms must be a positive integer")

    def validate_ratio(self, ratio):
        try:
            float(ratio.data)
        except ValueError:
            raise ValidationError("Common ratio must be a number")

        if float(ratio.data) == 0:
            raise ValidationError("Common ratio cannot be 0")


class PermutationsCombinationsCalculator(FlaskForm):
    calculator_type = SelectField("", choices=["Permutation", "Combination"])
    n = StringField("Number of objects", default="",  validators=[InputRequired()])
    r = StringField("Number of objects being chosen", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_n(self, n):
        try:
            float(n.data)
        except ValueError:
            raise ValidationError("Number of objects must be a number")

        try:
            int(n.data)
        except ValueError:
            raise ValidationError("Number of objects must be a positive integer")

        if float(n.data) <= 0:
            raise ValidationError("Number of objects must be a positive integer")

    def validate_r(self, r):
        try:
            float(r.data)
        except ValueError:
            raise ValidationError("Number of objects being chosen must be a number")

        try:
            int(r.data)
        except ValueError:
            raise ValidationError("Number of objects being chosen must be a positive integer")

        if float(r.data) <= 0:
            raise ValidationError("Number of objects being chosen must be a positive integer")


class SlopeCalculator(FlaskForm):
    x1 = StringField("x₁", default="",  validators=[InputRequired()])
    x2 = StringField("x₂", default="", validators=[InputRequired()])
    y1 = StringField("y₁", default="", validators=[InputRequired()])
    y2 = StringField("y₂", default="", validators=[InputRequired()])

    def validate_x1(self, x1):
        try:
            float(x1.data)
        except ValueError:
            raise ValidationError("Point must be a number")

    def validate_x2(self, x2):
        try:
            float(x2.data)
        except ValueError:
            raise ValidationError("Point must be a number")

    def validate_y1(self, y1):
        try:
            float(y1.data)
        except ValueError:
            raise ValidationError("Point must be a number")

    def validate_y2(self, y2):
        try:
            float(y2.data)
        except ValueError:
            raise ValidationError("Point must be a number")


class RectangleAreaCalculator(FlaskForm):
    length = StringField("Length", default="",  validators=[InputRequired()])
    width = StringField("Width", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_length(self, length):
        try:
            float(length.data)
        except ValueError:
            raise ValidationError("Length must be a number")

        if float(length.data) <= 0:
            raise ValidationError("Length must be positive")

    def validate_width(self, width):
        try:
            float(width.data)
        except ValueError:
            raise ValidationError("Width must be a number")

        if float(width.data) <= 0:
            raise ValidationError("Width must be positive")


class RectangularPrismCalculator(FlaskForm):
    length = StringField("Length", default="",  validators=[InputRequired()])
    width = StringField("Width", default="", validators=[InputRequired()])
    height = StringField("Height", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_length(self, length):
        try:
            float(length.data)
        except ValueError:
            raise ValidationError("Length must be a number")

        if float(length.data) <= 0:
            raise ValidationError("Length must be positive")

    def validate_width(self, width):
        try:
            float(width.data)
        except ValueError:
            raise ValidationError("Width must be a number")

        if float(width.data) <= 0:
            raise ValidationError("Width must be positive")

    def validate_height(self, height):
        try:
            float(height.data)
        except ValueError:
            raise ValidationError("Height must be a number")

        if float(height.data) <= 0:
            raise ValidationError("Height must be positive")


class TriangleAreaCalculatorBaseHeight(FlaskForm):
    base = StringField("Base", default="",  validators=[InputRequired()])
    height = StringField("Height", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_base(self, base):
        try:
            float(base.data)
        except ValueError:
            raise ValidationError("Base must be a number")

        if float(base.data) <= 0:
            raise ValidationError("Base must be positive")

    def validate_height(self, height):
        try:
            float(height.data)
        except ValueError:
            raise ValidationError("Height must be a number")

        if float(height.data) <= 0:
            raise ValidationError("Height must be positive")


class TriangleAreaCalculatorHeron(FlaskForm):
    a = StringField("Side a length", default="",  validators=[InputRequired()])
    b = StringField("Side b length", default="", validators=[InputRequired()])
    c = StringField("Side c length", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_a(self, a):
        try:
            float(a.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(a.data) <= 0:
            raise ValidationError("Side length must be positive")

    def validate_b(self, b):
        try:
            float(b.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(b.data) <= 0:
            raise ValidationError("Side length must be positive")

    def validate_c(self, c):
        try:
            float(c.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(c.data) <= 0:
            raise ValidationError("Side length must be positive")


class HypotenuseCalculator(FlaskForm):
    a = StringField("Side a length (base)", default="",  validators=[InputRequired()])
    b = StringField("Side b length (height)", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_a(self, a):
        try:
            float(a.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(a.data) <= 0:
            raise ValidationError("Side length must be positive")

    def validate_b(self, b):
        try:
            float(b.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(b.data) <= 0:
            raise ValidationError("Side length must be positive")


class TriangularPrismCalculator(FlaskForm):
    height = StringField("Height (h)", default="",  validators=[InputRequired()])
    a = StringField("Side a length", default="",  validators=[InputRequired()])
    b = StringField("Side b length", default="", validators=[InputRequired()])
    c = StringField("Side c length", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_a(self, a):
        try:
            float(a.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(a.data) <= 0:
            raise ValidationError("Side length must be positive")

    def validate_b(self, b):
        try:
            float(b.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(b.data) <= 0:
            raise ValidationError("Side length must be positive")

    def validate_c(self, c):
        try:
            float(c.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(c.data) <= 0:
            raise ValidationError("Side length must be positive")

    def validate_height(self, height):
        try:
            float(height.data)
        except ValueError:
            raise ValidationError("Height must be a number")

        if float(height.data) <= 0:
            raise ValidationError("Height must be positive")


class TrapezoidAreaCalculator(FlaskForm):
    a = StringField("a (base)", default="",  validators=[InputRequired()])
    b = StringField("b (base)", default="",  validators=[InputRequired()])
    height = StringField("Height", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_a(self, a):
        try:
            float(a.data)
        except ValueError:
            raise ValidationError("Base must be a number")

        if float(a.data) <= 0:
            raise ValidationError("Base must be positive")

    def validate_b(self, b):
        try:
            float(b.data)
        except ValueError:
            raise ValidationError("Base must be a number")

        if float(b.data) <= 0:
            raise ValidationError("Base must be positive")

    def validate_height(self, height):
        try:
            float(height.data)
        except ValueError:
            raise ValidationError("Height must be a number")

        if float(height.data) <= 0:
            raise ValidationError("Height must be positive")


class HexagonAreaCalculator(FlaskForm):
    side = StringField("Side length", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_side(self, side):
        try:
            float(side.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(side.data) <= 0:
            raise ValidationError("Side length must be positive")


class CircleAreaCalculator(FlaskForm):
    radius = StringField("Radius (r)", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_radius(self, radius):
        try:
            float(radius.data)
        except ValueError:
            raise ValidationError("Radius must be a number")

        if float(radius.data) <= 0:
            raise ValidationError("Radius must be positive")


class CircleCircumferenceCalculator(FlaskForm):
    diameter = StringField("Diameter (d)", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_diameter(self, diameter):
        try:
            float(diameter.data)
        except ValueError:
            raise ValidationError("Diameter must be a number")

        if float(diameter.data) <= 0:
            raise ValidationError("Diameter must be positive")


class EllipseAreaCalculator(FlaskForm):
    a = StringField("Axis a length", default="",  validators=[InputRequired()])
    b = StringField("Axis b length", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_a(self, a):
        try:
            float(a.data)
        except ValueError:
            raise ValidationError("Axis length must be a number")

        if float(a.data) <= 0:
            raise ValidationError("Axis length must be positive")

    def validate_b(self, b):
        try:
            float(b.data)
        except ValueError:
            raise ValidationError("Axis length must be a number")

        if float(b.data) <= 0:
            raise ValidationError("Axis length must be positive")


class SphereCalculator(FlaskForm):
    radius = StringField("Radius", default="",  validators=[InputRequired()])

    def validate_radius(self, radius):
        try:
            float(radius.data)
        except ValueError:
            raise ValidationError("Radius must be a number")

        if float(radius.data) <= 0:
            raise ValidationError("Radius must be positive")


class CylinderCalculator(FlaskForm):
    radius = StringField("Radius", default="",  validators=[InputRequired()])
    height = StringField("Height", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_radius(self, radius):
        try:
            float(radius.data)
        except ValueError:
            raise ValidationError("Radius must be a number")

        if float(radius.data) <= 0:
            raise ValidationError("Radius must be positive")

    def validate_height(self, height):
        try:
            float(height.data)
        except ValueError:
            raise ValidationError("Height must be a number")

        if float(height.data) <= 0:
            raise ValidationError("Height must be positive")


class RegularPolygonAreaCalculator(FlaskForm):
    side_number = StringField("Number of sides", default="",  validators=[InputRequired()])
    side_length = StringField("Side length", default="",  validators=[InputRequired()])
    apothem = StringField("Apothem", default="",  validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_side_number(self, side_number):
        try:
            float(side_number.data)
        except ValueError:
            raise ValidationError("Number of sides must be a number")

        try:
            int(side_number.data)
        except ValueError:
            raise ValidationError("Number of sides must be a positive integer")

        if float(side_number.data) <= 0:
            raise ValidationError("Number of sides must be a positive integer")

    def validate_side_length(self, side_length):
        try:
            float(side_length.data)
        except ValueError:
            raise ValidationError("Side length must be a number")

        if float(side_length.data) <= 0:
            raise ValidationError("Side length must be positive")

    def validate_apothem(self, apothem):
        try:
            float(apothem.data)
        except ValueError:
            raise ValidationError("Apothem must be a number")

        if float(apothem.data) <= 0:
            raise ValidationError("Apothem must be positive")
