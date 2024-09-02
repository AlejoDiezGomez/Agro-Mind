import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import os
from datetime import datetime

# Función para obtener el nombre del archivo CSV según la fecha actual
def obtener_ruta_csv():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return f'libro_diario_{fecha_actual}.csv'

# Inicializa DataFrames
FILE_PATH = obtener_ruta_csv()
if os.path.exists(FILE_PATH):
    try:
        libro_diario = pd.read_csv(FILE_PATH)
    except pd.errors.EmptyDataError:
        libro_diario = pd.DataFrame(columns=['Fecha', 'Cuenta', 'Débito', 'Crédito', 'Descripción'])
else:
    libro_diario = pd.DataFrame(columns=['Fecha', 'Cuenta', 'Débito', 'Crédito', 'Descripción'])

balance_mayor = pd.DataFrame(columns=['Cuenta', 'Débito', 'Crédito', 'Saldo'])

def actualizar_balance_mayor():
    global balance_mayor
    if not libro_diario.empty:
        balance_mayor = libro_diario.groupby('Cuenta').agg({
            'Débito': 'sum',
            'Crédito': 'sum'
        }).reset_index()
        balance_mayor['Saldo'] = balance_mayor['Débito'] - balance_mayor['Crédito']
    else:
        balance_mayor = pd.DataFrame(columns=['Cuenta', 'Débito', 'Crédito', 'Saldo'])

def agregar_transaccion(cuenta, debito, credito, descripcion):
    global libro_diario
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    nueva_transaccion = pd.DataFrame([[fecha_actual, cuenta, debito, credito, descripcion]],
                                     columns=libro_diario.columns)
    libro_diario = pd.concat([libro_diario, nueva_transaccion], ignore_index=True)
    actualizar_balance_mayor()
    guardar_en_csv(nueva_transaccion)

def ver_libro_diario():
    global libro_diario
    return libro_diario.to_string(index=False)

def ver_balance_mayor():
    global balance_mayor
    return balance_mayor.to_string(index=False)

def guardar_en_csv(nueva_transaccion):
    file_path = obtener_ruta_csv()
    if not os.path.exists(file_path):
        # Si el archivo no existe, crear uno nuevo con encabezados
        nueva_transaccion.to_csv(file_path, index=False, mode='w')
    else:
        # Si el archivo existe, agregar la nueva transacción sin encabezados
        nueva_transaccion.to_csv(file_path, index=False, mode='a', header=False)

# Actualizar balance_mayor al cargar datos existentes
actualizar_balance_mayor()

class ContableApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Layout para entradas
        input_layout = GridLayout(cols=2, row_default_height=40, spacing=10, size_hint_y=None)
        input_layout.bind(minimum_height=input_layout.setter('height'))

        # Etiquetas y campos de entrada

        input_layout.add_widget(Label(text='Cuenta:'))
        self.cuenta_input = TextInput(hint_text='Nombre de la cuenta', multiline=False)
        input_layout.add_widget(self.cuenta_input)

        input_layout.add_widget(Label(text='Débito:'))
        self.debito_input = TextInput(hint_text='0.00', multiline=False, input_filter='float')
        input_layout.add_widget(self.debito_input)

        input_layout.add_widget(Label(text='Crédito:'))
        self.credito_input = TextInput(hint_text='0.00', multiline=False, input_filter='float')
        input_layout.add_widget(self.credito_input)

        input_layout.add_widget(Label(text='Descripción:'))
        self.descripcion_input = TextInput(hint_text='Descripción de la transacción', multiline=False)
        input_layout.add_widget(self.descripcion_input)

        # Botón para agregar transacción
        add_button = Button(text='Agregar Transacción', size_hint_y=None, height=40)
        add_button.bind(on_press=self.agregar_transaccion)

        # Label para mostrar resultados
        self.result_label = Label(text='', size_hint_y=None, height=300, halign='left', valign='top')
        self.result_label.bind(size=self.result_label.setter('text_size'))

        # Agregar widgets al layout principal
        layout.add_widget(input_layout)
        layout.add_widget(add_button)
        layout.add_widget(self.result_label)

        # Mostrar datos existentes al iniciar
        self.actualizar_resultados()

        return layout

    def agregar_transaccion(self, instance):
        try:
            # Obtener y limpiar los datos de entrada
            cuenta = self.cuenta_input.text.strip()
            debito_text = self.debito_input.text.strip()
            credito_text = self.credito_input.text.strip()
            descripcion = self.descripcion_input.text.strip()

            # Convertir Débito y Crédito a flotantes
            debito = float(debito_text) if debito_text else 0.0
            credito = float(credito_text) if credito_text else 0.0

            # Validación de campos obligatorios
            if not cuenta or (debito == 0 and credito == 0):
                self.result_label.text = "Por favor, complete todos los campos obligatorios."
                return

            # Agregar la transacción
            agregar_transaccion(cuenta, debito, credito, descripcion)

            # Actualizar la visualización de resultados
            self.actualizar_resultados()

            # Limpiar campos de entrada
            self.cuenta_input.text = ''
            self.debito_input.text = ''
            self.credito_input.text = ''
            self.descripcion_input.text = ''

        except ValueError:
            self.result_label.text = "Error en los valores ingresados. Asegúrese de que Débito y Crédito sean números."

    def actualizar_resultados(self):
        if not libro_diario.empty:
            self.result_label.text = f"Libro Diario:\n{ver_libro_diario()}\n\nBalance Mayor:\n{ver_balance_mayor()}"
        else:
            self.result_label.text = "No hay datos."

if __name__ == '__main__':
    ContableApp().run()
