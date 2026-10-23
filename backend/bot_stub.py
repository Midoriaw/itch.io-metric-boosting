import sys
import os
import time
import random
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent


def send_log(message):
    print(json.dumps({"type": "log", "message": str(message)}), flush=True)


class AdvancedStealthEngine:
    """Ультимативный движок маскировки железа, отпечатков и сетевого окружения"""

    @staticmethod
    def get_user_agent():
        windows_versions = ["10.0; Win64; x64", "11.0; Win64; x64"]
        chrome_versions = [
            f"130.0.0.{random.randint(100, 999)}",
            f"131.0.0.{random.randint(100, 999)}",
            f"132.0.0.{random.randint(100, 999)}"
        ]
        return f"Mozilla/5.0 (Windows NT {random.choice(windows_versions)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"

    @staticmethod
    def inject(context):
        gpu_drivers = [
            "ANGLE (NVIDIA GeForce RTX 4060 Laptop GPU Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel(R) UHD Graphics 770 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD Radeon RX 6600 Direct3D11 vs_5_0 ps_5_0)"
        ]

        renderer = random.choice(gpu_drivers)
        vendor = "Google Inc. (NVIDIA)" if "NVIDIA" in renderer else "Google Inc. (AMD)" if "AMD" in renderer else "Google Inc. (Intel)"

        chosen_cores = random.choice([4, 6, 8, 12, 16])
        chosen_memory = random.choice([8, 16, 32])
        screen_w = random.choice([1920, 1440, 1536])
        screen_h = random.choice([1080, 900, 864])

        context.add_init_script(f"""
            Object.defineProperty(navigator, 'webdriver', {{ get: () => undefined }});
            Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: () => {chosen_cores} }});
            Object.defineProperty(navigator, 'deviceMemory', {{ get: () => {chosen_memory} }});
            Object.defineProperty(navigator, 'languages', {{ get: () => ['ru-RU', 'ru', 'en-US', 'en'] }});

            const mockWebGL = (proto) => {{
                const getParameter = proto.getParameter;
                proto.getParameter = function(parameter) {{
                    if (parameter === 37445) return '{vendor}';
                    if (parameter === 37446) return '{renderer}';
                    return getParameter.apply(this, arguments);
                }};
            }};
            if (window.WebGLRenderingContext) mockWebGL(WebGLRenderingContext.prototype);
            if (window.WebGL2RenderingContext) mockWebGL(WebGL2RenderingContext.prototype);

            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function(x, y, w, h) {{
                const imageData = originalGetImageData.apply(this, arguments);
                const data = imageData.data;
                for (let i = 0; i < data.length; i += 4) {{
                    if (Math.random() > 0.98) {{ data[i] = data[i] ^ 1; }}
                }}
                return imageData;
            }};
        """)
        return {"width": screen_w, "height": screen_h}


class HumanBehaviorSimulator:
    """Генератор органических человеческих движений и траекторий мыши"""

    @staticmethod
    def move_mouse_bezier(page, from_x, from_y, to_x, to_y, steps=25):
        cx1 = from_x + (to_x - from_x) * random.uniform(0.1, 0.4)
        cy1 = from_y + (to_y - from_y) * random.uniform(0.1, 0.3)
        cx2 = from_x + (to_x - from_x) * random.uniform(0.6, 0.9)
        cy2 = from_y + (to_y - from_y) * random.uniform(0.7, 0.9)

        for i in range(steps + 1):
            t = i / steps
            x = (1 - t) ** 3 * from_x + 3 * (1 - t) ** 2 * t * cx1 + 3 * (1 - t) * t ** 2 * cx2 + t ** 3 * to_x
            y = (1 - t) ** 3 * from_y + 3 * (1 - t) ** 2 * t * cy1 + 3 * (1 - t) * t ** 2 * cy2 + t ** 3 * to_y
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.005, 0.015))


