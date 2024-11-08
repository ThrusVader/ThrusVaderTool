import os
import tkinter as tk
from tkinter import Menu, PhotoImage, filedialog, Toplevel, messagebox, Canvas, Scale, HORIZONTAL, Button
from PIL import Image, ImageTk, ImageEnhance

# Função para carregar ícones
def load_icon(icon_name):
    base_path = os.path.join(os.path.dirname(__file__), 'assets', 'img')
    icon_path = os.path.join(base_path, icon_name)
    return ImageTk.PhotoImage(Image.open(icon_path).resize((35, 35), Image.Resampling.LANCZOS))

# Variáveis globais
global img, img_colors, img_tk, canvas, canvas_image, zoom_level, blocks_drawn, original_img, temp_img, backup_img
# noinspection PyRedeclaration
img = None
# noinspection PyRedeclaration
img_colors = []
# noinspection PyRedeclaration
canvas_image = None
# noinspection PyRedeclaration
zoom_level = 1.0
# noinspection PyRedeclaration
blocks_drawn = False
# noinspection PyRedeclaration
original_img = None
# noinspection PyRedeclaration
temp_img = None
# noinspection PyRedeclaration
backup_img = None

# Criando a janela principal
root = tk.Tk()
root.title("ThrusVader Tool 1.0 - TVT")
root.geometry("1024x768")
root.configure(bg="#323232")  # Cor de fundo

# Adicionando a logo como ícone da janela
logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'img', 'logo.png')
logo_image = PhotoImage(file=logo_path)
root.iconphoto(False, logo_image)

# Criando um Frame para o menu lateral
side_menu = tk.Frame(root, width=50, bg="#414141")
side_menu.pack(side="left", fill="y")



# Funções de Zoom In e Zoom Out
def zoom_in():
    global img, img_tk, canvas_image, zoom_level
    if img:
        zoom_level *= 1.2
        new_size = (int(min(img.width * zoom_level, 700)), int(min(img.height * zoom_level, 500)))
        img_resized = img.resize(new_size, Image.Resampling.NEAREST)
        img_tk = ImageTk.PhotoImage(img_resized)
        canvas.itemconfig(canvas_image, image=img_tk)
        center_image()
        print("Zoom In")

def zoom_out():
    global img, img_tk, canvas_image, zoom_level
    if img:
        zoom_level /= 1.2
        new_size = (int(min(img.width * zoom_level, 700)), int(min(img.height * zoom_level, 500)))
        img_resized = img.resize(new_size, Image.Resampling.NEAREST)
        img_tk = ImageTk.PhotoImage(img_resized)
        canvas.itemconfig(canvas_image, image=img_tk)
        center_image()
        print("Zoom Out")

# Carregando as imagens dos ícones
zoom_in_photo = load_icon('ampliar.png')
zoom_out_photo = load_icon('diminuir.png')

# Funções para o efeito de hover
def on_enter(event):
    event.widget.config(bg="#555555")  # Cor de fundo mais clara ao passar o mouse

def on_leave(event):
    event.widget.config(bg="#414141")  # Cor de fundo original ao sair com o mouse

# Adicionando botões ao menu lateral
zoom_in_button = tk.Button(side_menu, image=zoom_in_photo, command=zoom_in, bg="#414141", borderwidth=0)
zoom_in_button.pack(pady=10)
zoom_in_button.bind("<Enter>", on_enter)
zoom_in_button.bind("<Leave>", on_leave)
zoom_out_button = tk.Button(side_menu, image=zoom_out_photo, command=zoom_out, bg="#414141", borderwidth=0)
zoom_out_button.pack(pady=10)
zoom_out_button.bind("<Enter>", on_enter)
zoom_out_button.bind("<Leave>", on_leave)

# Criando um Canvas para exibir a imagem
# noinspection PyRedeclaration
canvas = tk.Canvas(root, bg="#323232", highlightthickness=0)
canvas.pack(expand=True, fill="both")

# Função para centralizar o retângulo
def center_rectangle(event=None):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    rect_size = (700, 500)
    # Ajusta a posição do retângulo
    canvas.coords(rect, (canvas_width / 2 - rect_size[0] / 2, canvas_height / 2 - rect_size[1] / 2,
                         canvas_width / 2 + rect_size[0] / 2, canvas_height / 2 + rect_size[1] / 2))

# Vinculando o redimensionamento da janela à função de centralização
canvas.bind("<Configure>", center_rectangle)

# Desenhando um retângulo branco no Canvas para representar a área da imagem
rect = canvas.create_rectangle(0, 0, 700, 500, outline="white", width=2, fill="white")
center_rectangle()

# Vinculando o redimensionamento da janela à função de centralização
# noinspection PyTypeChecker
canvas.bind("<Configure>", center_rectangle)

