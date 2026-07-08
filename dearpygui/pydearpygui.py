import dearpygui.dearpygui as dpg

numer_ventana = 1

dpg.create_context()

dpg.create_viewport(title='Custom Title', width=600, height=400)

def btn_save_click(sender, app_data):
    print("Save Clicked!!!!")
    global numer_ventana
    with dpg.window(tag=f"Save_{numer_ventana}", label="Save", autosize=True, no_resize=True, no_collapse=True, no_close=True):
        dpg.add_text("Save Clicked!!!!")
        dpg.add_button(label="Close", callback=lambda s, a, u: dpg.delete_item(u), user_data=f"Save_{numer_ventana}")
    numer_ventana += 1


with dpg.window(label="Tutorial", autosize=True, no_resize=True, no_collapse=True, no_close=True):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save", callback=btn_save_click)
    dpg.add_input_text(label="string")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()