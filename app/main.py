from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get():
    print("GOT A REQUEST FOR '/'")
    return Div(P('Hello World!'), hx_get="/change")

@rt('/change')
def get():
    print("GOT A REQUEST FOR '/change'")
    return Div(P('Hello EVERYONE'), hx_get="/")

serve(80)