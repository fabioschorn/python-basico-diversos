from pathlib import Path
import yt_dlp

PASTA_DESTINO = Path("/Users/fabioschorn/Documents/Videos/Videos-Youtube")


def escolher_qualidade():
    print("\nEscolha a qualidade:")
    print("1 - Melhor qualidade disponível")
    print("2 - 1080p")
    print("3 - 720p")
    print("4 - 480p")
    print("5 - 360p")
    print("6 - Somente áudio MP3")

    opcao = input("Digite a opção desejada: ").strip()

    formatos = {
        "1": "bestvideo+bestaudio/best",
        "2": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "3": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "4": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "5": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "6": "bestaudio/best",
    }

    return opcao, formatos.get(opcao, "bestvideo+bestaudio/best")


def baixar_video(url: str):
    PASTA_DESTINO.mkdir(parents=True, exist_ok=True)

    opcao, formato = escolher_qualidade()

    opcoes = {
        "format": formato,
        "outtmpl": str(PASTA_DESTINO / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "restrictfilenames": True,
    }

    if opcao == "6":
        opcoes["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
    else:
        opcoes["merge_output_format"] = "mp4"

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])


def main():
    print("=== TubeSaver - Downloader de vídeos do YouTube ===")
    print(f"Pasta de destino: {PASTA_DESTINO}")

    url = input("\nCole a URL do vídeo do YouTube: ").strip()

    if not url:
        print("Nenhuma URL informada.")
        return

    try:
        baixar_video(url)
        print("\nDownload concluído com sucesso.")
    except Exception as erro:
        print(f"\nErro ao baixar o vídeo: {erro}")


if __name__ == "__main__":
    main()
