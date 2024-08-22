import pandas as pd

# Inicializa DataFrames vacíos
libro_diario = pd.DataFrame(columns=['Fecha', 'Cuenta', 'Débito', 'Crédito', 'Descripción'])
balance_mayor = pd.DataFrame(columns=['Cuenta', 'Débito', 'Crédito', 'Saldo'])

def agregar_transaccion(fecha, cuenta, debito, credito, descripcion):
    global libro_diario
    nueva_transaccion = pd.DataFrame([[fecha, cuenta, debito, credito, descripcion]], columns=libro_diario.columns)
    libro_diario = pd.concat([libro_diario, nueva_transaccion], ignore_index=True)
    actualizar_balance_mayor()

def actualizar_balance_mayor():
    global balance_mayor
    balance_mayor = libro_diario.groupby('Cuenta').agg({
        'Débito': 'sum',
        'Crédito': 'sum'
    }).reset_index()
    balance_mayor['Saldo'] = balance_mayor['Débito'] - balance_mayor['Crédito']

def ver_libro_diario():
    return libro_diario

def ver_balance_mayor():
    return balance_mayor
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

# Inicializa DataFrames vacíos
libro_diario = pd.DataFrame(columns=['Fecha', 'Cuenta', 'Débito', 'Crédito', 'Descripción'])
balance_mayor = pd.DataFrame(columns=['Cuenta', 'Débito', 'Crédito', 'Saldo'])

def agregar_transaccion(fecha, cuenta, debito, credito, descripcion):
    global libro_diario
    nueva_transaccion = pd.DataFrame([[fecha, cuenta, debito, credito, descripcion]], columns=libro_diario.columns)
    libro_diario = pd.concat([libro_diario, nueva_transaccion], ignore_index=True)
    actualizar_balance_mayor()

def actualizar_balance_mayor():
    global balance_mayor
    balance_mayor = libro_diario.groupby('Cuenta').agg({
        'Débito': 'sum',
        'Crédito': 'sum'
    }).reset_index()
    balance_mayor['Saldo'] = balance_mayor['Débito'] - balance_mayor['Crédito']

def ver_libro_diario():
    global libro_diario
    return libro_diario.to_string(index=False)

def ver_balance_mayor():
    global balance_mayor
    return balance_mayor.to_string(index=False)

class ContableApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Entrada de datos
        input_layout = GridLayout(cols=2)
        self.fecha_input = TextInput(hint_text='Fecha', multiline=False)
        self.cuenta_input = TextInput(hint_text='Cuenta', multiline=False)
        self.debito_input = TextInput(hint_text='Débito', multiline=False)
        self.credito_input = TextInput(hint_text='Crédito', multiline=False)
        self.descripcion_input = TextInput(hint_text='Descripción', multiline=False)
        
        input_layout.add_widget(self.fecha_input)
        input_layout.add_widget(self.cuenta_input)
        input_layout.add_widget(self.debito_input)
        input_layout.add_widget(self.credito_input)
        input_layout.add_widget(self.descripcion_input)
        
        add_button = Button(text='Agregar Transacción')
        add_button.bind(on_press=self.agregar_transaccion)
        
        layout.add_widget(input_layout)
        layout.add_widget(add_button)
        
        self.result_label = Label(text='No hay datos', size_hint_y=None, height=44)
        layout.add_widget(self.result_label)
        
        return layout

    def agregar_transaccion(self, instance):
        fecha = self.fecha_input.text
        cuenta = self.cuenta_input.text
        debito = float(self.debito_input.text or 0)
        credito = float(self.credito_input.text or 0)
        descripcion = self.descripcion_input.text
        
        agregar_transaccion(fecha, cuenta, debito, credito, descripcion)
        self.result_label.text = f"Libro Diario:\n{ver_libro_diario()}\n\nBalance Mayor:\n{ver_balance_mayor()}"

if __name__ == '__main__':
    ContableApp().run()