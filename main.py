import re
from io import BytesIO
from typing import Optional
from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw,ImageColor
app = FastAPI(
    title="PlaceholderAPI",
    version="0.1.0"
)

@app.get('/')
def redirect():
    return RedirectResponse('/docs')

@app.get('/{width}/{height}/{color}')
def generate_image(width:int,height:int,color:str,text:Optional[str]=None):
    if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', f'#{color}'):
        raise HTTPException(status_code=400,detail=f"#{color} is not a valid hex color code")
    W, H = (width,height)
    rgb = ImageColor.getcolor(f'#{color}', "RGB")
    image = Image.new("RGB", (W, H), rgb)
    if text is not None:
        text = text.replace(',','\n')
        draw = ImageDraw.Draw(image)
        w, h = draw.textsize(text)
        draw.multiline_text(((W-w)/2,(H-h)/2), text, fill=(0, 0, 0))
    buffer = BytesIO()
    image.save(buffer,format='PNG')
    buffer.seek(0)
    return StreamingResponse(buffer,media_type='image/png')



