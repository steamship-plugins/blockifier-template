# Steamship Blockifier Plugin

This project implements a basic Steamship Blockifier that you can customize and deploy for your own use.

In Steamship, **Blockifiers** are responsible for converting some real-world data format into Steamship's universal **Block Format**.

This sample project transforms raw text into paragraphs, but other blockifiers might:

* Perform OCR on an image
* Perform speech-to-text
* Extract the contents of a Wikipedia page

Once a Blockifier has returned data to Steamship as **Block Format**, that data is ready for use by the rest of the ecosystem.

## First Time Setup

We recommend using Python virtual environments for development.
To set one up, run the following command from this directory:

```bash
python3 -m venv .venv
```

Activate your virtual environment by running:

```bash
source .venv/bin/activate
```

Your first time, install the required dependencies with:

```bash
python -m pip install -r requirements.dev.txt
python -m pip install -r requirements.txt
```

## Developing

All the code for this plugin is located in the `src/api.py` file:

* The BlockifierPlugin class
* The `run` method that handles `blockify` requests

## Testing

Tests are located in the `test/test_api.py` file. You can run them with:

```bash
pytest
```

We have provided sample data in the `test_data/` folder.

## Deploying

Deploy your plugin to Steamship by running:

```bash
ship deploy --register-plugin
```

That will deploy your app to Steamship and register it as a plugin for use.

The first time, you will be asked a few questions:
* What to name your plugin
* What handle to give your plugin

Your answers will be saved in the `steamship.json` file of this project.

## Using

Once deployed, your Blockifier Plugin can be referenced by the handle in your `steamship.json` file.

```python
from pathlib import Path
from steamship import Steamship, File, MimeTypes, Tag

MY_PLUGIN_HANDLE = ".. fill this out .."

client = Steamship(workspace="my-workspace")
blockifier = client.use_plugin(MY_PLUGIN_HANDLE)
test_file = Path("./test_data/king_speech.txt")
with test_file.open("rb") as txt:
    file = File.create(client, content=txt.read(), mime_type=MimeTypes.TXT)
file.blockify(plugin_instance=blockifier.handle).wait()

# now that our file has been blockified, by refreshing the file,
# we can access the blocks (and tags) added by our blockifier
file = file.refresh()
for block in file.blocks:
    print(block.text)
    print(block.tags)

# we can also query for tags in the file (here to see the beginning and end indices of paragraphs)
print("\n".join([str(t.value) for t in Tag.query(client, f'file_id "{file.id}" and kind "paragraph"').tags]))
```

## Sharing

Please share what you've built with hello@steamship.com! 

We would love take a look, hear your suggestions, help where we can, and share what you've made with the community.