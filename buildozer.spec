[app]
title = FB TikTok Downloader
package.name = fbtiktokdownloader
package.domain = org.myapp
source.dir = .
source.include_exts = py
version = 1.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,yt-dlp
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.arch = arm64-v8a,armeabi-v7a