def open_file():
    global img, img_colors, img_tk, canvas_image, zoom_level, original_img, backup_img
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if filepath:
        img = Image.open(filepath)
        img = img.convert("RGBA")  # Usar RGBA para suportar transparência
        original_img = img.copy()  # Salvar a imagem original
        backup_img = img.copy()  # Criar um backup da imagem original
        img_colors = list(img.getdata())  # Salvar as cores da imagem
        img.thumbnail((700, 500), Image.Resampling.LANCZOS)  # Redimensionar a imagem mantendo a proporção
        img_tk = ImageTk.PhotoImage(img)
        canvas_image = canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, image=img_tk)  # Centralizar a imagem no Canvas
        zoom_level = 1.0
        print("Image loaded successfully")

def update_image():
    global img_tk, canvas_image
    img_tk = ImageTk.PhotoImage(img)
    canvas.itemconfig(canvas_image, image=img_tk)

def save_file():
    print("Save File")

def save_as():
    print("Save As")

def adjust_brightness():
    # noinspection PyUnboundLocalVariable
    if img is None:
        messagebox.showerror("Error", "A imagem não foi carregada corretamente.")
        return

    # Criar uma nova janela para ajuste de brilho
    brightness_window = Toplevel(root)
    brightness_window.title("Ajustar Brilho")
    brightness_window.geometry("300x150")
    brightness_window.configure(bg="#323232")

    def update_brightness(value):
        global img, img_tk, canvas_image, temp_img
        enhancer = ImageEnhance.Brightness(img)
        temp_img = enhancer.enhance(float(value))
        img_tk = ImageTk.PhotoImage(temp_img)
        canvas.itemconfig(canvas_image, image=img_tk)

    def apply_brightness():
        global img, original_img, temp_img
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja aplicar essa alteração?"):
            original_img = temp_img.copy()  # Atualizar a imagem original com o brilho aplicado
            img = temp_img.copy()
        else:
            # noinspection PyShadowingNames
            img_tk = ImageTk.PhotoImage(original_img)
            # noinspection PyTypeChecker
            canvas.itemconfig(canvas_image, image=img_tk)

    def reset_brightness():
        global img, img_tk, canvas_image, original_img
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja voltar ao original?"):
            img = original_img.copy()  # Restaurar a imagem original
            img_tk = ImageTk.PhotoImage(img)
            canvas.itemconfig(canvas_image, image=img_tk)
            brightness_scale.set(1.0)  # Resetar a barra de brilho
        else:
            img_tk = ImageTk.PhotoImage(temp_img)
            canvas.itemconfig(canvas_image, image=img_tk)

    # Adicionar uma barra de porcentagem para ajustar o brilho
    brightness_scale = Scale(brightness_window, from_=0.0, to=2.0, resolution=0.1, orient=HORIZONTAL, length=250, command=update_brightness)
    brightness_scale.set(1.0)  # Valor inicial
    brightness_scale.pack(pady=10)

    # Adicionar botões para aplicar e resetar o brilho
    apply_button = Button(brightness_window, text="Aplicar Brilho", command=apply_brightness)
    apply_button.pack(side="left", padx=10, pady=10)

    reset_button = Button(brightness_window, text="Voltar ao Original", command=reset_brightness)
    reset_button.pack(side="right", padx=10, pady=10)

def adjust_hue_saturation():
    global img
    img = img.convert("RGB")
    img = img.point(lambda p: p * 1.1)  # Aumentar a saturação em 10%
    update_image()
    print("Hue and Saturation adjusted")

def sort_colors():
    global img_colors
    # Organiza as cores por seus valores RGB (Red, Green, Blue)
    img_colors_sorted = sorted(set(img_colors), key=lambda color: (color[0], color[1], color[2]))

    # Atualiza a tabela com as cores ordenadas
    color_table(img_colors_sorted)

def color_table(sorted_colors=None):
    if img is None:
        messagebox.showerror("Error", "A imagem não foi carregada corretamente.")
        return

    # Criar uma nova janela para a Tabela de Cores
    color_window = Toplevel(root)
    color_window.title("Tabela de Cores")
    color_window.geometry("320x400")
    color_window.configure(bg="#323232")

    # Criar um Canvas para desenhar os blocos de cores
    block_size = 20
    # noinspection PyShadowingNames
    canvas: Canvas = tk.Canvas(color_window, width=16 * block_size, height=16 * block_size, bg="#414141", highlightthickness=0)
    canvas.pack(pady=10)

    # Se não for fornecido um conjunto de cores ordenadas, usar o original
    if sorted_colors is None:
        sorted_colors = list(set(img_colors))[:256]  # Limitando a 256 cores únicas

    # Preenchendo a tabela com cores da imagem
    color_index = 0
    for j in range(16):
        for i in range(16):
            if color_index < len(sorted_colors):
                color = "#{:02x}{:02x}{:02x}".format(*sorted_colors[color_index])
                x1 = i * block_size
                y1 = j * block_size
                x2 = x1 + block_size
                y2 = y1 + block_size
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                color_index += 1

    # Adicionando o botão para organizar as cores
    sort_button = tk.Button(color_window, text="Organizar Cores", command=sort_colors)
    sort_button.pack(pady=10)

