import tkinter as tk
from tkinter import messagebox, filedialog
import xml_generator as XG

root = tk.Tk()
root.title("XML Format Modifier")
window_width = 550
window_height = 450
root.geometry(f"{window_width}x{window_height}")

offsetx = 4
offsety = 0

xml_modifier = XG.XMLModifier()

user_column_color = "0B2531"
user_row_color = "F0F8FF"
user_accent_row_color = "FF8C00"
user_subheading_color = "CFE9FF"

user_color_list = [user_column_color, user_row_color, user_accent_row_color, user_subheading_color]

tk.Label(root, text=r"Enter filepath (format : C\Users\documents)", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(10, 5))
filepath_entry = tk.Entry(root, width=50)
filepath_entry.grid(row=1, column=0, columnspan=5, padx=(20, 5), pady=5)

ui_entries = []
preview_widgets = []
row_widgets = []
color_list = []

def populate_color_rows():
    global form_list_last_row, color_list
    
    for widget in row_widgets:
        widget.destroy()
    row_widgets.clear()
    
    ui_entries.clear()
    preview_widgets.clear()
    
    raw_colors = xml_modifier.get_colors()
    excluded_colors = {"FFFFFF", "000000", "#FFFFFF", "#000000"}
    color_list = [c for c in raw_colors if c[1] not in excluded_colors]

    headers = ["ID Name", "Original", "Preview", "New Hex"]
    for col, text in enumerate(headers):
        lbl = tk.Label(root, text=text, font=("Arial", 10, "bold"))
        lbl.grid(row=offsetx, column=col+offsety, pady=5)
        row_widgets.append(lbl)

    form_list_last_row = offsetx
    for i, (c_id, hex_val) in enumerate(color_list):
        current_row = i + offsetx + 1
        
        id_label = tk.Label(root, text=c_id, font=("Arial", 10, "bold"))
        id_label.grid(row=current_row, column=0+offsety, padx=5)
        row_widgets.append(id_label)
        
        hex_label = tk.Label(root, text=f"#{hex_val}")
        hex_label.grid(row=current_row, column=1+offsety, padx=5)
        row_widgets.append(hex_label)
        
        canvas = tk.Canvas(root, height=25, width=25, bg=f"#{hex_val}", bd=1, relief="solid")
        canvas.grid(row=current_row, column=2+offsety, padx=5)
        row_widgets.append(canvas)
        
        entry = tk.Entry(root, width=15)
        entry.insert(0, f"{hex_val}") 
        entry.grid(row=current_row, column=3+offsety, padx=10)
        ui_entries.append(entry)
        row_widgets.append(entry)
        
        form_list_last_row = current_row
        
    btn_frame.grid(row=form_list_last_row+2, column=0, columnspan=10, pady=20)

def load_file_action():
    path = filepath_entry.get().strip().replace('"', '')
    if not path:
        messagebox.showwarning("Warning", "Please enter a file path first.")
        return

    try:
        xml_modifier.load_file(path)
        populate_color_rows()
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file: {e}")

def browse_file_action():
    filename = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if filename:
        filepath_entry.delete(0, tk.END)
        filepath_entry.insert(0, filename)
        load_file_action()

tk.Button(root, text="Browse", command=browse_file_action).grid(row=1, column=5, padx=(0, 20), pady=5)
tk.Button(root, text="Load File", command=load_file_action, width=20).grid(row=2, column=0, columnspan=6, pady=(5, 15))

def run_validation_and_preview():
    for widget in preview_widgets:
        widget.destroy()
    preview_widgets.clear()
    
    clean_data = []
    has_error = False
    
    for i, entry_widget in enumerate(ui_entries):
        raw_val = entry_widget.get().strip()
        final_color = raw_val if raw_val.startswith("#") else f"#{raw_val}"
        
        try:
            current_row = i + offsetx + 1
            canvas = tk.Canvas(root, height=25, width=25, bg=final_color, bd=1, relief="solid")
            canvas.grid(row=current_row, column=5+offsety, padx=10)
            preview_widgets.append(canvas)
            
            original_id = color_list[i][0]
            clean_data.append((original_id, raw_val))

        except tk.TclError:
            has_error = True
            current_row = i + offsetx + 1
            err_lbl = tk.Label(root, text="Invalid", fg="red", font=("Arial", 9, "bold"))
            err_lbl.grid(row=current_row, column=5+offsety)
            preview_widgets.append(err_lbl)
    
    if has_error:
        return False, []
    else:
        return True, clean_data

def update_preview():
    run_validation_and_preview()

def inject_entries():
    is_valid, data = run_validation_and_preview()
    
    if not is_valid:
        messagebox.showerror("Injection Failed", "Please fix the red 'Invalid' fields before injecting.")
        return
    
    try:
        xml_modifier.inject_colors(data)
        messagebox.showinfo("Success", "Colors injected and file saved!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save XML: {e}")

btn_frame = tk.Frame(root)
tk.Button(btn_frame, text="Generate Preview", command=update_preview).pack(side="left", padx=10)
tk.Button(btn_frame, text="Inject XML", command=inject_entries).pack(side="left", padx=10)

root.mainloop()