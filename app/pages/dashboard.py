from fasthtml.common import *

def getHTML():
    return Div(
        H1("Scarf Dashboard", cls="centered"),
            Div(
                Div(
                H2("Editor"),
                    Div(
                        Button("New Scarf", hx_get="/scarf/recipe/form", hx_target="#editor_pane"),
                        id="editor_pane"

                    ),
                    cls = "column"
                     ),
                    Div(
                    H2("Column 2"),
                        P(
                            "P2",
                            id="scarf-card"
                        ),
                        cls = "column"
                    ),
                    cls ="container"
            )

    )