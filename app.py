from fastapi import FastAPI, UploadFile, File , Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np

app = FastAPI()
template = Jinja2Templates(directory='templates')
app.mount("/images", StaticFiles(directory="images"), name="images")

IMAGEDIR = "images/"


@app.get('/')
def main(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.post('/upload')
async def upload_img(request: Request,file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(f"{IMAGEDIR}/out.jpg",img)
    show = ["out.jpg"]
    dct = {"apple": 10, "orange" : 30}
    return template.TemplateResponse("index.html",{"request": request,"show": show, "dct": dct})

