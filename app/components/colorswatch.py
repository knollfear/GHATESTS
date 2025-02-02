from fasthtml.common import *

class ColorSwatch():
    color: str

    def __init__(self, color):
        self.color = color

    @classmethod
    def getColorFromQueryParams(cls, queryParams):
        return  queryParams.get('primarycolor') or queryParams.get('secondarycolor') or queryParams.get('accentcolor')

    def toHTML(self):
        return Div("", style={"background-color": self.color, "width": "100px", "height": "100px", "border-radius": "50px"})