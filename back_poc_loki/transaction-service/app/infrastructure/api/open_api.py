from fastapi.openapi.utils import get_openapi


def generate_openapi_schema(app_routes):
    return get_openapi(
        title='My API',
        version='1.0.0',
        description='This is an API description',
        routes=app_routes,
    )