class ItchHumanBooster:
    def __init__(self, controller):
        self.controller = controller

    def _parse_url_details(self, url):
        try:
            clean = url.split("://")[-1].split("?")[0].strip("/")
            if ".itch.io" in clean:
                parts = clean.split(".itch.io/")
                return parts[0], parts[1]
        except Exception:
            pass
        return "inheogames", "xenologist"

    def run_boost_session(self, target_url, speed_mode, proxy_config=None):
        author, game_slug = self._parse_url_details(target_url)
        search_query = game_slug.replace("-", " ")
        user_agent = AdvancedStealthEngine.get_user_agent()

        with sync_playwright() as p:
            launch_args = ["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-gpu-sandbox"]

            browser_kwargs = {"headless": False, "args": launch_args}
            if proxy_config and isinstance(proxy_config, dict) and proxy_config.get("server"):
                browser_kwargs["proxy"] = proxy_config

            browser = p.chromium.launch(**browser_kwargs)

            context = browser.new_context(
                user_agent=user_agent,
                locale=random.choice(["ru-RU", "en-US", "en-GB"]),
                timezone_id=random.choice(["Europe/Moscow", "Europe/London", "America/New_York"])
            )

            screen_res = AdvancedStealthEngine.inject(context)
            page = context.new_page()
            page.set_viewport_size(screen_res)

            try:
                # --- ШАГ 1: ЧЕЛОВЕЧЕСКИЙ ПОИСК ---
                send_log("🛸 ПРОТОКОЛ: Выхожу на главную страницу itch.io...")
                page.goto("https://itch.io", wait_until="domcontentloaded", timeout=40000)
                time.sleep(random.uniform(2.0, 4.0))

                search_input = page.locator('input[type="text"][name="q"], input.search_input').first
                search_input.wait_for(state="visible", timeout=15000)

                s_box = search_input.bounding_box()
                if s_box:
                    HumanBehaviorSimulator.move_mouse_bezier(
                        page, screen_res["width"] / 2, screen_res["height"] / 2,
                              s_box["x"] + s_box["width"] / 2, s_box["y"] + s_box["height"] / 2
                    )
                search_input.click()
                time.sleep(0.5)

                for char in search_query:
                    search_input.type(char, delay=random.randint(60, 130))
                time.sleep(random.uniform(0.4, 0.8))
                page.keyboard.press("Enter")

                send_log(f"🔎 СЕО: Запрос '{search_query}' отправлен. Анализирую поисковую выдачу...")
                time.sleep(random.uniform(4.0, 6.0))

                target_card = page.locator(f'a[href*="{author}.itch.io/{game_slug}"]').first
                if target_card.is_visible():
                    box = target_card.bounding_box()
                    if box:
                        target_x = box["x"] + box["width"] / 2
                        target_y = box["y"] + box["height"] / 2
                        HumanBehaviorSimulator.move_mouse_bezier(page, 100, 100, target_x, target_y, steps=30)
                        time.sleep(0.2)
                        page.mouse.click(target_x, target_y)
                    send_log("🎯 ПОИСК: Целевой проект успешно обнаружен! Совершаю переход...")
                    page.wait_for_load_state("domcontentloaded", timeout=25000)
                else:
                    send_log("⚠️ СЕО: Выдача пуста или заблокирована. Захожу по прямому URL для удержания трафика...")
                    page.goto(f"https://{author}.itch.io/{game_slug}", wait_until="domcontentloaded", timeout=30000)

                # --- ШАГ 2: ИМИТАЦИЯ ЧТЕНИЯ И СКРОЛЛИНГА ---
                time.sleep(random.uniform(3.0, 5.0))
                for _ in range(random.randint(2, 4)):
                    scroll_amount = random.randint(200, 450)
                    page.evaluate(f"window.scrollBy({{top: {scroll_amount}, behavior: 'smooth'}})")
                    time.sleep(random.uniform(1.5, 3.5))

                # --- ШАГ 3: ПРОСМОТР ТРЕЙЛЕРА ---
                video_iframe = page.locator("iframe[src*='youtube'], .video_embed, .embed_wrapper").first
                if video_iframe.is_visible():
                    video_iframe.scroll_into_view_if_needed()
                    time.sleep(1.5)
                    v_box = video_iframe.bounding_box()
                    if v_box:
                        page.mouse.click(v_box["x"] + v_box["width"] / 2, v_box["y"] + v_box["height"] / 2)
                        watch_time = random.randint(12, 22)
                        send_log(f"🎬 МЕДИА: Имитирую вовлеченный просмотр медиаконтента ({watch_time} сек)...")
                        time.sleep(watch_time)

                # --- ШАГ 4: ГАЛЕРЕЯ СКРИНШОТОВ ---
                screenshot_img = page.locator(".screenshot_list a, .game_screenshots img").first
                if screenshot_img.is_visible():
                    screenshot_img.scroll_into_view_if_needed()
                    time.sleep(random.uniform(1.0, 2.0))
                    box = screenshot_img.bounding_box()
                    if box:
                        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        send_log("📸 ГАЛЕРЕЯ: Изучаю скриншоты проекта...")
                        for _ in range(random.randint(2, 4)):
                            time.sleep(random.uniform(2.0, 3.5))
                            page.keyboard.press("ArrowRight")
                        time.sleep(1.0)
                        page.keyboard.press("Escape")

                # --- ШАГ 5: ФИНАЛЬНОЕ ЦЕЛЕВОЕ ДЕЙСТВИЕ (DOWNLOAD) ---
                action_btn = page.locator(
                    ".buy_row a.button, .load_iframe_btn, .download_btn, button.load_game_btn"
                ).first
                if action_btn.is_visible():
                    action_btn.scroll_into_view_if_needed()
                    time.sleep(random.uniform(2.5, 4.5))
                    box = action_btn.bounding_box()
                    if box:
                        HumanBehaviorSimulator.move_mouse_bezier(
                            page, screen_res["width"] / 2, screen_res["height"] / 2,
                                  box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=20
                        )
                        time.sleep(0.3)
                        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        send_log("✦ ТОП_БУСТ: Конверсионный триггер (Download/Play) успешно зафиксирован площадкой!")
                        time.sleep(random.uniform(4.0, 6.0))

                        skip_price = page.locator(
                            'a.lightbox_close_btn, .checkout_lightbox a, text="No thanks, just take me to the downloads"'
                        ).first
                        if skip_price.is_visible():
                            skip_price.scroll_into_view_if_needed()
                            time.sleep(0.5)
                            skip_price.click()
                            time.sleep(2)

                send_log("✓ СИСТЕМА: Сессия органического визита закрыта без подозрений.")
                return True

            except Exception as e:
                send_log(f"❌ ОШИБКА АВТОМАЦИИ: {str(e)}")
                sys.stdout.flush()
                return False
            finally:
                context.close()
                browser.close()


