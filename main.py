from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.progressbar import MDLinearProgressIndicator
from kivymd.uix.label import MDLabel
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
import yt_dlp
import threading

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: '📥 FB & TikTok Downloader'
            elevation: 10
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            MDLabel:
                text: '🔗 បិទភ្ជាប់តំណ៖'
                font_style: 'H6'
            MDTextField:
                id: url_field
                hint_text: 'https://facebook.com/... ឬ tiktok.com/...'
                multiline: False
                height: dp(55)
            MDBoxLayout:
                spacing: dp(15)
                MDRectangleFlatButton:
                    text: '📋 Paste'
                    on_release: app.paste_link()
                MDRaisedButton:
                    text: '⬇️ ទាញយក'
                    on_release: app.start_download()
            MDLinearProgressIndicator:
                id: progress
                value: 0
                height: dp(12)
            MDLabel:
                id: status
                text: 'រង់ចាំតំណ... បិទភ្ជាប់មក!'
                halign: 'center'
'''

class VideoDownloader(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def paste_link(self):
        link = Clipboard.paste().strip()
        if link.startswith("http"):
            self.root.ids.url_field.text = link
            self.root.ids.status.text = "✅ បាន Paste!"

    def start_download(self):
        url = self.root.ids.url_field.text.strip()
        if not url:
            self.root.ids.status.text = "❌ សូមបិទតំណមុន!"
            return
        self.root.ids.status.text = "កំពុងរៀបចំ..."
        self.root.ids.progress.value = 0
        threading.Thread(target=self._download, args=(url,), daemon=True).start()

    def _download(self, url):
        def hook(d):
            if d['status'] == 'downloading':
                try:
                    p = float(d['_percent_str'].replace('%',''))
                    Clock.schedule_once(lambda dt: self.update_ui(p))
                except: pass
            elif d['status'] == 'finished':
                Clock.schedule_once(lambda dt: self.finish(True))

        opts = {
            'outtmpl': '/sdcard/Download/%(title)s.%(ext)s',
            'format': 'best',
            'progress_hooks': [hook],
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as e:
            Clock.schedule_once(lambda dt: self.finish(False, str(e)[:80]))

    def update_ui(self, percent):
        self.root.ids.progress.value = percent
        self.root.ids.status.text = f'ទាញយក... {percent:.1f}%'

    def finish(self, success, error=None):
        if success:
            self.root.ids.status.text = '✅ រួចរាល់!\nពិនិត្យ folder "Download"'
            self.root.ids.progress.value = 100
        else:
            self.root.ids.status.text = f'❌ មានបញ្ហា: {error}'

if __name__ == '__main__':
    VideoDownloader().run()
