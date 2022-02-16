from steamship.data.converter import ConvertRequest
from steamship.plugin.service import PluginRequest
from steamship import BlockTypes
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
    request = PluginRequest(data=ConvertRequest(
        data=roses,
        defaultMimeType="text/plain"
    ))
    response = converter.run(request)

    assert(response.error is None)
    assert(response.data is not None)

    assert (response.data.root is not None)
    assert (response.data.root.type == BlockTypes.Document)

    # The root should have three paragraph children.
    # Note: roses.txt is markdown, but the demo converter just parses pragraphs!
    paragraphs = list(map(
        lambda para: para.strip(),
        roses.split('\n')
    ))
    paragraphs = list(filter(
        lambda para: len(para) > 0,
        paragraphs
    ))

    assert (len(response.data.root.children) == 3)
    assert (len(paragraphs) == 3) # Test the test itself :)
    for (i, child) in enumerate(response.data.root.children):
        assert (child.type == BlockTypes.Paragraph)
        assert (child.text == paragraphs[i])

