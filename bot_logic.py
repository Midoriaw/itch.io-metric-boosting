import time
import os
import random
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ItchBot:
    def __init__(self, log_func):
        self.log = log_func

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        return webdriver.Chrome(options=options)

    def play_game_cycle(self, game_url, session_duration=3):
        driver = self.setup_driver()
        wait = WebDriverWait(driver, 15)

        try:
            self.log(f"Открываем страницу: {game_url}")
            driver.get(game_url)

            try:
                run_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.load_iframe_btn")))
                run_btn.click()
                self.log("Клик по кнопке 'Run game' выполнен успешно!")

                self.log(f"Имитируем игровую сессию ({session_duration} сек)...")
                time.sleep(session_duration)

            except Exception as e:
                self.log("Кнопка 'Run game' не найдена или страница долго грузилась.")

        except Exception as e:
            self.log(f"Ошибка в процессе работы: {e}")
        finally:
            self.log("Закрываем окно браузера.")
            driver.quit()


class TikTokBot:
    def __init__(self, log_func):
        self.log = log_func
        # Папка для сохранения профиля браузера (cookies, история)
        self.profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiktok_profile")
        os.makedirs(self.profile_dir, exist_ok=True)

    def setup_driver(self):
        options = uc.ChromeOptions()

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Твоё разрешение
        options.add_argument("--window-size=1440,1440")

        # User-Agent
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        )

        # ВАЖНО: сохраняем профиль браузера между запусками
        # Это делает поведение более "человечным" - TikTok видит "того же пользователя"
        options.add_argument(f"--user-data-dir={self.profile_dir}")

        driver = uc.Chrome(options=options, version_main=149)
        return driver

    def _human_like_mouse_move(self, driver):
        """Имитирует человеческое движение мыши"""
        try:
            actions = ActionChains(driver)
            # Случайные движения по странице
            for _ in range(random.randint(2, 5)):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset)
                time.sleep(random.uniform(0.1, 0.3))
            actions.perform()
        except:
            pass

    def _close_popups(self, driver):
        """Закрывает всплывающие окна TikTok"""
        popups_to_try = [
            (By.XPATH,
             "//button[contains(text(), 'Accept all') or contains(text(), 'Принять все') or contains(text(), 'Accept')]"),
            (By.CSS_SELECTOR, "[data-e2e='modal-close-inner-button']"),
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.CSS_SELECTOR, ".jsx-832288678"),
            (By.XPATH, "//button[contains(text(), 'Not now') or contains(text(), 'Не сейчас')]"),
        ]

        for by, selector in popups_to_try:
            try:
                elements = driver.find_elements(by, selector)
                for el in elements:
                    if el.is_displayed():
                        el.click()
                        self.log(f"Закрыт попап: {selector}")
                        time.sleep(0.5)
            except:
                pass

    def _check_if_video_playing(self, driver, video_element):
        """Проверяет, играет ли видео"""
        try:
            is_playing = driver.execute_script(
                "return arguments[0].paused === false && arguments[0].currentTime > 0;",
                video_element
            )
            return is_playing
        except:
            return False

    def watch_video_cycle(self, video_url, session_duration=5):
        driver = self.setup_driver()
        wait = WebDriverWait(driver, 20)

        try:
            self.log(f"Открываем TikTok видео: {video_url}")
            driver.get(video_url)

            # Даём странице загрузиться
            time.sleep(3)

            # Имитируем движение мыши
            self._human_like_mouse_move(driver)

            # Закрываем попапы
            self._close_popups(driver)
            time.sleep(1)
            self._close_popups(driver)

            try:
                # Ищем видео
                video_element = None

                # Способ 1: тег video
                try:
                    video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                except:
                    pass

                # Способ 2: через xgplayer
                if not video_element:
                    try:
                        video_element = driver.find_element(By.CSS_SELECTOR, "video.xg-video")
                    except:
                        pass

                # Способ 3: любой video
                if not video_element:
                    try:
                        videos = driver.find_elements(By.TAG_NAME, "video")
                        if videos:
                            video_element = videos[0]
                    except:
                        pass

                if video_element:
                    self.log("Видео найдено, запускаем просмотр...")

                    # Пытаемся запустить видео
                    try:
                        driver.execute_script("arguments[0].muted = true;", video_element)
                        driver.execute_script("arguments[0].volume = 0;", video_element)
                        driver.execute_script("arguments[0].play();", video_element)
                    except Exception as e:
                        self.log(f"Не удалось автозапустить: {e}")
                        # Кликаем по видео
                        try:
                            video_element.click()
                        except:
                            pass

                    # Проверяем, играет ли видео
                    time.sleep(2)
                    is_playing = self._check_if_video_playing(driver, video_element)

                    if not is_playing:
                        self.log("Видео не играет, пробуем запустить кликом...")
                        try:
                            video_element.click()
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].play();", video_element)
                            time.sleep(1)
                            is_playing = self._check_if_video_playing(driver, video_element)
                        except:
                            pass

                    if is_playing:
                        self.log("✓ Видео играет")
                    else:
                        self.log("✗ Видео не играет (возможна блокировка)")

                    # "Смотрим" видео
                    self.log(f"Просмотр видео ({session_duration} сек)...")

                    elapsed = 0
                    while elapsed < session_duration:
                        time.sleep(1)
                        elapsed += 1

                        # Имитация активности каждые 2-3 секунды
                        if elapsed % random.randint(2, 3) == 0:
                            self._human_like_mouse_move(driver)
                            try:
                                scroll_amount = random.randint(-30, 30)
                                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                            except:
                                pass

                        # Периодически закрываем попапы
                        if elapsed % 4 == 0:
                            self._close_popups(driver)

                        # Проверяем, продолжает ли видео играть
                        if elapsed % 3 == 0:
                            if not self._check_if_video_playing(driver, video_element):
                                self.log("Видео остановилось, пробуем перезапустить...")
                                try:
                                    driver.execute_script("arguments[0].play();", video_element)
                                except:
                                    pass

                    self.log("Просмотр завершен")
                else:
                    self.log("Видео не найдено, возможно капча или блокировка")
                    time.sleep(session_duration)

            except Exception as e:
                self.log(f"Ошибка при просмотре: {e}")
                time.sleep(session_duration)

        except Exception as e:
            self.log(f"Ошибка при работе с TikTok: {e}")
        finally:
            try:
                driver.quit()
                self.log("Браузер закрыт")
            except:
                pass