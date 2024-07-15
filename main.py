import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер изображений в TIFF")

        # Путь к папке с изображениями (можно изменить по необходимости)
        self.input_path = 'input'
        self.output_path = 'output'  # Путь к папке для сохранения TIFF файлов

        # Проверка существования папок input и output
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # Панель с выбором папок
        self.folder_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.folder_listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Заполнение списка папок
        self.update_folder_list()

        # Обработчики событий
        self.folder_listbox.bind("<Double-Button-1>", self.on_folder_select)
        self.folder_listbox.bind("<Return>", self.on_folder_select)

    def update_folder_list(self):
        # Очистка списка перед обновлением
        self.folder_listbox.delete(0, tk.END)

        # Получаем список папок в input_path
        folders = [folder for folder in os.listdir(self.input_path) if os.path.isdir(os.path.join(self.input_path, folder))]

        # Заполняем Listbox
        for folder in folders:
            self.folder_listbox.insert(tk.END, folder)

    def collect_images_from_folder(self, folder_path):
        images = []
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name.lower().endswith('.png'):
                    try:
                        image = Image.open(file_path)
                        images.append(image)
                    except Exception as e:
                        messagebox.showwarning("Предупреждение", f"Не удалось открыть файл {file_name}: {str(e)}")
        return images

    def create_image_grid(self, images, grid_size=(3, 3)):
        # Создаем холст для мозаики
        grid_width = grid_size[0] * images[0].width
        grid_height = grid_size[1] * images[0].height
        grid_image = Image.new('RGB', (grid_width, grid_height), (255, 255, 255))

        # Размещаем изображения на холсте
        for i, image in enumerate(images):
            row = i // grid_size[0]
            col = i % grid_size[0]
            grid_image.paste(image, (col * image.width, row * image.height))

        return grid_image

    def save_grid_to_tiff(self, grid_image, output_path):
        if grid_image:
            grid_image.save(output_path, format='TIFF')

    def convert_to_tiff(self):
        try:
            # Получаем выбранную папку
            selected_index = self.folder_listbox.curselection()
            if selected_index:
                selected_folder = self.folder_listbox.get(selected_index)
                folder_path = os.path.join(self.input_path, selected_folder)

                # Собираем все изображения из выбранной папки
                images = self.collect_images_from_folder(folder_path)

                if images:
                    # Создаем мозаику изображений
                    grid_image = self.create_image_grid(images)

                    # Создаем файл TIFF
                    output_folder_path = os.path.join(self.output_path, selected_folder)
                    os.makedirs(output_folder_path, exist_ok=True)
                    output_tiff_path = os.path.join(output_folder_path, f"{selected_folder}.tif")

                    # Сохраняем мозаику как TIFF
                    self.save_grid_to_tiff(grid_image, output_tiff_path)
                    messagebox.showinfo("Готово", f"TIFF файл создан успешно: {output_tiff_path}")
                else:
                    messagebox.showwarning("Предупреждение", "В выбранной папке нет поддерживаемых изображений.")
            else:
                messagebox.showwarning("Отмена", "Выберите папку для конвертации.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при конвертации: {str(e)}")

    def on_folder_select(self, event=None):
        # Метод для обработки выбора папки из Listbox
        self.convert_to_tiff()  # Вызываем конвертацию при выборе папки

def main():
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
