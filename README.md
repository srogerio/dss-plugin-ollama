# Ollama Plugin for Dataiku DSS

## Overview

The Ollama plugin extends the capabilities of Dataiku flow with custom nodes that leverage the power of language models. With this plugin, users can easily incorporate AI-driven text generation and processing tasks directly into their data workflows.

## Features

- **Text Generation**: Generate text using advanced language models.
- **Custom Nodes**: Integrate seamlessly as new node types within Dataiku DFlow.
- **Configurable Parameters**: Customize model settings, input parameters, and output formats.
- **User-Friendly Interface**: Easy to configure through the Dataiku UI.

## Installation

### Prerequisites

- Dataiku DSS (version 12.0 or later)
- Access to Ollama API endpoints

### Steps to Install

1. Download the latest release of the Ollama plugin from our [GitHub repository](https://github.com/alexbourret/dss-plugin-ollama/releases).

2. Extract the downloaded file into a directory accessible by your Dataiku DSS instance.

3. Navigate to **Apps > Plugins** in your Dataiku DSS interface.

4. Click on **Add plugin > Upload** and select the extracted plugin folder.

5. Follow the prompts to complete the installation process.

## Usage

The plugin consists in a custom recipe that take in input dataset, run an LLM model for every row in the input dataset based on a prompt that can integrate data contained by any column of that row.

1. In your Dataiu flow, select the input dataset that contains the work material for the LLM. 

2. In the right hand panel, pick the Ollama plugin recipe > Prediction, and create the output dataset

3. Select a prompt source. It can be a column of the input dataset, or a fixed prompt.

   - The fixed prompt can use data contained in any column of the input dataset, by using the `{{column name}}` format

4. Select the model

   - either select it from a list already installed models, 
   - or type the name of the model. Templates are allowed, so that name can be taked from an input's column

5. If it applies (for Llava for instance), add the column name containing the URL to an image

## Troubleshooting

- Ensure that your Dataiku DSS version is compatible with this plugin.
- Check network connectivity if you encounter issues accessing Ollama API endpoints.
- Review logs in **Admin > Logs** for detailed error messages and solutions.

## License

This plugin is distributed under the Apache License version 2.0
