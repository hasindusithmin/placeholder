import re
import textwrap
from io import BytesIO
from typing import Optional
from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw,ImageColor,ImageFont
app = FastAPI(
    title="PlaceholderAPI",
    version="0.1.0"
)

@app.get('/')
def redirect():
    return RedirectResponse('/docs')

@app.get('/{width}/{height}/{color}')
def generate_image(
    width:int,
    height:int,
    color:str,
    fontsize:Optional[int]=18,
    text:Optional[str]=None
    ):
    if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', f'#{color}'):
        raise HTTPException(status_code=400,detail=f"#{color} is not a valid hex color code")
    W, H = (width,height)
    rgb = ImageColor.getcolor(f'#{color}', "RGB")
    image = Image.new("RGB", (W, H), rgb)
    if text is not None:
        para = textwrap.wrap(text, width=15)
        current_h, pad = 50, 10
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", fontsize)
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text(((W - w) / 2, current_h), line, font=font, fill=(169,169,169))
            current_h += h + pad
    buffer = BytesIO()
    image.save(buffer,format='PNG')
    buffer.seek(0)
    return StreamingResponse(buffer,media_type='image/png')



