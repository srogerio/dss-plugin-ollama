import requests
import json
from ollama_common import DSSSelectorChoices, get_configuration


def do(payload, config, plugin_config, inputs):
    parameter_name = payload.get('parameterName')
    server_url, _, _ = get_configuration(config)
    choices = DSSSelectorChoices()
    if parameter_name in ["model_select"]:
        choices.start_with_manual_select()
        models = []
        try:
            response = requests.get(url="{}/api/tags".format(server_url))
            json_response = response.json()
            models = json_response.get("models", [])
        except Exception as error:
            pass
        for model in models:
            choices.append(
                "{}".format(model.get("name")), #label,
                "{}".format(model.get("name"))#value
            )
        #choices.append_column_select()
    return choices.to_dss()
