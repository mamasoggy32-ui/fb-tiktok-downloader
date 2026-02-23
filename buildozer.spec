name: Build APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install system dependencies
        run: |
          sudo apt-get update -y
          sudo apt-get install -y git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev openjdk-17-jdk wget unzip

      - name: Install Android command-line-tools
        run: |
          mkdir -p \~/android/cmdline-tools
          cd \~/android/cmdline-tools
          wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
          unzip commandlinetools-linux-11076708_latest.zip
          mv cmdline-tools latest
          mkdir tools
          mv latest tools/
          echo 'export ANDROID_HOME=\~/android' >> \~/.bashrc
          echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/tools/bin' >> \~/.bashrc
          source \~/.bashrc
          yes | sdkmanager --licenses
          sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

      - name: Install Buildozer & dependencies
        run: |
          python -m pip install --upgrade pip
          pip install --upgrade cython==0.29.33 virtualenv buildozer

      - name: Build APK
        run: buildozer -v android debug

      - name: Upload APK artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: APK
          path: bin/*.apk
          if-no-files-found: warn
