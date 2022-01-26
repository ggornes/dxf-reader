class DxfDocument:
    file_id: str
    original_filename: str
    blocks: list

    # def __init__(self, file_id: str):
    #     self.file_id = file_id

    def __init__(self, original_filename: str, file_id: str, blocks: list):
        self.original_filename = original_filename
        self.file_id = file_id
        self.blocks = blocks
