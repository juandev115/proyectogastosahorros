import customtkinter as ctk
import sqlite3
import os

DB_NAME = "finanzas_v2.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS billeteras (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE,
                        saldo REAL DEFAULT 0.0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS movimientos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        billetera_id INTEGER,
                        tipo TEXT,
                        monto REAL,
                        descripcion TEXT,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (billetera_id) REFERENCES billeteras(id))''')
    cursor.execute("SELECT COUNT(*) FROM billeteras")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO billeteras (nombre, saldo) VALUES ('Principal', 0.0)")
    conn.commit()
    conn.close()

class VentanaResumen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Resumen Consolidado")
        self.geometry("500x600")
        self.after(10, self.focus_force)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self, text="Resumen Personalizado", font=("Inter", 22, "bold"))
        self.lbl_titulo.grid(row=0, column=0, pady=20)

        self.frame_checks = ctk.CTkScrollableFrame(self, label_text="Selecciona cuentas para sumar")
        self.frame_checks.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.lbl_total = ctk.CTkLabel(self, text="Total: $ 0.00", font=("Inter", 32, "bold"), text_color="#2ecc71")
        self.lbl_total.grid(row=3, column=0, pady=30)

        self.vars_check = {}
        self.cargar_opciones()

    def cargar_opciones(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, saldo FROM billeteras")
        cuentas = cursor.fetchall()
        conn.close()

        for id_b, nombre, saldo in cuentas:
            var = ctk.BooleanVar(value=True)
            self.vars_check[id_b] = (var, saldo)
            cb = ctk.CTkCheckBox(self.frame_checks, text=f"{nombre} (${saldo:,.2f})", 
                                variable=var, command=self.calcular_total)
            cb.pack(pady=10, padx=20, anchor="w")
        
        self.calcular_total()

    def calcular_total(self):
        total = 0.0
        for id_b, (var, saldo) in self.vars_check.items():
            if var.get(): total += saldo
        self.lbl_total.configure(text=f"Total: $ {total:,.2f}")

class AppFinanzas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Control de Finanzas Pro")
        self.geometry("1200x750")
        
        # --- CONFIGURACIÓN PREDETERMINADA: MODO CLARO ---
        ctk.set_appearance_mode("light") 
        
        init_db()
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_wallet_title = ctk.CTkLabel(self.sidebar, text="BILLETERAS", font=("Inter", 22, "bold"))
        self.lbl_wallet_title.pack(pady=(30, 20), padx=10)

        self.btn_resumen = ctk.CTkButton(self.sidebar, text="📊 Resumen General", 
                                        fg_color="#f1c40f", hover_color="#f39c12", height=45, 
                                        font=("Inter", 14, "bold"), command=self.abrir_resumen)
        self.btn_resumen.pack(pady=5, padx=20, fill="x")

        # Botón Nueva Billetera (Azul Profesional)
        self.btn_add_wallet = ctk.CTkButton(self.sidebar, text="+ Nueva Billetera", 
                                           fg_color="#3498db", hover_color="#2980b9",
                                           height=40, font=("Inter", 14, "bold"), 
                                           command=self.dialogo_nueva_billetera)
        self.btn_add_wallet.pack(pady=5, padx=20, fill="x")

        # Botón Eliminar (Gris Azulado Elegante)
        self.btn_del_wallet = ctk.CTkButton(self.sidebar, text="🗑 Eliminar Actual", 
                                           fg_color="#5d6d7e", hover_color="#34495e",
                                           height=40, font=("Inter", 14),
                                           command=self.eliminar_billetera)
        self.btn_del_wallet.pack(pady=5, padx=20, fill="x")

        self.wallet_list_frame = ctk.CTkScrollableFrame(self.sidebar, label_text="Mis Cuentas")
        self.wallet_list_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # --- INTERRUPTOR DE MODO (Inicia en OFF para Modo Claro) ---
        self.modo_switch_var = ctk.StringVar(value="off")
        self.switch_modo = ctk.CTkSwitch(self.sidebar, text="Modo Claro", command=self.cambiar_tema,
                                        variable=self.modo_switch_var, onvalue="on", offvalue="off")
        self.switch_modo.pack(pady=20, padx=20)
        
        # --- Área Principal ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=40, pady=30, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        self.lbl_selected_wallet = ctk.CTkLabel(self.main_frame, text="Selecciona una cuenta", font=("Inter", 28, "bold"))
        self.lbl_selected_wallet.grid(row=0, column=0, pady=(10, 5), sticky="w")

        self.lbl_saldo = ctk.CTkLabel(self.main_frame, text="$ 0.00", font=("Inter", 52, "bold"), text_color="#3498db")
        self.lbl_saldo.grid(row=1, column=0, pady=10, sticky="w")

        self.entry_frame = ctk.CTkFrame(self.main_frame)
        self.entry_frame.grid(row=2, column=0, pady=25, sticky="ew")
        self.entry_frame.grid_columnconfigure((0, 1), weight=1)

        self.entry_monto = ctk.CTkEntry(self.entry_frame, placeholder_text="Monto $", height=50, font=("Inter", 15))
        self.entry_monto.grid(row=0, column=0, padx=15, pady=20, sticky="ew")
        
        self.entry_desc = ctk.CTkEntry(self.entry_frame, placeholder_text="Descripción", height=50, font=("Inter", 15))
        self.entry_desc.grid(row=0, column=1, padx=15, pady=20, sticky="ew")

        self.btn_in = ctk.CTkButton(self.entry_frame, text="Ingreso", fg_color="#27ae60", hover_color="#2ecc71", height=50, command=lambda: self.transaccion("Ingreso"))
        self.btn_in.grid(row=0, column=2, padx=10, pady=20)

        self.btn_out = ctk.CTkButton(self.entry_frame, text="Gasto", fg_color="#c0392b", hover_color="#e74c3c", height=50, command=lambda: self.transaccion("Gasto"))
        self.btn_out.grid(row=0, column=3, padx=10, pady=20)

        self.txt_historial = ctk.CTkTextbox(self.main_frame, font=("Segoe UI Variable Text", 16), corner_radius=15)
        self.txt_historial.grid(row=3, column=0, sticky="nsew", pady=(10, 0))
        self.txt_historial.tag_config("ingreso", foreground="#2ecc71")
        self.txt_historial.tag_config("gasto", foreground="#e74c3c")
        self.txt_historial.tag_config("fecha", foreground="#95a5a6")

        self.id_billetera_actual = None
        self.actualizar_lista_billeteras()

    def cambiar_tema(self):
        if self.modo_switch_var.get() == "on":
            ctk.set_appearance_mode("dark")
            self.switch_modo.configure(text="Modo Oscuro")
        else:
            ctk.set_appearance_mode("light")
            self.switch_modo.configure(text="Modo Claro")

    def abrir_resumen(self):
        VentanaResumen(self)

    def eliminar_billetera(self):
        if self.id_billetera_actual is None: return
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM billeteras")
        if cursor.fetchone()[0] > 1:
            cursor.execute("DELETE FROM movimientos WHERE billetera_id = ?", (self.id_billetera_actual,))
            cursor.execute("DELETE FROM billeteras WHERE id = ?", (self.id_billetera_actual,))
            conn.commit()
        conn.close()
        self.id_billetera_actual = None
        self.actualizar_lista_billeteras()
        self.cargar_historial()

    def actualizar_lista_billeteras(self):
        for widget in self.wallet_list_frame.winfo_children(): widget.destroy()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, saldo FROM billeteras")
        for row in cursor.fetchall():
            btn = ctk.CTkButton(self.wallet_list_frame, text=f"{row[1].upper()}\n$ {row[2]:,.2f}", 
                               anchor="w", font=("Inter", 14), fg_color="#d68910", height=70,
                               command=lambda r=row: self.seleccionar_billetera(r))
            btn.pack(pady=10, fill="x", padx=10)
        conn.close()

    def seleccionar_billetera(self, data):
        self.id_billetera_actual = data[0]
        self.lbl_selected_wallet.configure(text=f"Cuenta: {data[1]}")
        self.actualizar_saldo_ui()
        self.cargar_historial()

    def actualizar_saldo_ui(self):
        if not self.id_billetera_actual: return
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT saldo FROM billeteras WHERE id = ?", (self.id_billetera_actual,))
        res = cursor.fetchone()
        if res: self.lbl_saldo.configure(text=f"$ {res[0]:,.2f}")
        conn.close()

    def dialogo_nueva_billetera(self):
        dialog = ctk.CTkInputDialog(text="Nombre de la nueva cuenta:", title="Nueva Billetera")
        nombre = dialog.get_input()
        if nombre:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO billeteras (nombre, saldo) VALUES (?, 0.0)", (nombre,))
                conn.commit()
            except: pass
            conn.close()
            self.actualizar_lista_billeteras()

    def transaccion(self, tipo):
        if self.id_billetera_actual is None: return
        try:
            monto = float(self.entry_monto.get().replace(",", "."))
            desc = self.entry_desc.get() or "Sin descripción"
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO movimientos (billetera_id, tipo, monto, descripcion) VALUES (?, ?, ?, ?)",
                          (self.id_billetera_actual, tipo, monto, desc))
            ajuste = monto if tipo == "Ingreso" else -monto
            cursor.execute("UPDATE billeteras SET saldo = saldo + ? WHERE id = ?", (ajuste, self.id_billetera_actual))
            conn.commit()
            conn.close()
            self.actualizar_saldo_ui()
            self.cargar_historial()
            self.actualizar_lista_billeteras()
            self.entry_monto.delete(0, 'end'); self.entry_desc.delete(0, 'end')
        except: pass

    def cargar_historial(self):
        self.txt_historial.configure(state="normal")
        self.txt_historial.delete("1.0", "end")
        if not self.id_billetera_actual: 
            self.txt_historial.configure(state="disabled")
            return
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT tipo, monto, descripcion, fecha FROM movimientos WHERE billetera_id = ? ORDER BY fecha DESC", (self.id_billetera_actual,))
        for row in cursor.fetchall():
            tag = "ingreso" if row[0] == "Ingreso" else "gasto"
            self.txt_historial.insert("end", f"{'▲' if tag=='ingreso' else '▼'} {row[0].upper()}: ${row[1]:,.2f}", tag)
            self.txt_historial.insert("end", f" | {row[2]}  ")
            self.txt_historial.insert("end", f"({row[3]})\n", "fecha")
        conn.close()
        self.txt_historial.configure(state="disabled")

if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()