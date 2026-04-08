import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, font
from compilador.lexico import lexer, encontrar_columna
from compilador.sintactico import parser
from compilador.semantico import analizar, ErroSemantico
from compilador.interprete import interprete, InterpreterError

PALETTE = {
    "main_bg": "#fffafb",      
    "panel_bg": "#7de2d1",    
    "header_bg": "#339989",   
    "header_fg": "#131515",    
    "button1": "#339989",     
    "button2": "#339989",      
    "button3": "#339989",    
    "button4": "#339989",     
    "button5": "#339989",      
    "button_fg": "#131515",    
    "button_fg1": "#fffafb",   
    "output1": "#fffafb",      
    "output2": "#fffafb",    
    "output3": "#fffafb",    
    "info_bg": "#339989",      
    "info_fg": "#fffafb",     
    "border": "#131515",     
}

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiladores")
        self.root.configure(bg=PALETTE["main_bg"])
        self.font_family = "Verdana" 

        # Centrar ventana
        self.centrar(1200, 800)

        #Frame central para todo el contenido 
        self.central_frame = tk.Frame(root, bg=PALETTE["panel_bg"], bd=2, relief="ridge")
        self.central_frame.place(relx=0.5, rely=0.5, anchor="center", width=1370, height=700)

        #Header 
        tk.Label(self.central_frame, text="¡COMPILANDO EN PYTHON!", font=("Poppins", 24, "bold"),
                 bg=PALETTE["header_bg"], fg="#fffafb", pady=10).pack(fill="x", pady=(0, 10))

        #Caja de código fuente
        code_frame = tk.Frame(self.central_frame, bg=PALETTE["panel_bg"])
        code_frame.pack(pady=(10, 0))
        tk.Label(code_frame, text="Ingresa el código fuente Python:",
                 font=(self.font_family, 12, "bold"), bg=PALETTE["panel_bg"]).pack(anchor="w")
        self.code_input = scrolledtext.ScrolledText(code_frame, width=100, height=7,
                                                    font=(self.font_family, 12),
                                                    bg=PALETTE["main_bg"], fg=PALETTE["button_fg"], bd=2, relief="groove")
        self.code_input.pack(pady=5)

        #Botones de análisis 
        button_frame = tk.Frame(self.central_frame, bg=PALETTE["panel_bg"])
        button_frame.pack(pady=(10, 10))

        button_specs = [
            ("Análisis Léxico", self.analizador_lexico, PALETTE["button1"]),
            ("Análisis Sintáctico", self.analizador_sintactico, PALETTE["button2"]),
            ("Análisis Semántico", self.analisis_semantico, PALETTE["button3"]),
            ("Limpiar", self.limpiar_todo, PALETTE["button1"]),
            ("Exportar Resultados", self.export_results, PALETTE["button2"]),
            ("Información", self.informacion, PALETTE["button3"]),
        ]

        for i, (text, cmd, color) in enumerate(button_specs):
            tk.Button(button_frame, text=text, command=cmd,
                      font=(self.font_family, 11, "bold"),
                      bg=color, fg=PALETTE["button_fg1"], activebackground=PALETTE["button5"],
                      width=18, height=2, bd=0, relief="ridge").grid(row=0, column=i, padx=6, pady=2)

        # --- Cajas de resultados ---
        results_frame = tk.Frame(self.central_frame, bg=PALETTE["panel_bg"])
        results_frame.pack(pady=(15, 0), fill="x", expand=True)

        # Léxico
        lex_frame = tk.Frame(results_frame, bg=PALETTE["panel_bg"])
        lex_frame.grid(row=0, column=0, padx=10)
        tk.Label(lex_frame, text="Resultado Léxico", font=(self.font_family, 12, "bold"),
                 bg=PALETTE["panel_bg"], fg="#0d5c63").pack()
        self.lex_output = scrolledtext.ScrolledText(lex_frame, width=45, height=16,
                                                    font=(self.font_family, 11),
                                                    bg=PALETTE["output1"], fg=PALETTE["button_fg"], bd=2, relief="groove")
        self.lex_output.pack(pady=5)

        # Sintáctico
        syn_frame = tk.Frame(results_frame, bg=PALETTE["panel_bg"])
        syn_frame.grid(row=0, column=1, padx=10)
        tk.Label(syn_frame, text="Resultado Sintáctico", font=(self.font_family, 12, "bold"),
                 bg=PALETTE["panel_bg"], fg="#0d5c63").pack()
        self.syn_output = scrolledtext.ScrolledText(syn_frame, width=40, height=16,
                                                    font=(self.font_family, 11),
                                                    bg=PALETTE["output2"], fg=PALETTE["button_fg"], bd=2, relief="groove")
        self.syn_output.pack(pady=5)

        # Semántico
        sem_frame = tk.Frame(results_frame, bg=PALETTE["panel_bg"])
        sem_frame.grid(row=0, column=2, padx=10)
        tk.Label(sem_frame, text="Resultado Semántico", font=(self.font_family, 12, "bold"),
                 bg=PALETTE["panel_bg"], fg="#0d5c63").pack()
        self.sem_output = scrolledtext.ScrolledText(sem_frame, width=38, height=16,
                                                    font=(self.font_family, 11),
                                                    bg=PALETTE["output3"], fg=PALETTE["button_fg"], bd=2, relief="groove")
        self.sem_output.pack(pady=5)

        #  Mensaje informativo
        self.info_label = tk.Label(self.central_frame,
                                   text="Estefania Moreno Reyes",
                                   fg=PALETTE["info_fg"], bg=PALETTE["info_bg"],
                                   font=(self.font_family, 10, "italic"), pady=6)
        self.info_label.pack(side="bottom", fill="x", pady=(10, 0))

    def analizador_lexico(self):
        code = self.code_input.get("1.0", tk.END)
        self.lex_output.delete("1.0", tk.END)
        lexer.lineno = 1
        lexer.input(code)
        try:
            result_lines = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                # Calcular columna real
                col = encontrar_columna(code, tok) if callable(encontrar_columna) else tok.lexpos
                result_lines.append(
                    f"TOKEN -> {tok.type} -> {repr(tok.value)} -> [{tok.lineno},{col} ] "
                )
            if result_lines:
                self.lex_output.insert(tk.END, "\n".join(result_lines))
            else:
                self.lex_output.insert(tk.END, "No se encontraron tokens. ¿El código está vacío?")
        except Exception as e:
            # Mostrar SOLO el error léxico en la caja
            self.lex_output.delete("1.0", tk.END)
            self.lex_output.insert(tk.END, str(e))

    def analizador_sintactico(self):
        code = self.code_input.get("1.0", tk.END)
        self.syn_output.delete("1.0", tk.END)
        try:
            ast = parser.parse(code)
            if ast:
                self.syn_output.insert(tk.END, "¡Análisis sintáctico exitoso! El código cumple las reglas gramaticales.\n\n")
                self.syn_output.insert(tk.END, "Árbol de sintaxis abstracta (AST):\n")
                self.arbol(ast)
                # Ejecutar el AST y mostrar la salida
                try:
                    output = interprete(ast)
                    if output:
                        self.syn_output.insert(tk.END, "\nResultado de ejecución:\n")
                        self.syn_output.insert(tk.END, "\n".join(str(line) for line in output))
                    else:
                        self.syn_output.insert(tk.END, "\n(No hay salida de ejecución)")
                except InterpreterError as ie:
                    self.syn_output.insert(tk.END, f"\nError de ejecución: {ie}")
            else:
                self.syn_output.insert(tk.END, "No se pudo generar el AST. ¿El código está vacío o tiene errores?")
        except SyntaxError as e:
            self.syn_output.insert(tk.END, f"{e}")
        except Exception as e:
            self.syn_output.insert(tk.END, f"Error sintáctico inesperado: {e}")
            
    def arbol(self, node, level=0):
        """Muestra el AST de forma organizada con indentación"""
        if isinstance(node, tuple) and len(node) > 0:
            # Mostrar el tipo de nodo
            self.syn_output.insert(tk.END, "  " * level + f"- {node[0]}\n")
            # Procesar los hijos
            for child in node[1:]:
                self.arbol(child, level + 1)
        elif isinstance(node, list):
            # Procesar listas de nodos
            for item in node:
                self.arbol(item, level)
        else:
            # Mostrar valores terminales
            self.syn_output.insert(tk.END, "  " * level + f"- {node}\n")

    def analisis_semantico(self):
        code = self.code_input.get("1.0", tk.END)
        self.sem_output.delete("1.0", tk.END)
        try:
            ast = parser.parse(code)
            if not ast:
                self.sem_output.insert(tk.END, "No se pudo generar el AST. ¿El código está vacío o tiene errores?")
                return
            analizar(ast)
            self.sem_output.insert(tk.END, "¡Análisis semántico exitoso! No se encontraron errores semánticos.")
        except ErroSemantico as se:
            self.sem_output.insert(tk.END, f"Error semántico: {se}")
        except Exception as e:
            self.sem_output.insert(tk.END, f"Error inesperado: {e}")

    def centrar(self, width=1200, height=800):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def limpiar_todo(self):
        self.code_input.delete("1.0", tk.END)
        self.lex_output.delete("1.0", tk.END)
        self.syn_output.delete("1.0", tk.END)
        self.sem_output.delete("1.0", tk.END)
        self.info_label.config(
            text="Integrantes: Estefania Moreno Reyes, Maria Juanita Tamayo Marin ",
            fg=PALETTE["info_fg"]
        )

    def export_results(self):
        options = ["Léxico", "Sintáctico", "Semántico", "Todos"]
        export_win = tk.Toplevel(self.root)
        export_win.title("Exportar resultados")
        export_win.configure(bg=PALETTE["main_bg"])
        tk.Label(export_win, text="¿Qué resultado desea exportar?", font=(self.font_family, 11),
                 bg=PALETTE["main_bg"]).pack(padx=10, pady=10)
        var = tk.StringVar(value=options[0])

        for opt in options:
            tk.Radiobutton(export_win, text=opt, variable=var, value=opt, bg=PALETTE["main_bg"]).pack(anchor="w", padx=20)

        def exportar():
            choice = var.get()
            if choice == "Léxico":
                content = self.lex_output.get("1.0", tk.END)
            elif choice == "Sintáctico":
                content = self.syn_output.get("1.0", tk.END)
            elif choice == "Semántico":
                content = self.sem_output.get("1.0", tk.END)
            else:
                content = (
                    "=== Resultado Léxico ===\n" + self.lex_output.get("1.0", tk.END) +
                    "\n=== Resultado Sintáctico ===\n" + self.syn_output.get("1.0", tk.END) +
                    "\n=== Resultado Semántico ===\n" + self.sem_output.get("1.0", tk.END)
                )
            if not content.strip():
                messagebox.showinfo("Exportar", "No hay resultados para exportar.")
                export_win.destroy()
                return
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Exportar", f"Resultados exportados a:\n{file_path}")
            export_win.destroy()

        tk.Button(export_win, text="Exportar", command=exportar, width=15, bg=PALETTE["button2"]).pack(pady=10)
        export_win.transient(self.root)
        export_win.grab_set()
        self.root.wait_window(export_win)

    def informacion(self):
        # Ventana de información
        info_win = tk.Toplevel(self.root)
        info_win.title("Información")
        info_win.geometry("950x700")
        info_win.configure(bg=PALETTE["main_bg"])

        # Título principal
        tk.Label(
            info_win,
            text="Información del Lenguaje y Analizadores",
            font=(self.font_family, 18, "bold"),
            bg=PALETTE["header_bg"],
            fg="#fcfffd",
            pady=12
        ).pack(fill="x", pady=(0, 12))

        # --- Canvas + Scrollbar para contenido desplazable ---
        canvas_frame = tk.Frame(info_win, bg=PALETTE["main_bg"])
        canvas_frame.pack(fill="both", expand=True, padx=0, pady=0)

        canvas = tk.Canvas(canvas_frame, bg=PALETTE["main_bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame interior que contendrá los bloques de información
        container = tk.Frame(canvas, bg=PALETTE["main_bg"])
        # El frame se coloca dentro del canvas
        canvas.create_window((0, 0), window=container, anchor="nw")

        # Función para ajustar el scroll al tamaño del contenido
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        container.bind("<Configure>", on_configure)
        block_width = 700

        # --- Bloque: Lenguaje Python ---
        python_frame = tk.Frame(container, bg="#b2f7ef", bd=2, relief="ridge")
        python_frame.pack(fill="x", pady=(0, 18))
        tk.Label(
            python_frame,
            text="Lenguaje Python",
            font=(self.font_family, 14, "bold"),
            bg="#40c9b6",
            fg="#fcfffd",
            pady=6
        ).pack(fill="x")
        tk.Label(
            python_frame,
            text=(
                "Python es un lenguaje de programación interpretado, de alto nivel y propósito general.\n"
                "Su sintaxis clara y legible lo hace ideal para principiantes y profesionales.\n"
                "Permite el desarrollo rápido de aplicaciones, scripts, análisis de datos, inteligencia artificial y más.\n"
                "Ejemplo básico:\n"
                "    x = 10\n"
                "    y = 5\n"
                "    suma = x + y\n"
                "    print('La suma es:', suma)\n"
            ),
            font=(self.font_family, 11),
            bg="#b2f7ef",
            fg="#131515",
            justify="left",
            anchor="w"
        ).pack(fill="x", padx=12, pady=8)

        # --- Bloque: Analizador Léxico ---
        lexico_frame = tk.Frame(container, bg="#7de2d1", bd=2, relief="ridge")
        lexico_frame.pack(fill="x", pady=(0, 18))
        tk.Label(
            lexico_frame,
            text="Analizador Léxico",
            font=(self.font_family, 14, "bold"),
            bg="#339989",
            fg="#fcfffd",
            pady=6
        ).pack(fill="x")
        tk.Label(
            lexico_frame,
            text=(
                "Convierte el código fuente en una secuencia de tokens (palabras clave, identificadores, números, operadores, etc).\n"
                "Permite detectar errores como caracteres no válidos o identificadores mal formados.\n"
                "Ejemplo de entrada:\n"
                "    mensaje = \"Hola, mundo!\"\n"
                "    resultado = 7 + 3\n"
                "Ejemplo de salida:\n"
             
                "    TOKEN -> ID      -> mensaje         -> [Fila: 1 , Columna : 0 ]\n"
                "    TOKEN -> ASSIGN  -> =               -> [Fila: 1 , Columna : 8 \n"
                "    TOKEN -> STRING  -> \"Hola, mundo!\"-> [Fila: 1 , Columna : 10 ]\n"
                "    TOKEN -> ID      -> resultado       -> [Fila: 2 , Columna : 0  ]\n"
                "    TOKEN -> ASSIGN  -> =               -> [Fila: 2 , Columna : 10 ]\n"
                "    TOKEN -> NUMBER  -> 7               -> [Fila: 2 , Columna : 12 ]\n"
                "    TOKEN -> PLUS    -> +               -> [Fila: 2 , Columna : 14 ]\n"
                "    TOKEN -> UMBER   -> 3               -> [Fila: 2 , Columna : 16 ]\n"
                "Errores léxicos típicos: uso de símbolos no permitidos, cadenas sin cerrar, etc."
            ),
            font=(self.font_family, 11),
            bg="#7de2d1",
            fg="#131515",
            justify="left",
            anchor="w"
        ).pack(fill="x", padx=12, pady=8)

        # --- Bloque: Analizador Sintáctico ---
        sintactico_frame = tk.Frame(container, bg="#b2f7ef", bd=2, relief="ridge")
        sintactico_frame.pack(fill="x", pady=(0, 18))
        tk.Label(
            sintactico_frame,
            text="Analizador Sintáctico",
            font=(self.font_family, 14, "bold"),
            bg="#40c9b6",
            fg="#fcfffd",
            pady=6
        ).pack(fill="x")
        tk.Label(
            sintactico_frame,
            text=(
                "Verifica que el código cumple las reglas gramaticales del lenguaje y genera el Árbol de Sintaxis Abstracta (AST).\n"
                "Permite detectar errores como paréntesis no balanceados, estructuras mal formadas, etc.\n"
                "Ejemplo de entrada:\n"
                "    if x > 0:\n"
                "        print(\"Positivo\")\n"
                "    else:\n"
                "        print(\"No positivo\")\n"
                "Ejemplo de salida:\n"
                "    - if\n"
                "      - binop\n"
                "        - >\n"
                "        - id\n"
                "          - x\n"
                "        - number\n"
                "          - 0\n"
                "      - program\n"
                "        - call\n"
                "          - print\n"
                "          - string\n"
                "            - \"Positivo\"\n"
                "      - program\n"
                "        - call\n"
                "          - print\n"
                "          - string\n"
                "            - \"No positivo\"\n"
                "Errores sintácticos típicos: falta de dos puntos, indentación incorrecta, etc."
            ),
            font=(self.font_family, 11),
            bg="#b2f7ef",
            fg="#131515",
            justify="left",
            anchor="w"
        ).pack(fill="x", padx=12, pady=8)

        # --- Bloque: Analizador Semántico ---
        semantico_frame = tk.Frame(container, bg="#7de2d1", bd=2, relief="ridge")
        semantico_frame.pack(fill="x", pady=(0, 18))
        tk.Label(
            semantico_frame,
            text="Analizador Semántico",
            font=(self.font_family, 14, "bold"),
            bg="#339989",
            fg="#fffafb",
            pady=6
        ).pack(fill="x")
        tk.Label(
            semantico_frame,
            text=(
                "Comprueba el significado del código: tipos de datos, variables definidas, operaciones válidas, número correcto de argumentos, etc.\n"
                "Ejemplo de entrada:\n"
                "    x = \"Hola\" + 5\n"
                "    print(y)\n"
                "Ejemplo de salida:\n"
                "    Error semántico: no se puede sumar string y number\n"
                "    Error semántico: Variable 'y' no declarada\n"
                "Errores semánticos típicos: uso de variables no declaradas, operaciones entre tipos incompatibles, llamadas a funciones con argumentos incorrectos, etc.\n"
                "Ejemplo correcto:\n"
                "    x = 10\n"
                "    y = 20\n"
                "    suma = x + y\n"
                "    print(suma)\n"
                "    # Salida: 30"
            ),
            font=(self.font_family, 11),
            bg="#7de2d1",
            fg="#131515",
            justify="left",
            anchor="w"
        ).pack(fill="x", padx=12, pady=8)

        # Botón para cerrar
        tk.Button(
            info_win,
            text="Cerrar",
            command=info_win.destroy,
            font=(self.font_family, 11, "bold"),
            bg=PALETTE["button1"],
            fg=PALETTE["button_fg"]
        ).pack(pady=16)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()
