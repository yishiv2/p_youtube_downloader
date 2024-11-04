from tkinter import ttk, filedialog, StringVar, Label, Entry, Button, Radiobutton, Tk, mainloop
from yt_dlp import YoutubeDL
import re

class Application:
    def __init__(self, root):
        self.root = root
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.config(bg="#ffdddd")

        # タイトルラベル
        top_label = Label(self.root, text="Youtube-downloader", fg="orange", font=('Type Xero', 70))
        top_label.grid(pady=(0, 10))

        # リンク入力用ラベルとエントリ
        link_label = Label(self.root, text="YouTubeのリンクを添付してください", font=('SnowPersons', 30))
        link_label.grid(pady=(0, 20))
        self.youtubeEntryVar = StringVar()
        self.youtubeEntry = Entry(self.root, width=70, textvariable=self.youtubeEntryVar, font=("Agency Fb", 25))
        self.youtubeEntry.grid(pady=(0, 15), ipady=2)

        # エラーメッセージラベル
        self.youtubeEntryError = Label(self.root, text="", font=("Concert One", 20))
        self.youtubeEntryError.grid(pady=(0.8), ipady=2)

        # 保存先ディレクトリ選択
        self.youtubeFileSaveLabel = Label(self.root, text="保存先を選択", font=("Concert One", 30))
        self.youtubeFileSaveLabel.grid()
        self.youtubeFileDirectoryButton = Button(self.root, text="Directory", font=("Bell MT", 15), command=self.openDirectory)
        self.youtubeFileDirectoryButton.grid(pady=(10, 3))
        self.fileLocationLabel = Label(self.root, text="", font=("Freestyle Script", 25))
        self.fileLocationLabel.grid()

        # ダウンロード形式選択
        self.youtubeChooselabel = Label(self.root, text="ダウンロード形式", font=(30))
        self.youtubeChooselabel.grid()
        self.downloadChoices = [("Audio mp3", 1), ("Video webm", 2)]
        self.ChoicesVar = StringVar()
        self.ChoicesVar.set(1)
        for text, mode in self.downloadChoices:
            self.youtubeChoices = Radiobutton(self.root, text=text, font=("Northwest old", 15), variable=self.ChoicesVar, value=mode)
            self.youtubeChoices.grid()

        # ダウンロードボタン
        self.downloadButton = Button(self.root, text="Download", width=10, font=("Bell MT", 15), command=self.checkYouTubeLink)
        self.downloadButton.grid(pady=(30, 5))

    def checkYouTubeLink(self):
        youtube_url = self.youtubeEntryVar.get()
        if not re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+', youtube_url):
            self.youtubeEntryError.config(text="無効なYouTubeリンクです", fg="red")
            return

        if not self.fileLocationLabel.cget("text"):
            self.youtubeEntryError.config(text="保存先ディレクトリを選択してください", fg="red")
            return

        self.youtubeEntryError.config(text="リンクとディレクトリは有効です。ダウンロードを開始します...", fg="green")
        self.startDownload(youtube_url)

    def openDirectory(self):
        self.FolderName = filedialog.askdirectory()
        if self.FolderName:
            self.fileLocationLabel.config(text=self.FolderName, fg="green")
        else:
            self.fileLocationLabel.config(text="ディレクトリを選択してください", fg="red")

    def startDownload(self, youtube_url):
        ydl_opts = {
            'format': 'bestaudio/best' if self.ChoicesVar.get() == '1' else 'bestvideo+bestaudio',
            'outtmpl': f"{self.FolderName}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if self.ChoicesVar.get() == '1' else []
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            self.youtubeEntryError.config(text="ダウンロードが完了しました！", fg="green")
        except Exception as e:
            self.youtubeEntryError.config(text="ダウンロード中にエラーが発生しました。", fg="red")
            print("Error:", e)

if __name__ == "__main__":
    window = Tk()
    window.title("YouTube Downloader")
    window.state("zoomed")
    app = Application(window)
    mainloop()
