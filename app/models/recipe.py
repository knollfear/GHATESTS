from fasthtml.common import *
import webcolors
from components.colorswatch import  ColorSwatch

# Get a list of all HTML color names
html_colors = list(webcolors._definitions._CSS3_NAMES_TO_HEX.keys())
print(html_colors)

@dataclass
class Recipe():
    Id: int
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
            Id: int,
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
        self.Id = Id
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
            Input(name="id", style={"display": "none"}),
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
                   value="",
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


    def EditForm(self):
        return Form(
            Input(name="id", style={"display": "none"}, value=self.Id),
        Label('Name', Input(name="name", value=self.Name)),
            Fieldset(
                Legend("Colors:"),
                Select(
                    *[Option(option, value=option, selected=(option==self.PrimaryColor) ) for option in html_colors],
                    name="primarycolor",
                    hx_get="/scarf/component/color-swatch",
                    hx_target="#primarycolorpreview"
                ),

                Div(
                    ColorSwatch(self.PrimaryColor).toHTML(),
                    id="primarycolorpreview"
                ),
                Select(
                  *[Option(option, value=option, selected=(option==self.SecondaryColor)) for option in html_colors],
                   value=self.SecondaryColor,
                   name="secondarycolor",
                   hx_get="/scarf/component/color-swatch",
                   hx_target="#secondarycolorpreview"
                ),

                Div(
                ColorSwatch(self.SecondaryColor).toHTML(),
                    id="secondarycolorpreview"
                ),
                Select(
                  *[Option(option, value=option, selected=(option==self.AccentColor)) for option in html_colors],
                   name="accentcolor",
                   hx_get="/scarf/component/color-swatch",
                   hx_target="#accentcolorpreview"
                ),
                Div(
                ColorSwatch(self.AccentColor).toHTML(),
                    id="accentcolorpreview"
                ),
            ),
            Fieldset(
                Legend("Scarf Types:"),
                Label( "Veil", Input(name="veil", type="checkbox", checked=self.Veil)),
                Label( "Triangle", Input(name="triangle", type="checkbox", checked=self.Triangle)),
                Label( "Shawl", Input(name="shawl", type="checkbox", checked=self.Shawl)),
                Label("Infinity", Input(name="infinity", type="checkbox", checked=self.Infinity)),
            ),
            Label("Notes", Input(name="notes", type="textarea", value=self.Notes)),
            Button("Save", hx_post=f"/scarf/recipe/update/{self.Id}", hx_target="#scarf-card"),
        )

    @classmethod
    def FromFormData(cls, formData):
        return Recipe(
            formData.get("id") or None,
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


    @classmethod
    def ResultToFormData(cls, result):

        formData = {
            "id": result[0],
            "name": result[1],
            "primarycolor": result[2],
            "secondarycolor": result[3],
            "accentcolor": result[4],
            "veil": "on" if result[5] else "",
            "triangle": "on" if result[6] else "",
            "shawl": "on" if result[7] else "",
            "infinity": "on" if result[8] else "",
            "notes": result[9]
        }

        return formData


    def Row(self):
        return Tr(
            Td(self.Name),
            Td(
                Group(
                    ColorSwatch(self.PrimaryColor).toHTML(),
                    ColorSwatch(self.SecondaryColor).toHTML(),
                    ColorSwatch(self.AccentColor).toHTML()
                )
            ),
            Td(
                ("Veil, " if self.Veil else "") +
                ("Triangle, " if self.Triangle else "") +
                ("Shawl, " if self.Shawl else "") +
                ("Infinity " if self.Infinity else "")
            ),
            Td(self.Notes),
            Td(
                Group(
                Button("Edit", hx_get=f"/scarf/recipe/edit/{self.Id}", hx_target="#scarf-card"),
                Button("Details", hx_get=f"/scarf/recipe/{self.Id}", hx_target="#scarf-card"),
                )
            )
        )

    @classmethod
    def TableFromResults(cls, results):
        return Table(
            Thead(
                Tr(
                    Th("Name"),
                    Th("Colors"),
                    Th("Products"),
                    Th("Notes"),
                    Th("")
                )
            ),
            Tbody(
                *[Recipe.FromFormData(Recipe.ResultToFormData(recipe)).Row() for recipe in results]
            )
        )


    def Card(self):
        return Card(
        Div(
                Group(
                    ColorSwatch(self.PrimaryColor).toHTML(),
                    ColorSwatch(self.SecondaryColor).toHTML(),
                    ColorSwatch(self.AccentColor).toHTML(),
                )
            ),
            header=P(self.Name),

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