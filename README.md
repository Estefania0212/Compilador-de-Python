# 🧠 Compilador en Python

Este proyecto consiste en el desarrollo de un compilador en Python con interfaz gráfica, capaz de realizar análisis léxico, sintáctico y semántico sobre código fuente.

## 🚀 Características

- ✅ Análisis Léxico (tokens)
- ✅ Análisis Sintáctico (AST)
- ✅ Análisis Semántico (validación)
- ✅ Ejecución de código interpretado
- ✅ Interfaz gráfica amigable con Tkinter
- ✅ Exportación de resultados

## 🛠️ Tecnologías utilizadas

- Python
- Tkinter (GUI)
- Programación modular
- Compiladores (conceptos: lexer, parser, AST)

## ▶️ Ejecución
Para ejecutar: python -m interfaz.main

## Pruebas


PRUEBA 1: VÁLIDA
--------------------------
Código:
x = 5
y = 3
z = x + y
print(z)

Salida esperada:
- Léxico:
  Lista de Tokens
- Sintáctico:
  ¡Análisis sintáctico exitoso! -> Salida: 8
- Semántico:
  ¡Análisis semántico exitoso! No se encontraron errores semánticos.


PRUEBA 3: NO VÁLIDA (SINTÁCTICO)
--------------------------
Código:
x = 5
y = 
z = x + y

Salida esperada:
- Léxico:
  Listado de tokens
- Sintáctico:
  Error sintáctico: se esperaba un valor después de '=' en la línea 2.
- Semántico:
  No se pudo generar el AST. ¿El código está vacío o tiene errores?


PRUEBA 4: NO VÁLIDA (SEMÁNTICO)
--------------------------
Código:
x = "Hola"
y = 5
z = x + y

Salida esperada:
- Léxico:
  Listado de tokens
- Sintáctico:
  ¡Análisis sintáctico exitoso! El código cumple las reglas gramaticales.
- Semántico:
  Error semántico: no se puede sumar string y number
