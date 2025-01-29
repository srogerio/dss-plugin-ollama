import dataiku
import pandas
import requests
import json
import base64

from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

from ollama_common import (extract_string, process_template, get_configuration)


input_A_names = get_input_names_for_role('input_A_role')
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

output_A_names = get_output_names_for_role('main_output')
config = get_recipe_config()
prompts_df = input_A_datasets[0].get_dataframe()

server_url, model_name_template, output_format = get_configuration(config)

output = dataiku.Dataset(output_A_names[0])

first_dataframe = True
prompt_source = config.get("prompt_source", "column")
prompt_column = config.get("prompt_column")
image_column = config.get("image_column")
with output.get_writer() as writer:
    unnested_items_rows = []
    for index, input_parameters_row in prompts_df.iterrows():
        row = input_parameters_row.to_dict()
        if prompt_source == "column":
            prompt_template = row.get(prompt_column, "")
        else:
            prompt_template = config.get("prompt", "")
        prompt = process_template(prompt_template, row)
        model_name = process_template(model_name_template, row)
        image = None
        if image_column:
            image_url = row.get(image_column)
            if image_url and image_url.startswith("http"):
                # image = upload_image(image_url)
                # image = base64.b64encode(image).decode('utf-8')
                image = base64.b64encode(requests.get(image_url).content).decode('utf-8')
        data = {
          "model": "{}".format(model_name),
          "prompt": "{}".format(prompt)
         }
        if image:
            data["images"] = [image]
        if output_format:
            data["format"] = output_format
        try:
            response = requests.post(url="{}/api/generate".format(server_url), json=data)
        except Exception as error:
            raise Exception("Connection error: {}".format(error))
        answer = extract_string(response.content)
        if output_format == 'json':
            try:
                row['answer'] = json.loads(answer)
            except Exception as error:
                print("Not a valid JSON", error)
                row['answer'] = answer
        else:
            row['answer'] = answer
        unnested_items_rows.append(row)
    unnested_items_rows = pandas.DataFrame(unnested_items_rows)
    if first_dataframe:
        output.write_schema_from_dataframe(unnested_items_rows)
        first_dataframe = False
    if not unnested_items_rows.empty:
        writer.write_dataframe(unnested_items_rows)
