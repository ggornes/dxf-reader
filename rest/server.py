from fastapi import APIRouter, status, Request, FastAPI, UploadFile, File
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse

from app.settings import FILE_STORAGE, FIREBASE_SERVICE_ACCOUNT
from data.firebase_document_repository import FirebaseDocumentRepository

from domain import file_handler
from domain.document_handler import DxfDocumentHandler
from domain.dxf_document import DxfDocument
from domain.file_handler import FileHandler

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


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

# ################ DB ####################### #
cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
firebase_admin.initialize_app(cred)
db = firestore.client()


dxf_document_repository = FirebaseDocumentRepository(db)
dxf_document_handler = DxfDocumentHandler(dxf_document_repository)

file_handler = FileHandler(FILE_STORAGE)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
def handle_upload_file_request(request: Request, file: UploadFile = File(...)):
    # Todo: sanitize file (ie. validate file is .dxf, size, etc...)
    original_filename, file_id = file_handler.handle_upload(file)

    # create new firebase document
    new_doc = dxf_document_handler.handle_new(original_filename=original_filename, file_id=file_id)

    # get document
    # db_doc = dxf_document_handler.handle_get(file_id)

    return JSONResponse(
        status_code=201,
        content=new_doc
    )


@router.get("/dxf/{file_id}/read",
            status_code=status.HTTP_200_OK)
def get_blocks_from_file(file_id: str):
    # get all blocks from file
    # file query handler !== db query handler
    luminaria_blocks = file_handler.get_blocks_from_file(file_id=file_id, qry="LUMINARIA")  # should match autocad tag name

    # get document
    doc = dxf_document_handler.handle_get(file_id)

    dxf_document = DxfDocument(
        original_filename=doc["original_filename"],
        file_id=doc["file_id"],
        blocks=doc["blocks"]
    )

    # append blocks to dxf_document and update db document
    dxf_document.blocks = luminaria_blocks
    updated_doc = dxf_document_handler.handle_update(dxf_document)

    return JSONResponse(
        status_code=200,
        content=updated_doc
    )


@router.get("/dxf/{file_id}/convert",
            status_code=status.HTTP_200_OK)
def dxf_to_img(file_id: str):
    img_path = file_handler.handle_convert_to_png(file_id)

    return FileResponse(img_path)


app.include_router(router)
