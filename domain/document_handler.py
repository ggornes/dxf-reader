from data.document_repository import DocumentRepository
from domain.dxf_document import DxfDocument


class DxfDocumentHandler:
    document_repository: DocumentRepository

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def handle_upload(self, original_filename: str, file_id: str) -> object:
        new_dxf_doc = DxfDocument(original_filename, file_id, [])
        new_doc = self.document_repository.save(new_dxf_doc)
        return new_doc

    def handle_get(self, file_id: str) -> object:
        dxf_doc = self.document_repository.load(file_id)
        return dxf_doc

    def handle_get_all_documents(self) -> list:
        all_docs = self.document_repository.find_all()
        return all_docs

    def handle_get_document(self, file_id: str) -> object:
        doc = self.document_repository.find_by_file_id(file_id)
        return doc

    def handle_update(self, dxf_document: DxfDocument) -> object:
        updated_doc = self.document_repository.update(dxf_document)
        return updated_doc

