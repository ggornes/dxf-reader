import abc
from uuid import UUID

from domain.dxf_document import DxfDocument


class DocumentRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, document: DxfDocument) -> None:
        pass

    @abc.abstractmethod
    def load(self, file_id: UUID) -> DxfDocument:
        pass

    @abc.abstractmethod
    def update(self, file_id: UUID) -> DxfDocument:
        pass

    # @abc.abstractmethod
    # def delete(self, file_id: UUID) -> object:
    #     pass

