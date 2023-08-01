from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, ValidationError
from wtforms.validators import InputRequired


class CompoundInterestCalculator(FlaskForm):
    principal = StringField("Principal amount ($)", default="", validators=[InputRequired()])
    interest_rate = StringField("Interest rate (%)", default="", validators=[InputRequired()])
    times_period = SelectField("Times compounded per year",
                               choices=["Daily", "Monthly", "Quarterly", "Semiannually", "Annually"])
    time = StringField("Investment time span (years)", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_principal(self, principal):
        try:
            float(principal.data)
        except ValueError:
            raise ValidationError("Principal amount must be a number")

        if float(principal.data) <= 0:
            raise ValidationError("Principal amount must be positive")

    def validate_interest_rate(self, interest_rate):
        try:
            float(interest_rate.data)
        except ValueError:
            raise ValidationError("Interest rate must be a number")

        if float(interest_rate.data) <= 0:
            raise ValidationError("Interest rate must be positive")

    def validate_time(self, time):
        try:
            float(time.data)
        except ValueError:
            raise ValidationError("Investment time span must be a number")

        try:
            int(time.data)
        except ValueError:
            raise ValidationError("Investment time span must be a positive integer")

        if float(time.data) <= 0:
            raise ValidationError("Investment time span must be a positive integer")

        if int(time.data) < 1 or int(time.data) > 50:
            raise ValidationError("Investment time span must be between 1 and 50 years")


class SimpleInterestCalculator(FlaskForm):
    principal = StringField("Principal amount ($)", default="", validators=[InputRequired()])
    interest_rate = StringField("Interest rate (%)", default="", validators=[InputRequired()])
    time = StringField("Investment time span (years)", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_principal(self, principal):
        try:
            float(principal.data)
        except ValueError:
            raise ValidationError("Principal amount must be a number")

        if float(principal.data) <= 0:
            raise ValidationError("Principal amount must be positive")

    def validate_interest_rate(self, interest_rate):
        try:
            float(interest_rate.data)
        except ValueError:
            raise ValidationError("Interest rate must be a number")

        if float(interest_rate.data) <= 0:
            raise ValidationError("Interest rate must be positive")

    def validate_time(self, time):
        try:
            float(time.data)
        except ValueError:
            raise ValidationError("Investment time span must be a number")

        try:
            int(time.data)
        except ValueError:
            raise ValidationError("Investment time span must be a positive integer")

        if float(time.data) <= 0:
            raise ValidationError("Investment time span must be a positive integer")

        if int(time.data) < 1 or int(time.data) > 50:
            raise ValidationError("Investment time span must be between 1 and 50 years")


class DepreciationCalculator(FlaskForm):
    asset_cost = StringField("Asset cost ($)", default="", validators=[InputRequired()])
    salvage_value = StringField("Salvage value ($)", default="", validators=[InputRequired()])
    useful_life = StringField("Useful life (years)", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_asset_cost(self, asset_cost):
        try:
            float(asset_cost.data)
        except ValueError:
            raise ValidationError("Asset cost must be a number")

        if float(asset_cost.data) <= 0:
            raise ValidationError("Asset cost must be positive")

    def validate_salvage_value(self, salvage_value):
        try:
            float(salvage_value.data)
        except ValueError:
            raise ValidationError("Salvage value must be a number")

        if float(salvage_value.data) <= 0:
            raise ValidationError("Salvage value must be positive")

    def validate_useful_life(self, useful_life):
        try:
            float(useful_life.data)
        except ValueError:
            raise ValidationError("Useful life must be a number")

        if float(useful_life.data) <= 0:
            raise ValidationError("Useful life must be positive")

    def validate_depreciation_rate(self, depreciation_rate):
        try:
            float(depreciation_rate.data)
        except ValueError:
            raise ValidationError("Depreciation rate must be a number")

        if float(depreciation_rate.data) <= 0:
            raise ValidationError("Depreciation rate must be positive")


class ROICalculator(FlaskForm):
    initial_value = StringField("Initial investment value", default="", validators=[InputRequired()])
    final_value = StringField("Final investment value", default="", validators=[InputRequired()])
    cost = StringField("Cost of investment", default="", validators=[InputRequired()])
    submit = SubmitField("Calculate")

    def validate_initial_value(self, initial_value):
        try:
            float(initial_value.data)
        except ValueError:
            raise ValidationError("Initial investment value must be a number")

        if float(initial_value.data) <= 0:
            raise ValidationError("Initial investment value must be positive")

    def validate_final_value(self, final_value):
        try:
            float(final_value.data)
        except ValueError:
            raise ValidationError("Final investment value must be a number")

        if float(final_value.data) < 0:
            raise ValidationError("Final investment value must be nonnegative")

    def validate_cost(self, cost):
        try:
            float(cost.data)
        except ValueError:
            raise ValidationError("Cost of investment must be a number")

        if float(cost.data) <= 0:
            raise ValidationError("Cost of investment must be positive")
