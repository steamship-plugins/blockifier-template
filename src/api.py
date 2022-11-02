"""Example Steamship Blockifier Plugin.

A Blockifier is responsible for transforming some type of data into
Steamship's internal Block format.
"""
from typing import Type

from steamship.base.error import SteamshipError
from steamship.base import MimeTypes
from steamship.data.block import Block
from steamship.data.file import File
from steamship.data.tags import TagKind, DocTag, Tag
from steamship.invocable import Config, InvocableResponse, create_handler, post
from steamship.plugin.blockifier import Blockifier
from steamship.plugin.inputs.raw_data_plugin_input import RawDataPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput
from steamship.plugin.request import PluginRequest


class BlockifierPlugin(Blockifier):
    """"Example Steamship Blockifier plugin."""

    def config_cls(self) -> Type[Config]:
        return Config

    def run(self, request: PluginRequest[RawDataPluginInput]) -> InvocableResponse[BlockAndTagPluginOutput]:
        """Every plugin implements a `run` function.

        This template plugin does an extremely simple form of text parsing:
            - It checks that the incoming data is text.
            - It then interprets any newline character as a paragraph break.
            - It returns a single block spanning all of the text, with tags for those paragraphs.
        """

        # Only accept content of type text/plain. Otherwise return an error.
        if request.data.default_mime_type != MimeTypes.TXT:
            return InvocableResponse(error=SteamshipError(
                message="This blockifier only accepts text of type {}".format(MimeTypes.TXT)
            ))

        # This isn't necessary, but demonstrates that we can expect that Steamship
        # has properly interpreted the incoming bytes as a string object.
        if type(request.data.data) != str:
            return InvocableResponse(error=SteamshipError(
                message="The incoming data was not of expected String type"
            ))

        # Now let's split the text into paragraphs by splitting on newline.
        paragraphs = request.data.data.split("\n")
        paragraphs = [p.strip() for p in paragraphs]  # Strip extra whitespace
        paragraphs = list(filter(lambda x: len(x) > 0, paragraphs))  # Eliminate empty paragraphs

        # Now let's reconstruct the text.
        block_text = None
        tags = []
        for p in paragraphs:
            if block_text is None:
                start_idx = 0
                block_text = p
            else:
                block_text += '\n\n'
                start_idx = len(block_text)
                block_text += p

            # Create a tag for this paragraph
            tags.append(
                Tag.CreateRequest(
                    kind=TagKind.DOCUMENT,
                    name=DocTag.PARAGRAPH,
                    startIdx=start_idx,
                    endIdx=len(block_text)
                )
            )

        # And return the response. All plugins return a InvocableResponse. Blockifier plugins set the data
        # field of this object to BlockAndTagPluginOutput.
        return InvocableResponse(data=BlockAndTagPluginOutput(
            file=File.CreateRequest(
                blocks=[Block.CreateRequest(text=block_text, tags=tags)]
            )
        ))


handler = create_handler(BlockifierPlugin)
