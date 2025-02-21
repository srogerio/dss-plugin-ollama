import dataiku
from dataiku.connector import Connector
import ollama
import datetime  # Import datetime

class OllamaDataset(Connector):

    def __init__(self, config, plugin_config):
        Connector.__init__(self, config, plugin_config)
        self.ollama_host = config.get('ollama_host', "localhost")
        self.ollama_port = config.get('ollama_port', 11434)
        self.model_name = config.get('model_name')
        self.prompt = config.get('prompt')
        # The Ollama client library handles the URL construction:
        self.client = ollama.Client(host=f"http://{self.ollama_host}:{self.ollama_port}")


    def get_read_schema(self):
        return [
            {"name": "prompt", "type": "string"},
            {"name": "response", "type": "string"},
            {"name": "model", "type": "string"},
            {"name": "done", "type": "boolean"},
            {"name": "timestamp", "type": "date"} # Useful for tracking
        ]

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                      partition_id=None, records_limit=-1):

        response_stream = self.client.generate(model=self.model_name, prompt=self.prompt, stream=True)

        for chunk in response_stream:
            # Each 'chunk' is a dictionary with keys like 'response', 'done', 'model'.
            # The 'response' key only contains *part* of the full response in each chunk.
            yield {
                "prompt": self.prompt,
                "response": chunk.get('response', ''),  # Get the partial response
                "model": chunk.get('model', self.model_name), #The model can change during streaming.
                "done": chunk.get('done', False),
                "timestamp": datetime.datetime.now()
            }