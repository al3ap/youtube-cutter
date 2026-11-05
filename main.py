from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import subprocess
import uuid
import os

app = FastAPI()

# السماح لصفحة بلوجر بالاتصال بالسيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/cut")
def cut_video(url: str, start: str, end: str):
    try:
        output_filename = f"cut_{uuid.uuid4().hex[:8]}.mp4"
        
        # أمر yt-dlp لقص الفيديو بدون تحميله كاملاً
        cmd = [
            "yt-dlp",
            "--download-sections", f"*{start}-{end}",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", output_filename,
            url
        ]
        
        subprocess.run(cmd, check=True)
        
        return FileResponse(
            path=output_filename,
            filename="clipped_video.mp4",
            media_type="video/mp4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))