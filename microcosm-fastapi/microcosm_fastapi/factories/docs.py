from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from microcosm_fastapi.docs import get_doc_path


def configure_docs(graph):
    # Use locally hosted documentation dependencies for
    # additional security
    # https://github.com/tiangolo/fastapi/issues/2518
    graph.app.mount(
        "/static",
        StaticFiles(directory=get_doc_path("static")),
        name="static"
    )

    @graph.app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=graph.app.openapi_url,
            title=graph.app.title + " - Swagger UI",
            oauth2_redirect_url=graph.app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @graph.app.get(graph.app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @graph.app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=graph.app.openapi_url,
            title=graph.app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )
