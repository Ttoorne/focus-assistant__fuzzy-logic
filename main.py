import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QStackedWidget, QSlider, QDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QMovie, QFontDatabase
from fuzzy_logic import analyze_focus



class WelcomeScreen(QWidget):
    def __init__(self, switch_function):
        super().__init__()
        self.switch_function = switch_function
        self.load_fonts()
        self.init_ui()

    def load_fonts(self):
        font_id_bold = QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")
        font_id_regular = QFontDatabase.addApplicationFont("fonts/Montserrat-Regular.ttf")
        font_id_medium = QFontDatabase.addApplicationFont("fonts/Montserrat-Medium.ttf")

        self.montserrat_bold_family = QFontDatabase.applicationFontFamilies(font_id_bold)[0] if font_id_bold != -1 else "Montserrat"
        self.montserrat_regular_family = QFontDatabase.applicationFontFamilies(font_id_regular)[0] if font_id_regular != -1 else "Montserrat"
        self.montserrat_medium_family = QFontDatabase.applicationFontFamilies(font_id_medium)[0] if font_id_medium != -1 else "Montserrat"

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 10, 25, 40)  
        layout.setSpacing(10)  

        image = QLabel()
        movie = QMovie("images/welcome.gif")  
        movie.setScaledSize(QtCore.QSize(320, 320))  
        image.setMovie(movie)
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        movie.start()

    
        label = QLabel("Odak analiz sistemine\n hoş geldiniz!")
        label.setFont(QFont(self.montserrat_bold_family, 20, QFont.Weight.DemiBold))
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #333333;")

        description = QLabel("Size uygun müziği seçmenize ve mola zamanını hatırlatmamıza\n yardımcı olacağız.\n Sadece 5 soruyu yanıtlayın.")
        description.setFont(QFont(self.montserrat_regular_family, 14))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("color: #333333;")

        btn_start = QPushButton("Başla")
        btn_start.setFont(QFont(self.montserrat_medium_family, 14, QFont.Weight.Medium))
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #546A7B;
                color: white;
                padding: 12px 24px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        btn_start.clicked.connect(self.switch_function)

        layout.addStretch(1)  
        layout.addWidget(image)
        layout.addSpacing(10)
        layout.addWidget(label)
        layout.addSpacing(5)
        layout.addWidget(description)
        layout.addStretch(2)  
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)  

        self.setLayout(layout)

class ParameterWindow(QWidget):
    def __init__(self, label_text, min_val, max_val, color, next_callback, unit="",gif_path=None, info_text=None):
        super().__init__()
        self.value = (max_val + min_val) // 2
        self.load_fonts()
        self.next_callback = next_callback
        self.info_text = info_text or "Açıklama yok"

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 40)
        layout.setSpacing(15)

        if gif_path:
            gif_label = QLabel()
            movie = QMovie(gif_path)
            movie.setScaledSize(QtCore.QSize(340, 340))
            gif_label.setMovie(movie)
            gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            movie.start()
            layout.addWidget(gif_label)

        title_layout = QHBoxLayout()
        title_label = QLabel(label_text)
        title_label.setFont(QFont(self.montserrat_medium_family, 17, QFont.Weight.Medium))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_layout.addStretch()
        title_layout.addWidget(title_label)

        if info_text:
            info_button = QPushButton("?")
            info_button.setFont(QFont(self.montserrat_bold_family, 15))
            info_button.setFixedSize(27, 27)
            info_button.setCursor(Qt.CursorShape.PointingHandCursor)
            info_button.setStyleSheet("""
            QPushButton {
                background-color: #90CAF9;
                color: white;
                border-radius: 12px;
                padding: 2px;            
            }
            QPushButton:hover {
                background-color: #64B5F6;
            }
        """)
            info_button.clicked.connect(self.show_info_popup)
            title_layout.addWidget(info_button)

        title_layout.addStretch()
        layout.addLayout(title_layout)


        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setValue(self.value)
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)
        if label_text.startswith("Günün Saati"):
            self.slider.setStyleSheet("""
    QSlider::groove:horizontal {
        height: 10px;
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #9575CD,
            stop: 0.5 #B39DDB,
            stop: 1 #D1C4E9
        );
        border-radius: 5px;
        margin: 0 14px;
    }

    QSlider::handle:horizontal {
        background: qradialgradient(
            cx:0.5, cy:0.5, radius: 0.8,
            fx:0.5, fy:0.5,
            stop:0 white,
            stop:1 #7E57C2
        );
        border: 2px solid #673AB7;
        width: 20px;
        height: 20px;
        margin: -6px 0;
        border-radius: 10px;
    }

    QSlider::handle:horizontal:hover {
        background: #EDE7F6;
        border: 2px solid #9575CD;
    }
    """)


        else:
            self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 10px;
                background: {color};
                border-radius: 5px;
                margin: 0 12px;
            }}
            QSlider::handle:horizontal {{
                background: white;
                border: 3px solid #607D8B;
                width: 20px;
                height: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }}
            """)


        self.slider.valueChanged.connect(self.update_label)

        self.value_label = QLabel(f"{self.value} {unit}")
        self.value_label.setFont(QFont(self.montserrat_regular_family, 14))
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        next_button = QPushButton("İleri >")
        next_button.setFont(QFont(self.montserrat_medium_family, 13, QFont.Weight.Medium))
        next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        next_button.setStyleSheet("""
            QPushButton {
                background-color: #546A7B;
                color: white;
                padding: 12px 24px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        next_button.clicked.connect(self.go_next)

        layout.addStretch()
        layout.addWidget(title_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.value_label)
        layout.addSpacing(30)
        layout.addWidget(next_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def load_fonts(self):
        font_id_bold = QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")
        font_id_regular = QFontDatabase.addApplicationFont("fonts/Montserrat-Regular.ttf")
        font_id_medium = QFontDatabase.addApplicationFont("fonts/Montserrat-Medium.ttf")
        font_id_semibold = QFontDatabase.addApplicationFont("fonts/Montserrat-SemiBold.ttf")


        self.montserrat_bold_family = QFontDatabase.applicationFontFamilies(font_id_bold)[0] if font_id_bold != -1 else "Montserrat"
        self.montserrat_regular_family = QFontDatabase.applicationFontFamilies(font_id_regular)[0] if font_id_regular != -1 else "Montserrat"
        self.montserrat_medium_family = QFontDatabase.applicationFontFamilies(font_id_medium)[0] if font_id_medium != -1 else "Montserrat"
        self.montserrat_semibold_family = QFontDatabase.applicationFontFamilies(font_id_semibold)[0] if font_id_semibold != -1 else "Montserrat"


    def show_info_popup(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("İpucu")
        dialog.setFixedSize(500, 370)

        layout = QVBoxLayout()
        label = QLabel(self.info_text)
        label.setWordWrap(True)
        label.setFont(QFont(self.montserrat_regular_family, 14))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        close_btn = QPushButton("Anladım")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(""" QPushButton {
                border: none;
                font-weight: bold;
                font-size: 16px;
                }
            QPushButton:hover {
                text-decoration: underline; 
                }""")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        screen = QApplication.primaryScreen().availableGeometry()
        center_x = screen.center().x()
        center_y = screen.center().y() - 20
        dialog.move(center_x - dialog.width() // 2, center_y - dialog.height() // 2)


        dialog.setLayout(layout)
        dialog.exec()



    def update_label(self, val):
        self.value = val
        self.value_label.setText(str(val))

    def go_next(self):
        self.next_callback(self.value)

class ResultScreen(QWidget):
    def load_fonts(self):
        font_id_bold = QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")
        font_id_regular = QFontDatabase.addApplicationFont("fonts/Montserrat-Regular.ttf")
        font_id_medium = QFontDatabase.addApplicationFont("fonts/Montserrat-Medium.ttf")
        font_id_semibold = QFontDatabase.addApplicationFont("fonts/Montserrat-SemiBold.ttf")

        self.montserrat_bold_family = QFontDatabase.applicationFontFamilies(font_id_bold)[0] if font_id_bold != -1 else "Montserrat"
        self.montserrat_regular_family = QFontDatabase.applicationFontFamilies(font_id_regular)[0] if font_id_regular != -1 else "Montserrat"
        self.montserrat_medium_family = QFontDatabase.applicationFontFamilies(font_id_medium)[0] if font_id_medium != -1 else "Montserrat"
        self.montserrat_semibold_family = QFontDatabase.applicationFontFamilies(font_id_semibold)[0] if font_id_semibold != -1 else "Montserrat"

    def __init__(self, music_result, pause_result, restart_callback):
        super().__init__()
        self.load_fonts()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 20, 25, 40)
        main_layout.setSpacing(20)

        title_label = QLabel("Analiz Sonuçları")
        title_label.setFont(QFont(self.montserrat_bold_family, 22, QFont.Weight.DemiBold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        images_row = QHBoxLayout()
        images_row.setSpacing(30)

        self.music_gif_label = QLabel()
        self.music_gif_label.setFixedSize(200, 200)
        self.set_music_gif(music_result[0])
        images_row.addWidget(self.music_gif_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.pause_gif_label = QLabel()
        self.pause_gif_label.setFixedSize(200, 200)
        self.set_pause_gif(pause_result[0])
        images_row.addWidget(self.pause_gif_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(images_row)

        titles_row = QHBoxLayout()
        titles_row.setSpacing(30)

        music_title = QLabel(f"{music_result[0].capitalize()}")
        music_title.setFont(QFont(self.montserrat_medium_family, 16, QFont.Weight.Medium))
        music_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titles_row.addWidget(music_title)

        pause_title = QLabel(f"{pause_result[0].capitalize()}")
        pause_title.setFont(QFont(self.montserrat_medium_family, 16, QFont.Weight.Medium))
        pause_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titles_row.addWidget(pause_title)

        main_layout.addLayout(titles_row)

        descriptions_row = QHBoxLayout()
        descriptions_row.setSpacing(30)

        music_desc = QLabel(music_result[1])
        music_desc.setFont(QFont(self.montserrat_medium_family, 13 ))
        music_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        music_desc.setWordWrap(True)
        descriptions_row.addWidget(music_desc)

        pause_desc = QLabel(pause_result[1])
        pause_desc.setFont(QFont(self.montserrat_medium_family, 13))
        pause_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pause_desc.setWordWrap(True)
        descriptions_row.addWidget(pause_desc)

        main_layout.addLayout(descriptions_row)

        restart_button = QPushButton("Yeniden Başla")
        restart_button.setFont(QFont(self.montserrat_medium_family, 13, QFont.Weight.Medium))
        restart_button.setCursor(Qt.CursorShape.PointingHandCursor)
        restart_button.setStyleSheet("""
        QPushButton {
            background-color: #546A7B;
            color: white;
            padding: 12px 24px;
            border-radius: 20px;
            border: none;
        }
        QPushButton:hover {
            background-color: #333333;
        }
    """)
        restart_button.clicked.connect(restart_callback)

        main_layout.addSpacing(30)
        main_layout.addWidget(restart_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)


    def set_music_gif(self, music_text):
        gif_map = {
            "sessizlik": "images/silence.gif",
            "yumuşak müzik": "images/soft_music.gif",
            "beyaz gürültü": "images/white_noise.gif",
        }
        path = gif_map.get(music_text, None)
        if path:
            movie = QMovie(path)
            movie.setScaledSize(self.music_gif_label.size())
            self.music_gif_label.setMovie(movie)
            movie.start()
        else:
            self.music_gif_label.clear()

    def set_pause_gif(self, pause_text):
        gif_map = {
            "devam edebilirsiniz": "images/continue.gif",
            "mola yakında": "images/soon_break.gif",
            "dinlenme zamanı": "images/rest.gif",
        }
        path = gif_map.get(pause_text, None)
        if path:
            movie = QMovie(path)
            movie.setScaledSize(self.pause_gif_label.size())
            self.pause_gif_label.setMovie(movie)
            movie.start()
        else:
            self.pause_gif_label.clear()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuzzy Focus App")
        self.setFixedSize(460, 650)

        self.center()
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.inputs = []

        self.stack.addWidget(WelcomeScreen(self.show_noise_screen))

    def center(self):
        screen = self.screen().availableGeometry()  
        size = self.geometry()  
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def show_noise_screen(self):
        info = (
            "\n"
            "Çevrenizdeki gürültü seviyesini tahmin etmeye çalışın:\n\n"
            "• 0–10: Neredeyse tam sessizlik\n"
            "• 11–40: Sessiz (ev, ofis)\n"
            "• 41–70: Orta (sokak, kafe)\n"
            "• 71–90: Gürültülü (yol, kalabalık)\n"
            "• 91–100: Çok gürültülü (inşaat, konser)\n"
        )
        screen = ParameterWindow("Gürültü Seviyesi (0–100)", 0, 100, "#90CAF9", self.collect_noise, gif_path="images/noise.gif", info_text=info)
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)


    def collect_noise(self, value):
        self.inputs.append(value)
        self.show_time_screen()

    def show_time_screen(self):
        info = (
            "\n"
            "Günün saatini belirtin:\n\n"
            "• 0–6: Gece\n"
            "• 7–11: Sabah\n"
            "• 12–17: Öğle / Öğleden sonra\n"
            "• 18–21: Akşam\n"
            "• 22–24: Gece geç saatler\n\n"
            "Biyolojik ritimler ve günün farklı saatleri, odaklanma ve üretkenlik üzerinde etkili olur.\n"
            "Kendinizi en yakın saate göre değerlendirin."
            "\n"

        )
        screen = ParameterWindow(
            "Günün Saati (0–24)", 0, 24, "#B39DDB", self.collect_time,
            unit="saat", gif_path="images/time-choose.gif", info_text=info
        )
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)


    def collect_time(self, value):
        self.inputs.append(value)
        self.show_session_screen()

    def show_session_screen(self):
        info = (
            "Oturum, çalışma veya ders için kesintisiz ayırdığınız süredir.\n"
            "Zamanı doğru kullanmak, yorgunluğu azaltır ve odaklanmayı artırır.\n\n"
            "• 15–30 dk: Yeni başlayanlar veya zor görevler için ideal.\n"
            "• 30–60 dk: Çoğu kullanıcı için en verimli süredir.\n"
            "• 60+ dk: Deneyimliler için uygundur, molalar gerektirir.\n\n"
            "Her oturum sonrası 5–10 dakikalık mola vermeyi unutmayın."
            "\n"

        )
        screen = ParameterWindow(
            "Oturum Süresi (dk)",
            0, 180,
            "#FAB784",
            self.collect_session,
            unit="dk",
            gif_path="images/work_in_progress.gif",
            info_text=info
        )
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)

    def collect_session(self, value):
        self.inputs.append(value)
        self.show_distraction_screen()

    def show_distraction_screen(self):
        info = (
            "Dikkat dağınıklığı seviyesi, çalışma sırasında odaklanma düzeyinizi gösterir.\n"
            "• 0 — Tam konsantrasyon, dikkat dağılmadı.\n"
            "• 1–3 — Küçük dikkat dağınıklıkları, hızlıca göreve döndünüz.\n"
            "• 4–6 — Zaman zaman dikkat dağıldı, odaklanmak zor oldu.\n"
            "• 7–9 — Sık sık dikkat dağıldı, verimli çalışma zorlaştı.\n"
            "• 10 — Neredeyse hiç odaklanamadınız.\n"
            "Dikkat seviyesini düzenli ölçmek, verimliliğinizi etkileyen faktörleri anlamanızı\n"
            "ve daha iyi odaklanma yöntemleri geliştirmenizi sağlar."
        )

        screen = ParameterWindow("Dikkat Dağınıklığı\n Seviyesi (0–10)", 0, 10, "#FFE066", self.collect_distractions, gif_path="images/distraction.gif", info_text=info)
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)

    def collect_distractions(self, value):
        self.inputs.append(value)
        self.show_mood_screen()

    def show_mood_screen(self):
        info = (
            "Mod, çalışma sırasında duygusal durumunuzu yansıtır.\n"
            "• 0 — Çok kötü mod, odaklanmak zor.\n"
            "• 1–3 — Orta altı mod, yorgunluk veya sinirlilik olabilir.\n"
            "• 4–6 — Orta mod, çalışma motivasyonu dengeli.\n"
            "• 7–9 — İyi mod, yüksek motivasyon ve enerji.\n"
            "• 10 — Mükemmel mod, tam performans ve verimlilik.\n"
            "Modunuzu düzenli değerlendirmek, duyguların verimliliğinizi nasıl etkilediğini anlamanıza yardımcı olur."
        )
        screen = ParameterWindow("Mod (0-10)", 0, 10, "#A5D6A7", self.collect_mood, gif_path="images/mood.gif", info_text=info)
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)

    def collect_mood(self, value):
        self.inputs.append(value)
        noise, time_val, session, distractions, mood = self.inputs
        music, pause = analyze_focus(noise, time_val, session, distractions, mood)
        result_screen = ResultScreen(music, pause, self.restart)
        self.stack.addWidget(result_screen)
        self.stack.setCurrentWidget(result_screen)
    
    def restart(self):
        self.inputs = []
        self.stack.setCurrentIndex(0)  


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font_ids = {
        "regular": QFontDatabase.addApplicationFont("fonts/Montserrat-Regular.ttf"),
        "medium": QFontDatabase.addApplicationFont("fonts/Montserrat-Medium.ttf"),
        "semibold": QFontDatabase.addApplicationFont("fonts/Montserrat-SemiBold.ttf"),
        "bold": QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf"),
    }

    montserrat_families = {}

    for weight, font_id in font_ids.items():
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                montserrat_families[weight] = families[0]

    if "regular" in montserrat_families:
        app.setFont(QFont(montserrat_families["regular"]))

    app.setStyleSheet("""
        QWidget {
            background-color: #FFF9F0;
            color: #333333;
            font-family: 'Montserrat', sans-serif;
        }
        QLabel {
            color: #333333;
        }
    """)

    window = MainApp()
    window.show()
    sys.exit(app.exec())
