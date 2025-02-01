from fasthtml.common import *
import data

app,rt = fast_app()
data.init()
setup_toasts(app)

@rt('/')
def get(request):
    print(request.query_params)
    print(request.url)


    return Title("Scarf Tracker", P(request.query_params), hx_get="/change")

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


serve()