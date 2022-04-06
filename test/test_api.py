from steamship.plugin.service import PluginRequest
from steamship.plugin.inputs.raw_data_plugin_input import RawDataPluginInput
from steamship.data.tags import TagKind, DocTag
from src.api import ConverterPlugin
import os

__copyright__ = "Steamship"
__license__ = "MIT"

def _read_test_file(filename: str) -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, '..', 'test_data', filename), 'r') as f:
        return f.read()

def test_converter():
    converter = ConverterPlugin()
    roses = _read_test_file('roses.mkd')
    request = PluginRequest(data=RawDataPluginInput(
        data=roses,
        defaultMimeType="text/plain"
    ))
    response = converter.run(request)

    assert(response.error is None)
    assert(response.data is not None)
    assert (response.data.file is not None)
    assert (response.data.file.blocks is not None)
    assert (response.data.file.tags is None)
    assert (len(response.data.file.blocks) == 1)

    block = response.data.file.blocks[0]
    assert (block.text == roses)
    assert (len(block.tags) == 3)

    t1 = block.tags[0]
    t2 = block.tags[1]
    t3 = block.tags[2]

    assert(block.text[t1.startIdx:t1.endIdx] == "# A Poem")
    assert(block.text[t2.startIdx:t2.endIdx] == "Roses are red. Violets are blue.")
    assert(block.text[t3.startIdx:t3.endIdx] == "Sugar is sweet, and I love you.")

    for t in block.tags:
        assert(t.kind == TagKind.doc)
        assert(t.name == DocTag.paragraph)