# Função de saída
def exit_application():
    root.quit()

def change_rectangle_color():
    current_color = canvas.itemcget(rect, "fill")
    new_color = "" if current_color == "white" else "white"
    canvas.itemconfig(rect, fill=new_color)

def center_image():
    # noinspection PyTypeChecker
    canvas.coords(canvas_image, canvas.coords(rect)[0] + 350, canvas.coords(rect)[1] + 250)

# Criando a barra de menu
menu_bar = Menu(root)

# Criando o menu 'File'
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()  # Adiciona uma linha separadora
file_menu.add_command(label="Exit", command=exit_application)  # Adiciona a opção Exit dentro do menu 'File'
menu_bar.add_cascade(label="File", menu=file_menu)

# Criando o menu 'Options'
options_menu = Menu(menu_bar, tearoff=0)

# Criando o submenu 'Image'
image_submenu = Menu(options_menu, tearoff=0)
image_submenu.add_command(label="Adjust Brightness", command=adjust_brightness)
image_submenu.add_command(label="Adjust Hue and Saturation", command=adjust_hue_saturation)
image_submenu.add_command(label="Color Table", command=color_table)
image_submenu.add_command(label="Change Background Color", command=change_rectangle_color)

# Adicionando o submenu 'Image' ao menu 'Options'
options_menu.add_cascade(label="Image", menu=image_submenu)

# Adicionando o menu 'Options' à barra de menu
menu_bar.add_cascade(label="Options", menu=options_menu)

# Configurando a barra de menu na janela
root.config(menu=menu_bar)

# Alterando a cor da barra de título
root.configure(bg="#414141")  # Cor de fundo da janela principal
root.title("ThrusVader Tool 1.0 - TVT")  # Atualizar o título

# Função para o efeito de hover no menu
# Função para o efeito de hover no menu e submenu
def on_menu_enter(event):
    event.widget.config(bg="#555555")  # Cor de fundo mais clara ao passar o mouse

def on_menu_leave(event):
    event.widget.config(bg="#414141")  # Cor de fundo original ao sair com o mouse

# Criando a barra de menu
menu_bar = Menu(root, bg="#414141", activebackground="#555555")  # Cor de fundo do menu e a cor ativa

# Criando o menu 'File'
file_menu = Menu(menu_bar, tearoff=0, bg="#414141", fg="white")
file_menu.add_command(label="Open", command=open_file, activebackground="#555555", activeforeground="white")
file_menu.add_command(label="Save", command=save_file, activebackground="#555555", activeforeground="white")
file_menu.add_command(label="Save As", command=save_as, activebackground="#555555", activeforeground="white")
file_menu.add_separator()  # Linha separadora
file_menu.add_command(label="Exit", command=exit_application, activebackground="#555555", activeforeground="white")
menu_bar.add_cascade(label="File", menu=file_menu)

# Criando o menu 'Options'
options_menu = Menu(menu_bar, tearoff=0, bg="#414141", fg="white")

# Criando o submenu 'Image'
image_submenu = Menu(options_menu, tearoff=0, bg="#414141", fg="white")
image_submenu.add_command(label="Adjust Brightness", command=adjust_brightness, activebackground="#555555", activeforeground="white")
image_submenu.add_command(label="Adjust Hue and Saturation", command=adjust_hue_saturation, activebackground="#555555", activeforeground="white")
image_submenu.add_command(label="Color Table", command=color_table, activebackground="#555555", activeforeground="white")
image_submenu.add_command(label="Change Background Color", command=change_rectangle_color, activebackground="#555555", activeforeground="white")

# Adicionando o submenu 'Image' ao menu 'Options'
options_menu.add_cascade(label="Image", menu=image_submenu)

# Adicionando o menu 'Options' à barra de menu
menu_bar.add_cascade(label="Options", menu=options_menu)

# Configurando a barra de menu na janela
root.config(menu=menu_bar)

# Aplicando o efeito hover nas opções do menu principal
for menu_item in menu_bar.winfo_children():
    menu_item.bind("<Enter>", on_menu_enter)  # Ao passar o mouse, mudar a cor de fundo
    menu_item.bind("<Leave>", on_menu_leave)  # Ao sair com o mouse, voltar à cor original

# Aplicando o efeito hover nas opções do submenu "Image"
for submenu_item in image_submenu.winfo_children():
    submenu_item.bind("<Enter>", on_menu_enter)  # Ao passar o mouse, mudar a cor de fundo
    submenu_item.bind("<Leave>", on_menu_leave)  # Ao sair com o mouse, voltar à cor original

# Iniciando a aplicação
root.mainloop()
