from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="routers/templates")


class Expression(BaseModel):
    expression: str


@router.get("/", response_class= HTMLResponse)
@router.get("/home", response_class= HTMLResponse)
async def Home(request: Request):
    title = 'Componentes H&J | Home'
    return templates.TemplateResponse("home.j2", {
        "request": request,
        "title": title, 
    })

@router.post("/calculadora")
def calculadora(expression: Expression):
    resultado = calcular(expression.expression)
    return resultado


def calcular(expression: str):
    try:
        # Removemos espacios en blanco de la expresión
        expression = expression.replace(" ", "")
        
        # Utilizamos una lista de operadores permitidos
        operadores = ['+', '-', '*', '/', '%', '//', '**']
        
        # Inicializamos las variables para almacenar los números y operador
        numero1 = ''
        numero2 = ''
        operacion = ''
        char_ant = '' 
        
        # Recorremos la expresión para separar números y operador
        for char in expression:
            if char_ant == '/' and char == '/' or char_ant == '*' and char == '*':
                char = char_ant+char
                print(char)
            if char in operadores:
                operacion = char
            else:
                if operacion:
                    numero2 += char
                else:
                    numero1 += char
            char_ant=char
        
        # Verificamos que tengamos números y un operador
        if not operacion or not numero1 or not numero2:
            raise ValueError("Error")
        
        # Convertimos los números a tipo float
        num1 = float(numero1)
        num2 = float(numero2)
        
        # Realizamos la operación
        if operacion == '+':
            resultado = num1 + num2
        elif operacion == '//':
            resultado = num1 // num2
        elif operacion == '**':
            resultado = num1 ** num2
        elif operacion == '-':
            resultado = num1 - num2
        elif operacion == '*':
            resultado = num1 * num2
        elif operacion == '/':
            resultado = num1 / num2
        elif operacion == '%':
            resultado = num1 % num2
        
        return resultado
    except Exception as e:
        return str(e)