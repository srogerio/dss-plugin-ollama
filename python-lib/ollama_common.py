import json
# try:
#     from BytesIO import BytesIO  # for Python 2
# except ImportError:
#     from io import BytesIO  # for Python 3


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
    output_format = None
    if config.get("display_advanced_parameters", False):
        server_url = config.get("server_url", "http://localhost:11434")
        output_format = config.get("output_format", None)
    else:
        server_url = "http://localhost:11434"
    model_name = config.get("model_select")
    if not model_name:
        model_name = config.get("model_name", "mistral")
    server_url = server_url.strip("/")
    return server_url, model_name, output_format


MANUAL_SELECT_ENTRY = {"label": "✍️ Enter manually", "value": None}
COLUMN_SELECT_ENTRY = {"label": "🏛️ Get from column", "value": "dku_column_select"}


# def upload_image(image_url):
#     import tempfile
#     import requests
#     output = None
#     with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
#         response = requests.get(image_url)
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 tmp_file.write(chunk)
#         with tempfile.NamedTemporaryFile(delete=True, suffix=".jpg") as tmp_jpg_file:
#             tmp_jpg_file = jpeg_compress(tmp_file, tmp_jpg_file)
#             tmp_jpg_file.seek(0)
#             output = tmp_file.read()
#     return output


# def jpeg_compress(tmp_file, tmp_jpg_file):
#     from PIL import Image
#     tmp_file.flush()
#     tmp_file.seek(0)
#     raw_image = Image.open(tmp_file.name)
#     buffer = BytesIO()
#     raw_image.save(buffer, "JPEG", quality=70)
#     tmp_jpg_file.write(buffer.getbuffer())
#     tmp_jpg_file.flush()
#     tmp_jpg_file.seek(0)
#     return tmp_jpg_file


class DSSSelectorChoices(object):

    def __init__(self):
        self.choices = []

    def append(self, label, value):
        self.choices.append(
            {
                "label": label,
                "value": value
            }
        )

    def append_alphabetically(self, new_label, new_value):
        index = 0
        new_choice = {
            "label": new_label,
            "value": new_value
        }
        for choice in self.choices:
            choice_label = choice.get("label")
            if choice_label < new_label:
                index += 1
            else:
                break
        self.choices.insert(index, new_choice)

    def append_manual_select(self):
        self.choices.append(MANUAL_SELECT_ENTRY)

    def start_with_manual_select(self):
        self.choices.insert(0, MANUAL_SELECT_ENTRY)

    def append_column_select(self):
        self.choices.append(COLUMN_SELECT_ENTRY)

    def _build_select_choices(self, choices=None):
        if not choices:
            return {"choices": []}
        if isinstance(choices, str):
            return {"choices": [{"label": "{}".format(choices)}]}
        if isinstance(choices, list):
            return {"choices": choices}
        if isinstance(choices, dict):
            returned_choices = []
            for choice_key in choices:
                returned_choices.append({
                    "label": choice_key,
                    "value": choices.get(choice_key)
                })
            return returned_choices

    def text_message(self, text_message):
        return self._build_select_choices(text_message)

    def to_dss(self):
        return self._build_select_choices(self.choices)
