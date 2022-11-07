import os

from steamship import TaskState
from steamship.plugin.inputs.raw_data_plugin_input import RawDataPluginInput
from steamship.plugin.request import PluginRequest
from steamship.data.tags import TagKind, DocTag
from api import BlockifierPlugin

__copyright__ = "Steamship"
__license__ = "MIT"


def _read_test_file(filename: str) -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, '..', 'test_data', filename), 'r') as f:
        return f.read()


def test_blockifier():
    blockifier = BlockifierPlugin()
    roses = _read_test_file('roses.mkd')
    request = PluginRequest(data=RawDataPluginInput(data=roses, defaultMimeType="text/plain"))
    response = blockifier.run(request)

    assert (response.status.state is TaskState.succeeded)

    blockified_file = response.data.file
    assert (blockified_file is not None)
    assert (blockified_file.blocks is not None)
    assert (len(blockified_file.tags) == 0)
    assert (len(blockified_file.blocks) == 1)

    block = blockified_file.blocks[0]
    assert (block.text == roses)
    assert (len(block.tags) == 3)

    t1 = block.tags[0]
    t2 = block.tags[1]
    t3 = block.tags[2]

    assert (block.text[t1.start_idx:t1.end_idx] == "# A Poem")
    assert (block.text[t2.start_idx:t2.end_idx] == "Roses are red. Violets are blue.")
    assert (block.text[t3.start_idx:t3.end_idx] == "Sugar is sweet, and I love you.")

    for t in block.tags:
        assert (t.kind == TagKind.DOCUMENT)
        assert (t.name == DocTag.PARAGRAPH)
