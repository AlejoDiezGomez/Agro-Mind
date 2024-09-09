from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import pandas as pd
import os
from datetime import datetime

# Funciones para manejar los libros
def obtener_ruta_csv():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return f'libro_diario_{fecha_actual}.csv'

LIBRO_CUENTAS_FILE = 'libro_cuentas.csv'

def generar_id():
    """Genera un ID único basado en el número total de transacciones."""
    ruta_archivo = obtener_ruta_csv()

    # Crear el archivo si no existe
    if not os.path.exists(ruta_archivo):
        pd.DataFrame(columns=['id', 'Fecha', 'Cuenta', 'Débito', 'Crédito', 'Descripción']).to_csv(ruta_archivo, index=False)
    
    df = pd.read_csv(ruta_archivo)
    if not df.empty:
        # Convertir 'id' a cadena para manejar cualquier formato, y separar el ID secuencial
        df['id_num'] = df['id'].str.split('_').str[1].astype(int)  # Obtener solo la parte numérica del ID
        max_id = df['id_num'].max()
        nuevo_id = int(max_id) + 1  # Incrementar el ID
    else:
        nuevo_id = 1  # Comenzar desde 1 si no hay transacciones

    # Combinar la fecha actual con el ID secuencial
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return f"{fecha_actual}_{nuevo_id}"

def convertir_a_numero(valor):
    """Convierte una cadena a número (flotante) si es posible."""
    try:
        return float(valor)
    except ValueError:
        return 0.0

if os.path.exists(obtener_ruta_csv()):
    try:
        libro_diario = pd.read_csv(obtener_ruta_csv())
    except pd.errors.EmptyDataError:
        libro_diario = pd.DataFrame(columns=['id', 'Fecha', 'Cuenta', 'Débito', 'Crédito', 'Descripción'])
else:
    libro_diario = pd.DataFrame(columns=['id', 'Fecha', 'Cuenta', 'Débito', 'Crédito', 'Descripción'])
    libro_diario.to_csv(obtener_ruta_csv(), index=False)

if os.path.exists(LIBRO_CUENTAS_FILE):
    libro_cuentas = pd.read_csv(LIBRO_CUENTAS_FILE)
else:
    libro_cuentas = pd.DataFrame(columns=['Cuenta', 'Descripción'])

balance_mayor = pd.DataFrame(columns=['Cuenta', 'Débito', 'Crédito', 'Saldo'])

def actualizar_balance_mayor():
    global balance_mayor
    if not libro_diario.empty:
        libro_diario['Débito'] = libro_diario['Débito'].apply(convertir_a_numero)
        libro_diario['Crédito'] = libro_diario['Crédito'].apply(convertir_a_numero)
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
    nuevo_id = generar_id()
    nueva_transaccion = pd.DataFrame([[nuevo_id, fecha_actual, cuenta, debito, credito, descripcion]],
                                     columns=libro_diario.columns)
    libro_diario = pd.concat([libro_diario, nueva_transaccion], ignore_index=True)
    actualizar_balance_mayor()
    guardar_en_csv(nueva_transaccion)

def eliminar_transaccion(id):
    global libro_diario
    # Filtrar el libro diario para eliminar la transacción con el ID dado
    libro_diario = libro_diario[libro_diario['id'] != id]
    actualizar_balance_mayor()
    guardar_en_csv(libro_diario)  # Guardar los cambios en el archivo CSV

def agregar_cuenta(cuenta, descripcion):
    global libro_cuentas
    nueva_cuenta = pd.DataFrame([[cuenta, descripcion]], columns=libro_cuentas.columns)
    libro_cuentas = pd.concat([libro_cuentas, nueva_cuenta], ignore_index=True)
    guardar_libro_cuentas()

def eliminar_cuenta(cuenta):
    global libro_cuentas
    libro_cuentas = libro_cuentas[libro_cuentas['Cuenta'] != cuenta]
    guardar_libro_cuentas()

def ver_libro_diario():
    global libro_diario
    return libro_diario.to_string(index=False)

def ver_balance_mayor():
    global balance_mayor
    return balance_mayor.to_string(index=False)

def ver_libro_cuentas():
    global libro_cuentas
    return libro_cuentas.to_string(index=False)

def guardar_en_csv(nueva_transaccion):
    file_path = obtener_ruta_csv()
    if not os.path.exists(file_path):
        nueva_transaccion.to_csv(file_path, index=False, mode='w')
    else:
        nueva_transaccion.to_csv(file_path, index=False, mode='a', header=False)

def guardar_libro_cuentas():
    libro_cuentas.to_csv(LIBRO_CUENTAS_FILE, index=False)

# Pantallas
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        cuentas_button = Button(text='Administrar Cuentas', size_hint_y=None, height=50)
        cuentas_button.bind(on_press=self.cambiar_a_cuentas)
        layout.add_widget(cuentas_button)

        diario_button = Button(text='Libro Diario', size_hint_y=None, height=50)
        diario_button.bind(on_press=self.cambiar_a_diario)
        layout.add_widget(diario_button)

        self.add_widget(layout)

    def cambiar_a_cuentas(self, instance):
        self.manager.current = 'cuentas'

    def cambiar_a_diario(self, instance):
        self.manager.current = 'diario'

