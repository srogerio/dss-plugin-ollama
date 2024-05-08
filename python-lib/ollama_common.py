import json


def extract_string(source):
    source = source.decode('utf-8')
    response_strings = source.split("\n")
    answer = ""
    for response_string in response_strings:
        try:
            dictionary = json.loads(response_string)
        except:
            break
        answer += "{}".format(dictionary.get("response", ""))
    return answer


def process_template(template, dictionnary):
    template = str(template)
    for key in dictionnary:
        replacement = str(dictionnary.get(key, ""))
        template = template.replace("{{{{{}}}}}".format(key), str(replacement))
    return template


def get_configuration(config):
    if config.get("display_advanced_parameters", False):
        server_url = config.get("server_url", "http://localhost:11434")
        model_name = config.get("model_name", "mistral")
    else:
        server_url = "http://localhost:11434"
        model_name = "mistral"
    server_url = server_url.strip("/")
    return server_url, model_name
