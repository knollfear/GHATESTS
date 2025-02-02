from fasthtml.common import *
import webcolors

# Get a list of all HTML color names
html_colors = list(webcolors._definitions._CSS3_NAMES_TO_HEX.keys())
print(html_colors)


class Recipe():
    Name: str
    PrimaryColor: str
    SecondaryColor: str
    AccentColor: str
    Veil: bool
    Triangle: bool
    Shawl: bool
    Infinity: bool
    Notes: str

    def __init__(
            self,
            Name: str,
            PrimaryColor: str,
            SecondaryColor: str,
            AccentColor: str,
            Veil: bool,
            Triangle: bool,
            Shawl: bool,
            Infinity: bool,
            Notes: str = "",  # Optional parameter with a default value
    ):
        """
        Initialize a Recipe object with the given attributes.

        :param Name: The name of the recipe.
        :param PrimaryColor: The primary color of the recipe.
        :param SecondaryColor: The secondary color of the recipe.
        :param AccentColor: The accent color of the recipe.
        :param Veil: Whether the recipe includes a veil.
        :param Triangle: Whether the recipe includes a triangle.
        :param Shawl: Whether the recipe includes a shawl.
        :param Infinity: Whether the recipe includes an infinity.
        :param Notes: Additional notes about the recipe (optional).
        """
        self.Name = Name
        self.PrimaryColor = PrimaryColor
        self.SecondaryColor = SecondaryColor
        self.AccentColor = AccentColor
        self.Veil = Veil
        self.Triangle = Triangle
        self.Shawl = Shawl
        self.Infinity = Infinity
        self.Notes = Notes

    @classmethod
    def Form(cls):
        return Form(
        Label('Name', Input(name="name")),
            Fieldset(
                Legend("Colors:"),
                Select(
                    *[Option(option, value=option, style={"background-color": option}) for option in html_colors],
                    name="primarycolor",
                    hx_get="/scarf/component/color-swatch",
                    hx_target="#primarycolorpreview"
                ),

                Div(
                    "",
                    id="primarycolorpreview"
                ),
                Select(
                  *[Option(option, value=option) for option in html_colors],
                   name="secondarycolor",
                   hx_get="/scarf/component/color-swatch",
                   hx_target="#secondarycolorpreview"
                ),

                Div(
                    "",
                    id="secondarycolorpreview"
                ),
                Select(
                  *[Option(option, value=option) for option in html_colors],
                   name="accentcolor",
                   hx_get="/scarf/component/color-swatch",
                   hx_target="#accentcolorpreview"
                ),
                Div(
                    "",
                    id="accentcolorpreview"
                ),
            ),
            Fieldset(
                Legend("Scarf Types:"),
                Label( "Veil", Input(name="veil", type="checkbox")),
                Label( "Triangle", Input(name="triangle", type="checkbox")),
                Label( "Shawl", Input(name="shawl", type="checkbox")),
                Label("Infinity", Input(name="infinity", type="checkbox")),
            ),
            Label("Notes", Input(name="notes", type="textarea")),
            Button("Save", hx_post="/scarf/recipe/new", hx_target="#scarf-card"),
        )

    @classmethod
    def FromFormData(cls, formData):
        return Recipe(
            formData["name"],
            formData["primarycolor"],
            formData["secondarycolor"],
            formData["accentcolor"],
            formData.get("veil") == "on",
            formData.get("triangle") == "on",
            formData.get("shawl") == "on",
            formData.get("infinity") == "on",
            formData["notes"],
        )


    def Card(self):
        return Card(
        Div(
                Ol(
                    Li("Primary Color: " + self.PrimaryColor),
                    Li("Secondary Color: " + self.SecondaryColor),
                    Li("Accent Color: " + self.AccentColor),
                )
            ),
            header=P(self.Name),
            footer=P('foot')
        )

    @classmethod
    def CreateTable(cls, db):
        metadata = db.MetaData()
        Recipe = db.Table('Recipe', metadata,
                          db.Column('Id', db.Integer(), primary_key=True),
                          db.Column('Name', db.String(255), nullable=False),
                          db.Column('PrimaryColor', db.String(255), nullable=False),
                          db.Column('SecondaryColor', db.String(255), nullable=False),
                          db.Column('AccentColor', db.String(255), nullable=True),
                          db.Column('Veil', db.Boolean, default=True),
                          db.Column('Triangle', db.Boolean, default=True),
                          db.Column('Shawl', db.Boolean, default=True),
                          db.Column('Infinity', db.Boolean, default=True),
                          db.Column('Notes', db.String(511), nullable=True),
                          )
        return Recipe