class MainController:
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.proxies_pool = []

    def start_bot(self, platform, url, count, speed):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._worker, args=(platform, url, int(count), speed), daemon=True)
        self.thread.start()

    def stop_bot(self):
        self.is_running = False

    def _worker(self, platform, url, count, speed):
        send_log(f">>>> УЛЬТИМАТИВНЫЙ ОРГАНИЧЕСКИЙ ПРОТОКОЛ АКТИВИРОВАН. ЦЕЛЬ: {count} КРУГОВ <<<<")
        booster = ItchHumanBooster(self)
        successful_cycles = 0

        while successful_cycles < count and self.is_running:
            send_log(f"[ПОТОК] Сборка цифрового следа и запуск сессии #{successful_cycles + 1}")
            current_proxy = random.choice(self.proxies_pool) if self.proxies_pool else None
            success = booster.run_boost_session(url, speed, proxy_config=current_proxy)

            if success:
                successful_cycles += 1

            if not self.is_running:
                break

            pause = random.randint(15, 45) if speed == "Normal" else random.randint(5, 12)
            send_log(f"⏳ ТАЙМАУТ: Ожидание следующего игрока ({pause} сек)...")
            time.sleep(pause)

        self.is_running = False
        send_log(">>> ПРОТОКОЛ УСПЕШНО ЗАВЕРШЕН. СИСТЕМА В РЕЖИМЕ READY_TO_RUN <<<")


if __name__ == "__main__":
    controller = MainController()
    for line in sys.stdin:
        try:
            data = json.loads(line.strip())
            if data.get("cmd") == "start":
                url = data.get("url") or data.get("target") or data.get("TARGET") or ""
                count = data.get("CYCLES") or data.get("cycles") or data.get("count") or 5
                speed = data.get("SPEED") or data.get("speed") or "Normal"

                if "proxies" in data:
                    controller.proxies_pool = data["proxies"]

                controller.start_bot("itch", url, count, speed)
            elif data.get("cmd") == "stop":
                controller.stop_bot()
        except json.JSONDecodeError:
            pass
        except Exception as e:
            send_log(f"❌ ОШИБКА КОНТРОЛЛЕРА: {str(e)}")