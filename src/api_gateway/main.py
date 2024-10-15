from fastapi import FastAPI, File, UploadFile

from schemas import Login, Signup

app=FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.post("/login")
async def login(request, login:Login):
    """Call login service and return token as response

    Returns:
        JsonResponse: Token information
    """
    return {"access_token":"test"}

@app.post("/signup")
async def signup(signup:Signup):
    """Call signup service and return signup success response

    Returns:
        JsonResponse: Signup success information
    """
    return {"message":"signup success"}

@app.post("/convert-video")
async def convert_video(video_file:UploadFile=File(...)):
    """Call upload video service and return upload video success response

    Returns:
        JsonResponse: Upload video success information
    """
    # todo: validate if logged in
    # todo: upload video to mongodb
    # todo: return video id
    # todo: trigger mp3 coonverter event via message broker
    # todo: convert video to mp3
    return {"message":"upload video success"}

