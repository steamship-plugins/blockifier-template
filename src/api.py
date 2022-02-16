"""Example Steamship Converter Plugin.

A Convert is responsible for transforming some type of data into
Steamship's internal Block format.
"""

from steamship import Block, BlockTypes, MimeTypes, SteamshipError
from steamship.app import App, post, create_handler, Response
from steamship.data.converter import ConvertResponse, ConvertRequest
from steamship.plugin.converter import Converter
from steamship.plugin.service import PluginResponse, PluginRequest


class ConverterPlugin(Converter, App):
    """"Example Steamship Converter plugin."""

    def run(self, request: PluginRequest[ConvertRequest]) -> PluginResponse[ConvertResponse]:
        """Every plugin implements a `run` function.

        This template plugin does an extremely simple form of text parsing:
            - It checks that the incoming data is text
            - It then interprets any newline character as a paragraph break
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

        # Finally we'll return a tree of Blocks, Steamship's internal format
        document = Block(type=BlockTypes.Document, children=[])
        for text in paragraphs:
            document.children.append(Block(type=BlockTypes.Paragraph, text=text))

        # And return the response. All plugins return a PluginResponse. Converter Plugins set the data
        # field of this object to a ConvertResponse.
        return PluginResponse(data=ConvertResponse(root=document))

    @post('convert')
    def convert(self, **kwargs) -> Response:
        """App endpoint for our plugin.

        The `run` method above implements the Plugin interface for a Converter.
        This `convert` method exposes it over an HTTP endpoint as a Steamship App.

        When developing your own plugin, you can almost always leave the below code unchanged.
        """
        convertRequest = Converter.parse_request(request=kwargs)
        convertResponse = self.run(convertRequest)
        ret = Converter.response_to_dict(convertResponse)
        return Response(json=ret)


handler = create_handler(ConverterPlugin)
