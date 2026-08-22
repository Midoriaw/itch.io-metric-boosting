import time
import threading
import customtkinter as ctk
from bot_logic import ItchBot, TikTokBot

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class BotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("D:ROCHILA")
        self.geometry("750x520")
        self.resizable(False, False)

        self.is_running = False
        self.bot_thread = None
        self.iteration_count = 0

     
        self.itch_bot = ItchBot(log_func=self.log)
        self.tiktok_bot = TikTokBot(log_func=self.log)

        self.current_tab = "itch"

        self.sidebar_is_open = True
        self.sidebar_width = 160


        self.grid_columnconfigure(0, weight=0)  # кнопка toggle
        self.grid_columnconfigure(1, weight=0)  # сайдбар
        self.grid_columnconfigure(2, weight=1)  # контент
        self.grid_rowconfigure(0, weight=1)

    
        self.toggle_frame = ctk.CTkFrame(self, width=40, fg_color="transparent")
        self.toggle_frame.grid(row=0, column=0, sticky="nsew")
        self.toggle_frame.grid_propagate(False)

        self.btn_toggle_sidebar = ctk.CTkButton(
            self.toggle_frame, text="≡", width=30, height=30,
            fg_color="#1E1E24", hover_color="#2A2A32",
            font=("Arial", 18, "bold"), command=self.toggle_sidebar,
            corner_radius=6
        )
        self.btn_toggle_sidebar.pack(anchor="center", pady=10)

    
        self.sidebar_frame = ctk.CTkFrame(self, width=self.sidebar_width, corner_radius=0, fg_color="#1E1E24")
        self.sidebar_frame.grid(row=0, column=1, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        self.btn_tab_itch = ctk.CTkButton(
            self.sidebar_frame, text="🎮 Itch.io", anchor="w", fg_color="#2A2A32",
            hover_color="#3A3A45", command=lambda: self.switch_tab("itch"),
            corner_radius=8
        )
        self.btn_tab_itch.pack(fill="x", padx=10, pady=(20, 5))

        self.btn_tab_tt = ctk.CTkButton(
            self.sidebar_frame, text="🎵 TikTok", anchor="w", fg_color="transparent",
            hover_color="#2A2A32", command=lambda: self.switch_tab("tt"),
            corner_radius=8
        )
        self.btn_tab_tt.pack(fill="x", padx=10, pady=5)

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=2, sticky="nsew", padx=20, pady=10)

   
        self.label_url = ctk.CTkLabel(self.content_frame, text="Ссылка на игру Itch.io:", font=("Arial", 14, "bold"))
        self.label_url.pack(pady=(10, 5), anchor="w")

     
        self.entry_url = ctk.CTkEntry(
            self.content_frame, height=35,
            placeholder_text="https://itch.io",
            border_color="#3A3A45", fg_color="#1E1E24",
            corner_radius=8
        )
        self.entry_url.pack(pady=5, fill="x")
        self.setup_hotkeys()

       
        self.settings_frame = ctk.CTkFrame(self.content_frame, fg_color="#1E1E24", corner_radius=10)
        self.settings_frame.pack(pady=15, fill="x")

        settings_row = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        settings_row.pack(fill="x", padx=15, pady=15)

      
        col1 = ctk.CTkFrame(settings_row, fg_color="transparent")
        col1.pack(side="left", expand=True, fill="x", padx=(0, 10))

        ctk.CTkLabel(col1, text="Количество запусков", font=("Arial", 11), text_color="gray").pack(anchor="w",
                                                                                                   pady=(0, 5))

        self.entry_amount = ctk.CTkEntry(
            col1, height=32,
            placeholder_text="0 = ∞",
            border_color="#3A3A45", fg_color="#2A2A32",
            corner_radius=6, font=("Arial", 12, "bold"),
            justify="center"
        )
        self.entry_amount.pack(fill="x")
        self.entry_amount.insert(0, "0")

     
        col2 = ctk.CTkFrame(settings_row, fg_color="transparent")
        col2.pack(side="left", expand=True, fill="x")

        ctk.CTkLabel(col2, text="Скорость выполнения", font=("Arial", 11), text_color="gray").pack(anchor="w",
                                                                                                   pady=(0, 5))

        self.speed_var = ctk.StringVar(value="Средняя")
        self.speed_menu = ctk.CTkOptionMenu(
            col2, values=["Медленная", "Средняя", "Быстрая"],
            variable=self.speed_var,
            fg_color="#2A2A32", button_color="#3A3A45",
            button_hover_color="#4A4A55",
            corner_radius=6, height=32,
            font=("Arial", 12, "bold")
        )
        self.speed_menu.pack(fill="x")

        self.counter_frame = ctk.CTkFrame(self.content_frame, fg_color="#1E1E24", corner_radius=8)
        self.counter_frame.pack(pady=10)

        self.iteration_label = ctk.CTkLabel(
            self.counter_frame, text="0",
            font=("Arial", 18, "bold"), text_color="#2ecc71"
        )
        self.iteration_label.pack(side="left", padx=(15, 5), pady=10)

        self.iteration_desc = ctk.CTkLabel(
            self.counter_frame, text="запусков",
            font=("Arial", 11), text_color="gray"
        )
        self.iteration_desc.pack(side="left", padx=(0, 15), pady=10)

       
        self.label_status = ctk.CTkLabel(
            self.content_frame, text="Готов к работе",
            font=("Arial", 12, "italic"), text_color="#3498db"
        )
        self.label_status.pack(pady=5)

       
        self.frame_buttons = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.frame_buttons.pack(pady=10, anchor="center")

        self.btn_start = ctk.CTkButton(
            self.frame_buttons, text="▶  Старт", width=140, height=40,
            fg_color="#2ecc71", hover_color="#27ae60",
            text_color="white", font=("Arial", 13, "bold"),
            corner_radius=10, command=self.start_bot
        )
        self.btn_start.grid(row=0, column=0, padx=10)

        self.btn_stop = ctk.CTkButton(
            self.frame_buttons, text="■  Стоп", width=140, height=40,
            fg_color="#e74c3c", hover_color="#c0392b",
            text_color="white", font=("Arial", 13, "bold"),
            corner_radius=10, command=self.stop_bot, state="disabled"
        )
        self.btn_stop.grid(row=0, column=1, padx=10)


    def toggle_sidebar(self):
        if self.sidebar_is_open:
            self.sidebar_frame.grid_remove()
            self.sidebar_is_open = False
        else:
            self.sidebar_frame.grid()
            self.sidebar_is_open = True

    def switch_tab(self, tab_name):
        self.current_tab = tab_name

        if tab_name == "itch":
            self.btn_tab_itch.configure(fg_color="#2A2A32")
            self.btn_tab_tt.configure(fg_color="transparent")
         
            self.label_url.configure(text="Ссылка на игру Itch.io:")
            self.entry_url.configure(placeholder_text="https://itch.io")

        elif tab_name == "tt":
            self.btn_tab_itch.configure(fg_color="transparent")
            self.btn_tab_tt.configure(fg_color="#2A2A32")
        
            self.label_url.configure(text="Ссылка на видео TikTok:")
            self.entry_url.configure(placeholder_text="https://tiktok.com/@user/video/...")

    def setup_hotkeys(self):
        """Привязка стандартных комбинаций клавиш"""
        self.entry_url.bind("<Control-v>", lambda e: self.entry_url.event_generate("<<Paste>>"))
        self.entry_url.bind("<Control-V>", lambda e: self.entry_url.event_generate("<<Paste>>"))
        self.entry_url.bind("<Control-c>", lambda e: self.entry_url.event_generate("<<Copy>>"))
        self.entry_url.bind("<Control-C>", lambda e: self.entry_url.event_generate("<<Copy>>"))
        self.entry_url.bind("<Control-x>", lambda e: self.entry_url.event_generate("<<Cut>>"))
        self.entry_url.bind("<Control-X>", lambda e: self.entry_url.event_generate("<<Cut>>"))
        self.entry_url.bind("<Control-a>", lambda e: self.entry_url.event_generate("<<SelectAll>>"))
        self.entry_url.bind("<Control-A>", lambda e: self.entry_url.event_generate("<<SelectAll>>"))

    def log(self, text):
        """Логирует только важные сообщения"""
        skip_messages = [
            "Открываем страницу:",
            "Имитируем игровую сессию",
            "Закрываем окно браузера",
            "Клик по кнопке",
            "Пауза",
            "Открываем TikTok видео:",
            "Видео загружено",
            "Просмотр видео",
            "Просмотр завершен",
            "Закрываем браузер"
        ]

        if any(skip in text for skip in skip_messages):
            return

        print(f"[{time.strftime('%H:%M')}] {text}")

    def update_iteration(self):
        """Обновляет счетчик итераций"""
        self.iteration_count += 1
        self.after(0, lambda: self.iteration_label.configure(text=str(self.iteration_count)))

    def get_timing_by_speed(self):
        """Возвращает (session_duration, delay) в зависимости от скорости"""
        speed = self.speed_var.get()
        if speed == "Медленная":
            return 10.0, 5.0
        elif speed == "Быстрая":
            return 2.0, 0.5
        else:
            return 5.0, 2.0

    def bot_loop(self, bot, method_name, target_url, max_iterations, session_duration, delay):
        iteration = 1
        bot_method = getattr(bot, method_name)

        while self.is_running:
            if max_iterations > 0 and iteration > max_iterations:
                self.log(f"Достигнут лимит: {max_iterations}")
                break

            self.update_iteration()
            self.log(f"Запуск #{iteration}")

            bot_method(target_url, session_duration=session_duration)

            for _ in range(int(delay * 10)):
                if not self.is_running:
                    break
                time.sleep(0.1)

            iteration += 1

        self.log("Работа остановлена")
        self.after(0, self.reset_ui_state)

    def start_bot(self):
        target_url = self.entry_url.get().strip()
        if not target_url:
            error_msg = "Нужна ссылка на игру!" if self.current_tab == "itch" else "Нужна ссылка на видео!"
            self.label_status.configure(text=f"Ошибка: {error_msg}", text_color="#e74c3c")
            return

        try:
            amount_str = self.entry_amount.get().strip()
            max_iterations = int(amount_str) if amount_str else 0
            if max_iterations < 0:
                max_iterations = 0
        except ValueError:
            max_iterations = 0

        session_duration, delay = self.get_timing_by_speed()

        self.label_status.configure(text="Работает...", text_color="#2ecc71")
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.entry_url.configure(state="disabled")
        self.entry_amount.configure(state="disabled")
        self.speed_menu.configure(state="disabled")

        self.iteration_count = 0
        self.iteration_label.configure(text="0")

        self.is_running = True

        
        if self.current_tab == "itch":
            bot = self.itch_bot
            method_name = "play_game_cycle"
        else:
            bot = self.tiktok_bot
            method_name = "watch_video_cycle"

        self.bot_thread = threading.Thread(
            target=self.bot_loop,
            args=(bot, method_name, target_url, max_iterations, session_duration, delay),
            daemon=True
        )
        self.bot_thread.start()

    def stop_bot(self):
        self.label_status.configure(text="Остановка...", text_color="#f39c12")
        self.btn_stop.configure(state="disabled")
        self.is_running = False

    def reset_ui_state(self):
        self.btn_start.configure(state="normal")
        self.entry_url.configure(state="normal")
        self.entry_amount.configure(state="normal")
        self.speed_menu.configure(state="normal")
        self.label_status.configure(text="Готов к работе", text_color="#3498db")


if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
