import os
import secrets

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileAllowed, FileField, FileRequired
from image_processing import (
    image_color_distribution,
    mark_plot,
    open_image,
)
from werkzeug.utils import secure_filename
from wtforms import DecimalField, RadioField, SelectField, SubmitField, BooleanField
from wtforms.validators import NumberRange

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["RECAPTCHA_USE_SSL"] = False
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LcsgX0pAAAAAC24mMVYI61PGxBsU5YP9C8B_KaR"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LcsgX0pAAAAAJXAad63oZwYrwjIAHoWD9EvdjUo"
app.config["RECAPTCHA_OPTIONS"] = {"theme": "dark"}
bootstrap = Bootstrap(app)


class ImageForm(FlaskForm):
    cross_position = SelectField(
        "Position of the cross",
        choices=[
            ("horizontal", "Horizontal"),
            ("vertical", "Vertical"),
        ],
        render_kw={
            "style": "margin-bottom: 12px;  background-color: transparent; border: 1px solid #3c3c3c",
            "class": "cross_position"
        }
    )
    upload_image = FileField(
        "Uploading an image",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "png", "jpeg"], "Incorrect image format"
            ),
        ],
        description="jpg, png, jpeg",
        render_kw={"style": "display: flex; margin-bottom: 12px;"}
    )
    percent_red = DecimalField(
        label="Percent red",
        validators=[
            NumberRange(
                min=0, max=100, message="The value must be in the range from 0 to 100"
            ),
        ],
        render_kw={"style": "margin-bottom: 12px;"}
    )
    percent_green = DecimalField(
        label="Green percentage",
        validators=[
            NumberRange(
                min=0, max=100, message="The value must be in the range from 0 to 100"
            ),
        ],
        render_kw={"style": "margin-bottom: 12px;"}
    )
    percent_blue = DecimalField(
        label="Blue percentage",
        validators=[
            NumberRange(
                min=0, max=100, message="The value must be in the range from 0 to 100"
            ),
        ],
        render_kw={"style": "margin-bottom: 12px;"}
    )
    original_image_color_option = BooleanField(
        "Display the color of the original image",
    )
    processed_image_color_option = BooleanField(
        "Displaying the color of the processed image",
    )
    google_recaptcha = RecaptchaField(
        render_kw={"style": "display: flex; justify-content: center"}
    )
    submit = SubmitField("Processing...", render_kw={"style": "margin-top: 12px; padding: 10px 20px; display: flex; justify-content: center"})


@app.route("/", methods=["GET", "POST"])
def default_router():
    form = ImageForm()
    filename = None
    save_file = None
    save_color_image = None
    save_color_new_image = None
    try:
        if form.validate_on_submit():
            filename = os.path.join(
                "./static", secure_filename(form.upload_image.data.filename)
            )
            form.upload_image.data.save(filename)
            fimage = open_image(filename)

            percent_red = form.percent_red.data / 100
            percent_green = form.percent_green.data / 100
            percent_blue = form.percent_blue.data / 100
            decode = mark_plot(
                fimage,
                r=percent_red,
                g=percent_green,
                b=percent_blue,
                horisontal=(False if form.cross_position.data == "horizontal" else True),
            )
            if decode is not None:
                print("decode", decode)

                split_filename = filename.split(os.sep)
                save_file = (
                        os.sep.join(split_filename[:-1])
                        + os.sep
                        + "mark"
                        + split_filename[-1]
                )

                if form.original_image_color_option.data is True:
                    save_color_image = (
                            os.sep.join(split_filename[:-1])
                            + os.sep
                            + form.cross_position.data
                            + "_colors_"
                            + ".png"
                    )
                if form.processed_image_color_option.data is True:
                    save_color_new_image = (
                            os.sep.join(split_filename[:-1])
                            + os.sep
                            + form.cross_position.data
                            + "_colors_new_"
                            + ".png"
                    )
            else:
                save_file = None
            if save_file is not None:
                decode.save(save_file)
            if save_color_image is not None:
                colored = image_color_distribution(filename)
                colored.savefig(
                    save_color_image, bbox_inches="tight", pad_inches=0, dpi=1000
                )
            if save_color_new_image is not None:
                colored = image_color_distribution(save_file)
                colored.savefig(
                    save_color_new_image, bbox_inches="tight", pad_inches=0, dpi=1000
                )
    except Exception as error:
        print(save_file)
    return render_template(
        "index.html",
        form=form,
        image_name=filename,
        image_name_proc=save_file,
        save_color_new_image=save_color_new_image,
        save_color_image=save_color_image,
    )


@app.route("/info")
def info():
    return render_template(
        "info.html",
        title="about",
    )


if __name__ == "__main__":
    app.run(host="localhost", port=6001)
