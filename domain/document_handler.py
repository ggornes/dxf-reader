from data.document_repository import DocumentRepository
from domain.dxf_document import DxfDocument


class DxfDocumentHandler:
    document_repository: DocumentRepository

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def handle_new(self, original_filename: str, file_id: str) -> object:
        new_dxf_doc = DxfDocument(original_filename, file_id, [])
        new_doc_ref = self.document_repository.save(new_dxf_doc)
        return new_doc_ref

    def handle_get(self, file_id: str) -> object:
        dxf_doc = self.document_repository.load(file_id)
        return dxf_doc

    def handle_update(self, dxf_document: DxfDocument) -> object:
        updated_doc = self.document_repository.update(dxf_document)
        return updated_doc

