import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import qrcode
from PIL import Image, ImageTk
import io

class WireGuardQRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("WireGuard QR Generator")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Создаем основной фрейм
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="WireGuard QR Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Левая панель - ввод конфигурации
        left_frame = ttk.LabelFrame(main_frame, text="Конфигурация WireGuard", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Инструкция
        instruction_label = ttk.Label(left_frame, 
                                    text="Вставьте конфигурацию WireGuard в поле ниже:",
                                    font=('Arial', 10))
        instruction_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Текстовое поле для конфигурации
        self.config_text = scrolledtext.ScrolledText(left_frame, 
                                                   width=40, 
                                                   height=15,
                                                   font=('Consolas', 10),
                                                   wrap=tk.WORD)
        self.config_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Кнопки управления
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        self.generate_btn = ttk.Button(button_frame, text="Генерировать QR", 
                                     command=self.generate_qr)
        self.generate_btn.grid(row=0, column=0, padx=(0, 3), sticky=(tk.W, tk.E))
        
        self.copy_btn = ttk.Button(button_frame, text="Копировать", 
                                 command=self.copy_text)
        self.copy_btn.grid(row=0, column=1, padx=3, sticky=(tk.W, tk.E))
        
        self.clear_btn = ttk.Button(button_frame, text="Очистить", 
                                  command=self.clear_text)
        self.clear_btn.grid(row=0, column=2, padx=(3, 0), sticky=(tk.W, tk.E))
        
        # Правая панель - QR код
        right_frame = ttk.LabelFrame(main_frame, text="QR Код", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Информация о QR коде
        self.qr_info_label = ttk.Label(right_frame, 
                                     text="QR код появится здесь после генерации",
                                     font=('Arial', 10),
                                     foreground='gray')
        self.qr_info_label.grid(row=0, column=0, pady=(0, 10))
        
        # Фрейм для QR кода
        self.qr_frame = ttk.Frame(right_frame)
        self.qr_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.qr_frame.columnconfigure(0, weight=1)
        self.qr_frame.rowconfigure(0, weight=1)
        
        # Настраиваем горячие клавиши и контекстное меню
        self.setup_keyboard_shortcuts()
        self.setup_context_menu()
        
        # Вставляем пример конфигурации
        self.insert_example_config()
        
    def insert_example_config(self):
        """Вставляет пример конфигурации в текстовое поле"""
        example_config = """[Interface]
ListenPort = 51820
PrivateKey = qIfIZwxGv5Amog0IR93nZpDRBiisuVwXLCS+N09RMH0=
Address = 10.10.21.2/24
DNS = 10.10.21.1

[Peer]
PublicKey = g/qb7Xv4vSQT5jo2+7k5eber7fs3MqeegTT9QWzHpg0=
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 46.234.29.170:51810
PresharedKey = GJgXTNRQ7AAiv/5ThPN0INmkpMK7bXqwGJRmd3qiS3g=
PersistentKeepalive = 16"""
        
        self.config_text.insert(tk.END, example_config)
    
    def setup_keyboard_shortcuts(self):
        """Настраивает горячие клавиши"""
        # Привязываем горячие клавиши к текстовому полю
        self.config_text.bind('<Control-v>', lambda e: self.paste_text())
        self.config_text.bind('<Control-V>', lambda e: self.paste_text())
        self.config_text.bind('<Control-c>', lambda e: self.copy_text())
        self.config_text.bind('<Control-C>', lambda e: self.copy_text())
        self.config_text.bind('<Control-a>', lambda e: self.select_all_text())
        self.config_text.bind('<Control-A>', lambda e: self.select_all_text())
        
        # Привязываем горячие клавиши к главному окну
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.root.bind('<Control-V>', lambda e: self.paste_text())
        self.root.bind('<Control-c>', lambda e: self.copy_text())
        self.root.bind('<Control-C>', lambda e: self.copy_text())
        self.root.bind('<Control-a>', lambda e: self.select_all_text())
        self.root.bind('<Control-A>', lambda e: self.select_all_text())
    
    def setup_context_menu(self):
        """Настраивает контекстное меню"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Вырезать", command=self.cut_text)
        self.context_menu.add_command(label="Копировать", command=self.copy_text)
        self.context_menu.add_command(label="Вставить", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Выделить всё", command=self.select_all_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Очистить", command=self.clear_text)
        
        # Привязываем контекстное меню к текстовому полю
        self.config_text.bind('<Button-3>', self.show_context_menu)
        self.config_text.bind('<Control-Button-1>', self.show_context_menu)
    
    def show_context_menu(self, event):
        """Показывает контекстное меню"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def paste_text(self):
        """Вставляет текст из буфера обмена"""
        try:
            self.config_text.event_generate('<<Paste>>')
        except tk.TclError:
            pass
    
    def copy_text(self):
        """Копирует выделенный текст в буфер обмена"""
        try:
            self.config_text.event_generate('<<Copy>>')
        except tk.TclError:
            pass
    
    def cut_text(self):
        """Вырезает выделенный текст"""
        try:
            self.config_text.event_generate('<<Cut>>')
        except tk.TclError:
            pass
    
    def select_all_text(self):
        """Выделяет весь текст"""
        self.config_text.tag_add(tk.SEL, "1.0", tk.END)
        self.config_text.mark_set(tk.INSERT, "1.0")
        self.config_text.see(tk.INSERT)
    
    def generate_qr(self):
        """Генерирует QR код из конфигурации"""
        config_text = self.config_text.get("1.0", tk.END).strip()
        
        if not config_text:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите конфигурацию WireGuard")
            return
        
        try:
            # Создаем QR код
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(config_text)
            qr.make(fit=True)
            
            # Создаем изображение QR кода
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Изменяем размер изображения для отображения
            qr_image = qr_image.resize((300, 300), Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage для tkinter
            self.qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Очищаем предыдущий QR код
            for widget in self.qr_frame.winfo_children():
                widget.destroy()
            
            # Создаем лейбл с QR кодом
            qr_label = ttk.Label(self.qr_frame, image=self.qr_photo)
            qr_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Обновляем информацию
            self.qr_info_label.config(
                text=f"QR код сгенерирован успешно!\nРазмер: {len(config_text)} символов",
                foreground='green'
            )
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при генерации QR кода: {str(e)}")
            self.qr_info_label.config(
                text="Ошибка при генерации QR кода",
                foreground='red'
            )
    
    def clear_text(self):
        """Очищает текстовое поле"""
        self.config_text.delete("1.0", tk.END)
        
        # Очищаем QR код
        for widget in self.qr_frame.winfo_children():
            widget.destroy()
        
        self.qr_info_label.config(
            text="QR код появится здесь после генерации",
            foreground='gray'
        )

def main():
    root = tk.Tk()
    app = WireGuardQRGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
