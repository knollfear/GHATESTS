from fasthtml.common import *
import data
import models.recipe
import components.colorswatch
import pages.dashboard
import time

tailwind_css = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
global_style = Style("""
        /* Center the h1 header */
        h1 {
            text-align: center;
            font-family: Arial, sans-serif;
            
        }

        /* Create a container for the columns */
        .container {
            display: flex;
            justify-content: space-between;
            margin: 20px auto;
            max-width: 95vw;
            padding: 0 20px;
        }

        /* Style the columns */
        .column {
            flex: 1; /* Equal width for both columns */
            padding: 20px;
            border: 1px solid #ccc;
            margin: 0 10px;
            
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            color: #555;
        }

        /* Responsive design for smaller screens */
        @media (max-width: 600px) {
            .container {
                flex-direction: column;
            }
            .column {
                margin: 10px 0;
            }
        }
""")

app,rt = fast_app(hdrs=(global_style,))
data.init()
setup_toasts(app)
port = int(os.environ.get("port")) or 5001


@rt('/')
def get():
    return Div("Scarf Tracker", P("Hello World"), hx_get="/change")

@rt('/change')
def get():
    print("GOT A REQUEST FOR '/change'")
    return Div(P('Hello EVERYONE'), hx_get="/yolo")

@rt('/yolo')
def get():
    print("GOT A REQUEST FOR '/yolo'")
    return Div(P('Hello YOLO'), hx_get="/")

@rt('/users')
def get():
    profile_form = Form(
        Fieldset(
            Label('Name', Input(name="name")),
            Label('Email', Input(name="email")),
            Label("High Score", Input(name="highscore")),
        ),
        Button("Save", hx_post="/users" ),
    )
    return profile_form

@rt('/users')
async def post(request, session):
    formData = await parse_form(request)
    result = data.add_user(formData["name"], formData["email"], formData["highscore"])
    add_toast(session, f"User #{result.inserted_primary_key[0]} Saved", "success")
    return Button("Save", hx_post="/users" )


@rt('/users')
def get():
    profile_form = Form(
        Fieldset(
            Label('Name', Input(name="name")),
            Label('Email', Input(name="email")),
            Label("High Score", Input(name="highscore")),
        ),
        Button("Save", hx_post="/users" ),
    )
    return profile_form


@rt('/scarf/dashboard')
def get():
    return pages.dashboard.getHTML()

@rt('/scarf/recipe/form')
def get():
    return models.recipe.Recipe.Form()

@rt('/scarf/recipe/new')
async def post(request, session):
    formData = await parse_form(request)
    recipe = models.recipe.Recipe.FromFormData(formData)
    result = data.add_recipe(recipe)
    add_toast(session, f"Recipe #{result.inserted_primary_key[0]} Saved", "success")
    return recipe.Card()

@rt('/scarf/recipe/all')
def get():
    time.sleep(3)
    results = data.get_recipes()
    return models.recipe.Recipe.TableFromResults(results)


@rt('/scarf/recipe/edit/{id}')
def get(id:int):
    recipe = models.recipe.Recipe.FromFormData(models.recipe.Recipe.ResultToFormData(data.get_recipe(id)))

    return recipe.EditForm()

@rt('/scarf/recipe/update/{id}')
async def patch(request, session):
    formData = await parse_form(request)
    recipe = models.recipe.Recipe.FromFormData(formData)
    data.update_recipe(recipe)
    add_toast(session, f"Recipe #{formData["id"]} Updated", "success")
    return recipe.Card()


@rt('/scarf/recipe/{id}')
async def get(id:int):
    recipe = models.recipe.Recipe.FromFormData(models.recipe.Recipe.ResultToFormData(data.get_recipe(id)))

    return recipe.Card()



@rt('/scarf/component/color-swatch')
async def get(request):
    color = components.colorswatch.ColorSwatch.getColorFromQueryParams(request.query_params)
    return components.colorswatch.ColorSwatch(color).toHTML()

print("Serving on port " + str(port))
serve(port=port)