class CuentasScreen(Screen):
    def __init__(self, **kwargs):
        super(CuentasScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.cuenta_input = TextInput(hint_text='Nombre de la nueva cuenta', multiline=False)
        layout.add_widget(self.cuenta_input)

        self.descripcion_input = TextInput(hint_text='Descripción de la nueva cuenta', multiline=False)
        layout.add_widget(self.descripcion_input)

        add_button = Button(text='Agregar Cuenta', size_hint_y=None, height=50)
        add_button.bind(on_press=self.agregar_cuenta)
        layout.add_widget(add_button)

        delete_button = Button(text='Eliminar Cuenta', size_hint_y=None, height=50)
        delete_button.bind(on_press=self.eliminar_cuenta)
        layout.add_widget(delete_button)

        self.result_label = Label(text='', size_hint_y=None, height=300)
        layout.add_widget(self.result_label)

        back_button = Button(text='Volver al Menú', size_hint_y=None, height=50)
        back_button.bind(on_press=self.volver_al_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)
        self.actualizar_resultados()

    def obtener_cuentas(self):
        return libro_cuentas['Cuenta'].tolist()

    def actualizar_resultados(self):
        self.result_label.text = ver_libro_cuentas()

    def agregar_cuenta(self, instance):
        cuenta = self.cuenta_input.text.strip()
        descripcion = self.descripcion_input.text.strip()

        if cuenta and descripcion:
            agregar_cuenta(cuenta, descripcion)
            self.result_label.text = f"Cuenta '{cuenta}' agregada con éxito."
            self.cuenta_input.text = ''
            self.descripcion_input.text = ''
            self.actualizar_resultados()
        else:
            self.result_label.text = "Por favor, complete todos los campos para registrar una nueva cuenta."

    def eliminar_cuenta(self, instance):
        cuenta = self.cuenta_input.text.strip()
        if cuenta in libro_cuentas['Cuenta'].values:
            eliminar_cuenta(cuenta)
            self.result_label.text = f"Cuenta '{cuenta}' eliminada con éxito."
            self.cuenta_input.text = ''
            self.actualizar_resultados()
        else:
            self.result_label.text = "La cuenta no existe."

    def volver_al_menu(self, instance):
        self.manager.current = 'menu'

class DiarioScreen(Screen):
    def __init__(self, **kwargs):
        super(DiarioScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.cuenta_spinner = Spinner(text='Selecciona una cuenta', values=self.obtener_cuentas(), size_hint_y=None, height=50)
        layout.add_widget(self.cuenta_spinner)

        self.debito_input = TextInput(hint_text='0.00', multiline=False, input_filter='float')
        layout.add_widget(self.debito_input)

        self.credito_input = TextInput(hint_text='0.00', multiline=False, input_filter='float')
        layout.add_widget(self.credito_input)

        self.descripcion_input = TextInput(hint_text='Descripción de la transacción', multiline=False)
        layout.add_widget(self.descripcion_input)

        add_button = Button(text='Agregar Transacción', size_hint_y=None, height=50)
        add_button.bind(on_press=self.agregar_transaccion)
        layout.add_widget(add_button)

        delete_button = Button(text='Eliminar Transacción', size_hint_y=None, height=50)
        delete_button.bind(on_press=self.eliminar_transaccion)
        layout.add_widget(delete_button)

        self.id_input = TextInput(hint_text='ID de la transacción', multiline=False)
        layout.add_widget(self.id_input)

        self.result_label = Label(text='', size_hint_y=None, height=300)
        layout.add_widget(self.result_label)

        back_button = Button(text='Volver al Menú', size_hint_y=None, height=50)
        back_button.bind(on_press=self.volver_al_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)
        self.actualizar_resultados()

    def obtener_cuentas(self):
        return libro_cuentas['Cuenta'].tolist()

    def actualizar_resultados(self):
        self.result_label.text = ver_libro_diario()

    def agregar_transaccion(self, instance):
        cuenta = self.cuenta_spinner.text
        debito = self.debito_input.text.strip()
        credito = self.credito_input.text.strip()
        descripcion = self.descripcion_input.text.strip()

        if cuenta and (debito or credito) and descripcion:
            debito_num = convertir_a_numero(debito)
            credito_num = convertir_a_numero(credito)
            agregar_transaccion(cuenta, debito_num, credito_num, descripcion)
            self.result_label.text = f"Transacción agregada con éxito en la cuenta '{cuenta}'."
            self.debito_input.text = ''
            self.credito_input.text = ''
            self.descripcion_input.text = ''
            self.actualizar_resultados()
        else:
            self.result_label.text = "Por favor, complete todos los campos para registrar una nueva transacción."

    def eliminar_transaccion(self, instance):
        id_transaccion = self.id_input.text.strip()
        if id_transaccion:
            eliminar_transaccion(id_transaccion)
            self.result_label.text = f"Transacción con ID '{id_transaccion}' eliminada con éxito."
            self.id_input.text = ''
            self.actualizar_resultados()
        else:
            self.result_label.text = "Por favor, ingrese un ID de transacción para eliminar."

    def volver_al_menu(self, instance):
        self.manager.current = 'menu'

class LibroDiarioApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CuentasScreen(name='cuentas'))
        sm.add_widget(DiarioScreen(name='diario'))
        return sm

if __name__ == '__main__':
    LibroDiarioApp().run()

