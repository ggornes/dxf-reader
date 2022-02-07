import os
import pathlib
import re
import shutil
import uuid
import ezdxf

from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from matplotlib import pyplot as plt

from app.settings import FILE_STORAGE


class FileHandler:
    file_repository = FILE_STORAGE

    def __init__(self, file_repository: FILE_STORAGE):
        self.file_repository = file_repository

    def handle_upload(self, file: object):

        # Generate names and build save paths
        original_filename = os.path.splitext(file.filename)[0] + os.path.splitext(file.filename)[1]
        file_id = str(uuid.uuid1())
        new_filename = file_id + ".dxf"
        save_file_path = FILE_STORAGE
        uploaded_files_dir = os.path.join(pathlib.Path().absolute() / save_file_path)
        uploaded_file_path = os.path.join(uploaded_files_dir, new_filename)

        # Todo: catch exceptions
        if not os.path.exists(uploaded_files_dir):
            os.makedirs(uploaded_files_dir)
        open_folder = open(uploaded_file_path, 'wb+')
        shutil.copyfileobj(file.file, open_folder)
        open_folder.close()

        # dxf_file = DxfFile(original_filename)
        return original_filename, file_id

    def get_blocks_from_file(self, file_id: str, qry: str) -> object:
        file_path = FILE_STORAGE + file_id + ".dxf"

        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()

        all_blocks = []
        block_attributes_tuple_list = []

        query_string = 'INSERT[name=="' + qry + '"]'

        # for insert in msp.query('INSERT[name=="LUMINARIA"]'):
        for insert in msp.query(query_string):
            print(insert)

            # append the type of blocks we are reading (LUMINARIA in this case)
            block_attributes_tuple_list.append(("name", qry))
            block_attributes_tuple_list.append(("INSERT_id_ref", str(insert))) # this is if we want to keep track of the reference to the .dxf file

            # block_attributes list
            for attrib in insert.attribs:
                attribute_name = attrib.dxf.tag
                attribute_value = attrib.dxf.text
                attribute_tuple = (attribute_name, attribute_value)
                block_attributes_tuple_list.append(attribute_tuple)

            # convert attribute_list into dictionary
            attribute_dict = dict(block_attributes_tuple_list)
            print(attribute_dict)

            block_attributes_tuple_list.clear()
            all_blocks.append(attribute_dict)

        return all_blocks

    def handle_convert_to_png(self, file_id: str):
        default_img_format = '.png'
        default_img_res = 300
        default_bg_color = '#FFFFFF'  # White
        clr = default_bg_color
        img_format = default_img_format
        img_res = default_img_res

        file_path = FILE_STORAGE + file_id + ".dxf"

        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        # Recommended: audit & repair DXF document before rendering
        auditor = doc.audit()
        if len(auditor.errors) != 0:
            raise Exception("This DXF document is damaged and can't be converted! --> ", file_path)
        else:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            ctx = RenderContext(doc)
            ctx.set_current_layout(msp)
            ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = clr
            out = MatplotlibBackend(ax)
            Frontend(ctx, out).draw_layout(msp, finalize=True)

            img_name = re.findall("(\S+)\.", file_path)  # select the image name that is the same as the dxf file name
            img_path = ''.join(img_name) + img_format  # concatenate list and string
            fig.savefig(img_path, dpi=img_res)
            # print(file_path, " Converted Successfully")
            return img_path
