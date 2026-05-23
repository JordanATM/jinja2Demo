from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(title="Mini Web con Jinja2")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


productos = [
    {
        "id": 1,
        "nombre": "Laptop",
        "precio": 1200,
        "descripcion": "Una laptop potente para desarrollo."
    },
    {
        "id": 2,
        "nombre": "Mouse",
        "precio": 25,
        "descripcion": "Mouse inalámbrico ergonómico."
    },
    {
        "id": 3,
        "nombre": "Teclado",
        "precio": 80,
        "descripcion": "Teclado mecánico para programadores."
    },
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "titulo": "Mini tienda con FastAPI + Jinja2",
            "productos": productos,
        },
    )


@app.get("/productos/{producto_id}", response_class=HTMLResponse)
async def detalle_producto(request: Request, producto_id: int):
    producto = next((p for p in productos if p["id"] == producto_id), None)

    if producto is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={"mensaje": "Producto no encontrado"},
            status_code=404,
        )

    return templates.TemplateResponse(
        request=request,
        name="producto.html",
        context={"producto": producto},
    )


@app.post("/productos")
async def crear_producto(
    nombre: Annotated[str, Form()],
    precio: Annotated[float, Form()],
    descripcion: Annotated[str, Form()],
):
    nuevo_id = len(productos) + 1

    productos.append(
        {
            "id": nuevo_id,
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion,
        }
    )

    return RedirectResponse(url="/", status_code=303)