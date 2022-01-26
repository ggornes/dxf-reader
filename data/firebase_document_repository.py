from data.document_repository import DocumentRepository
from domain.dxf_document import DxfDocument


class BaseRepository:
    def __init__(self, db) -> None:
        self.db = db


class FirebaseDocumentRepository(BaseRepository, DocumentRepository):
    def save(self, dxf_document: DxfDocument) -> None:
        file_id = dxf_document.file_id
        original_filename = dxf_document.original_filename
        blocks = dxf_document.blocks

        # todo: try except block
        new_doc_ref = self.db.collection(u'documents').document(file_id)
        new_doc_ref.set({u'original_filename': original_filename, u'file_id': file_id, u'blocks': blocks})
        new_doc = new_doc_ref.get()
        return new_doc.to_dict()

    def load(self, file_id: str) -> object:
        doc_ref = self.db.collection(u'documents').document(file_id)
        doc = doc_ref.get()
        doc_dict = doc.to_dict()
        # dxf_document = DxfDocument(doc_dict["file_id"], doc_dict["original_filename"], doc_dict["blocks"])
        return doc_dict

    def update(self, dxf_document: DxfDocument) -> object:
        file_id = dxf_document.file_id
        all_blocks = dxf_document.blocks
        doc_ref = self.db.collection(u'documents').document(file_id)
        doc_ref.update({u'blocks': all_blocks})
        doc = doc_ref.get()
        doc_dict = doc.to_dict()
        return doc_dict
