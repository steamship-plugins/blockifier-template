# Steamship Converter Plugin

This project implements a basic Steamship Converter that you can customize and deploy for your own use.

In Steamship, **Converters** are responsible for converting some real-world data format into Steamship's universal **Block Format**.

This sample project transforms raw text into paragraphs, but other converters might:

* Perform OCR on an image
* Perform speech-to-text
* Extract the contents of a Wikipedia page

Once a Converter has returned data to Steamship as **Block Format**, that data is ready for use by the rest of the ecosystem.

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

* The ConverterPlugin class
* The `/convert` endpoint

## Testing

Tests are located in the `test/test_api.py` file. You can run them with:

```bash
pytest
```

We have provided sample data in the `test_data/` folder.

## Deploying

Deploy your converter to Steamship by running:

```bash
ship deploy --register-plugin
```

That will deploy your app to Steamship and register it as a plugin for use.

The first time, you will be asked a few questions:
* What to name your plugin
* What handle to give your plugin

Your answers will be saved in the `nludb.json` file of this project.

## Using

Once deployed, your Convert Plugin can be referenced by the handle in your `steamship.json` file.

```python
from steamship import Steamship, BlockTypes

MY_PLUGIN_HANDLE = ".. fill this out .."

client = Steamship()
file = client.create_file(file="./test_data/king_speech.txt")
file.convert(plugin=MY_PLUGIN_HANDLE).wait()
file.query(blockType=BlockTypes.Paragraph).wait().data
```

## Sharing

Plesae share what you've built with hello@steamship.com! 

We would love take a look, hear your suggestions, help where we can, and share what you've made with the community.