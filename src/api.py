"""Example Steamship Converter Plugin.

A Convert is responsible for transforming some type of data into
Steamship's internal Block format.
"""

from steamship.app import App, Response, post, create_handler
from steamship.plugin.converter import Converter
from steamship.plugin.service import PluginResponse, PluginRequest
from steamship.base.error import SteamshipError
from steamship.base import MimeTypes
from steamship.data.block import Block
from steamship.data.file import File
from steamship.data.tags import TagKind, DocTag, Tag
from steamship.plugin.inputs.raw_data_plugin_input import RawDataPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput


class ConverterPlugin(Converter, App):
    """"Example Steamship Converter plugin."""

    def run(self, request: PluginRequest[RawDataPluginInput]) -> PluginResponse[BlockAndTagPluginOutput]:
        """Every plugin implements a `run` function.

        This template plugin does an extremely simple form of text parsing:
            - It checks that the incoming data is text.
            - It then interprets any newline character as a paragraph break.
            - It returns a single block spanning all of the text, with tags for those paragraphs.
        """

        # Only accept content of type text/plain. Otherwise return an error.
        if request.data.defaultMimeType != MimeTypes.TXT:
            return Response(error=SteamshipError(
                message="This converter only accepts text of type {}".format(MimeTypes.TXT)
            ))

        # This isn't necessary, but demonstrates that we can expect that Steamship
        # has properly interpreted the incoming bytes as a string object.
        if type(request.data.data) != str:
            return Response(error=SteamshipError(
                message="The incoming data was not of expected String type"
            ))

        # Now let's split the text into paragraphs by splitting on newline.
        paragraphs = request.data.data.split("\n")
        paragraphs = [p.strip() for p in paragraphs] # Strip extra whitespace
        paragraphs = list(filter(lambda x: len(x) > 0, paragraphs)) # Eliminate empty paragraphs

        # Now let's reconstruct the text.
        block = Block(tags=[])
        for p in paragraphs:
            if block.text is None:
                startIdx = 0
                block.text = p
            else:
                block.text += '\n\n'
                startIdx = len(block.text)
                block.text += p

            # Create a tag for this para
            block.tags.append(
                Tag.CreateRequest(
                    kind=TagKind.doc,
                    name=DocTag.paragraph,
                    startIdx=startIdx, 
                    endIdx=len(block.text)
                )
            )

        # And return the response. All plugins return a PluginResponse. Converter Plugins set the data
        # field of this object to a ConvertResponse.
        return PluginResponse(data=BlockAndTagPluginOutput(
            file=File.CreateRequest(
                blocks=[block]
            )
        ))

    @post('convert')
    def convert(self, **kwargs) -> Response:
        """App endpoint for our plugin.

        The `run` method above implements the Plugin interface for a Converter.
        This `convert` method exposes it over an HTTP endpoint as a Steamship App.

        When developing your own plugin, you can almost always leave the below code unchanged.
        """
        convertRequest = Converter.parse_request(request=kwargs)
        convertResponse = self.run(convertRequest)
        return Converter.response_to_dict(convertResponse)


handler = create_handler(ConverterPlugin)
