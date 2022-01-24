from fastapi import APIRouter, status, Request, FastAPI, UploadFile, File
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse

from app.settings import FILE_STORAGE
from domain import file_handler
from domain.file_handler import FileHandler


def get_application():
    app = FastAPI(title="dxf file reader API")

    # ################### CORS ################### #
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_application()

router = APIRouter()

file_handler = FileHandler(FILE_STORAGE)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
def handle_upload_file_request(request: Request, file: UploadFile = File(...)):
    # Todo validate file
    file_id = file_handler.handle_save(file)

    return JSONResponse(
        status_code=201,
        content={
            "filename": file_id}
    )


@router.get("/dxf/{file_id}/read",
            status_code=status.HTTP_200_OK)
def read_dxf_file(file_id: str):
    all_blocks = file_handler.handle_parse(file_id)

    return JSONResponse(
        status_code=200,
        content={
            "blocks": jsonable_encoder(all_blocks)}
    )


@router.get("/dxf/{file_id}/convert",
            status_code=status.HTTP_200_OK)
def dxf_to_img(file_id: str):
    img_path = file_handler.handle_convert_to_png(file_id)

    return FileResponse(img_path)


app.include_router(router)
