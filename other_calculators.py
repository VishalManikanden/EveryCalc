from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, ValidationError
from wtforms.validators import InputRequired


class BMICalculator(FlaskForm):
    feet = StringField("Height (feet)", default="", validators=[InputRequired()])
    inches = StringField("Height (inches)", default="", validators=[InputRequired()])
    weight = StringField("Weight (pounds)", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_feet(self, feet):
        try:
            float(feet.data)
        except ValueError:
            raise ValidationError("Height must be a number")

        if float(feet.data) <= 0:
            raise ValidationError("Height must be positive")

    def validate_inches(self, inches):
        try:
            float(inches.data)
        except ValueError:
            raise ValidationError("Height must be a number")

        if float(inches.data) <= 0:
            raise ValidationError("Height must be positive")

    def validate_weight(self, weight):
        try:
            float(weight.data)
        except ValueError:
            raise ValidationError("Weight must be a number")

        if float(weight.data) <= 0:
            raise ValidationError("Weight must be positive")


class DiceRoller(FlaskForm):
    sides = StringField("Number of faces", default="", validators=[InputRequired()])
    submit = SubmitField("Roll")

    def validate_sides(self, sides):
        try:
            int(sides.data)
        except ValueError:
            raise ValidationError("Number of sides must be an integer")

        if float(sides.data) <= 0:
            raise ValidationError("Number of sides must be positive")


class HashGenerator(FlaskForm):
    hash_type = SelectField("Hash type",
                            choices=["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512", "BLAKE2B", "BLAKE2S"])
    string = StringField("String", default="", validators=[InputRequired()])
    submit = SubmitField("Generate")


class PasswordGenerator(FlaskForm):
    password_length = StringField("Password length", default="", validators=[InputRequired()])
    include_capital_letters = BooleanField("Include capital letters")
    include_numbers = BooleanField("Include numbers")
    include_special_characters = BooleanField("Include special characters")

    def validate_password_length(self, password_length):
        try:
            float(password_length.data)
        except ValueError:
            raise ValidationError("Password length must be a number")

        try:
            int(password_length.data)
        except ValueError:
            raise ValidationError("Password length must be a positive integer")

        if float(password_length.data) <= 0:
            raise ValidationError("Password length must be a positive integer")

        if int(password_length.data) < 1 or int(password_length.data) > 100:
            raise ValidationError("Password length must be between 1 and 100 characters")
