from flasgger import SwaggerView


class Inicio(SwaggerView):
    def get(self):
        return {}, 200
