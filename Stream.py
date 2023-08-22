import os
import re
from flask import Flask,render_template, request, Blueprint, current_app, send_file

app = Flask(__name__)

# your request handles here with @core.route()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video", methods=["GET"])
def video():
    headers = request.headers
    if not "range" in headers:
        ##return current_app.response_class(status=400)
        pass

    video_path = os.path.abspath(os.path.join("media", "sample.mp4"))
    size = os.stat(video_path)
    size = size.st_size

    chunk_size = (10 ** 6) * 3 #1000kb makes 1mb * 3 = 3mb (this is based on your choice)
    ## we put if case
    ## because <video> tag in html
    ## didnt send range header in first request
    ## so we put the default value of range == 0
    if not "range" in headers:
        start = 0
    else:
        start = int(re.sub("\D", "", headers["range"]))
    end = min(start + chunk_size, size - 1)

    content_lenght = end - start + 1

    def get_chunk(video_path, start, chunk_size):
        with open(video_path, "rb") as f:
            f.seek(start)
            chunk = f.read(chunk_size)
        return chunk

    headers = {
        "Content-Range": f"bytes {start}-{end}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": content_lenght,
        "Content-Type": "video/mp4",
    }

    return current_app.response_class(get_chunk(video_path, start,chunk_size), 206, headers)


if __name__ == "__main__":
    app.run()





