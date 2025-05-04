import argparse
import os
from re import *

def pluralize(word):
    if search('[sxz]$', word) or search('[^aeioudgkprt]h$', word):
        return sub('$', 'es', word)
    elif search('[bcdfghjklmnpqrstvwxz]y$', word):
        return sub('y$', 'ies', word)
    else:
        return word + 's'

def to_normal_case(value):
    return ' '.join(value.split('-'))

def to_snake_case(value):
    return "_".join(value.lower().split('-'))

def to_pascal_case(value):
    return "".join(value.title().split('-'))

def to_camel_case(value):
    content = "".join(value.title().split('-'))
    return content[0].lower() + content[1:]

def create_mod_dir(name):
    os.mkdir(os.path.join(base_path, name))

def create_providers_dir(name):
    os.mkdir(os.path.join(base_path, f'{name}/providers'))

def create_interfaces_dir(name):
    os.mkdir(os.path.join(base_path, f'{name}/interfaces'))

def create_entities_dir(name):
    os.mkdir(os.path.join(base_path, f'{name}/entities'))

def create_dtos_dir(name):
    os.mkdir(os.path.join(base_path, f'{name}/dtos'))

def create_responses_dir(name):
    os.mkdir(os.path.join(base_path, f'{name}/responses'))

def read_template(template_name):
    template_path = os.path.join(template_dir, template_name)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file {template_path} not found")
    with open(template_path, 'r') as file:
        return file.read()

def format_template(template_content, name, template_name, attr_map=None):
    format_dict = {
        'normal': to_normal_case(name),
        'normal_capital': to_normal_case(name.capitalize()),
        'camel': to_camel_case(name),
        'camel_plural': to_camel_case(pluralize(name)),
        'pascal': to_pascal_case(name),
        'plural_kebab': pluralize(name),
        'snake': to_snake_case(name),
        'snake_plural': to_snake_case(pluralize(name)),
        'plural_normal': to_normal_case(pluralize(name)),
        'plural_capitalized': to_normal_case(pluralize(name.capitalize())),
        'kebab': name
    }
    
    # Handle attributes placeholder
    if attr_map and '<%attributes%>' in template_content:
        attributes_text = ''
        for attr_name in attr_map:
            if 'interface' in template_name:
                attributes_text += f'  {to_camel_case(attr_name)}: {attr_map[attr_name]};\n'
            elif 'entity' in template_name:
                additional = ', nullable: true' if attr_name.endswith('?') else ''
                attributes_text += f'''
  @Column({{ name: '{to_snake_case(attr_name.replace('?',''))}'{additional} }})
  {to_camel_case(attr_name)}: {attr_map[attr_name]};
'''
            elif 'response' in template_name:
                attributes_text += f'''
  {to_camel_case(attr_name)}: {attr_map[attr_name]};
'''
        template_content = template_content.replace('<%attributes%>', attributes_text.rstrip('\n'))
    
    # Replace <%key%> placeholders with values from format_dict
    for key, value in format_dict.items():
        template_content = template_content.replace(f'<%{key}%>', value)
    
    return template_content

def create_file(name, filename, template_name, attr_map=None):
    template_content = read_template(template_name)
    content = format_template(template_content, name, template_name, attr_map)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        file.write(content)

def create_mod_file(name):
    filename = os.path.join(base_path, f'{name}/{name}.module.ts')
    create_file(name, filename, 'module.template')

def create_controller_file(name):
    filename = os.path.join(base_path, f'{name}/{name}.controller.ts')
    create_file(name, filename, 'controller.template')

def create_repo_file(name):
    filename = os.path.join(base_path, f'{name}/providers/{name}.repository.ts')
    create_file(name, filename, 'repository.template')

def create_service_file(name):
    filename = os.path.join(base_path, f'{name}/providers/{name}.service.ts')
    create_file(name, filename, 'service.template')

def create_irepo_file(name):
    filename = os.path.join(base_path, f'{name}/interfaces/{name}.repository.interface.ts')
    create_file(name, filename, 'repository.interface.template')

def create_iservice_file(name):
    filename = os.path.join(base_path, f'{name}/interfaces/{name}.service.interface.ts')
    create_file(name, filename, 'service.interface.template')

def create_ires_file(name, attr_map):
    filename = os.path.join(base_path, f'{name}/interfaces/{name}.interface.ts')
    create_file(name, filename, 'interface.template', attr_map)

def create_entity_file(name, attr_map):
    filename = os.path.join(base_path, f'{name}/entities/{name}.entity.ts')
    create_file(name, filename, 'entity.template', attr_map)

def create_create_dto_file(name):
    filename = os.path.join(base_path, f'{name}/dtos/create-{name}.dto.ts')
    create_file(name, filename, 'create.dto.template')

def create_update_dto_file(name):
    filename = os.path.join(base_path, f'{name}/dtos/update-{name}.dto.ts')
    create_file(name, filename, 'update.dto.template')

def create_response_file(name, attr_map):
    filename = os.path.join(base_path, f'{name}/responses/{name}.response.ts')
    create_file(name, filename, 'response.template', attr_map)

def create_paginated_response_file(name):
    filename = os.path.join(base_path, f'{name}/responses/{name}.paginated.response.ts')
    create_file(name, filename, 'paginated.response.template')

parser = argparse.ArgumentParser(prog='ResGen', description='Generates resources')
parser.add_argument('modname')
parser.add_argument('attributes')
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('-c', '--controller', action='store_true')
parser.add_argument('-s', '--service', action='store_true')

args = parser.parse_args()
curr_dir = os.getcwd()
base_path = os.path.join(curr_dir, 'src/modules')
script_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(script_dir, 'template')
attrs = args.attributes.split(',')
attr_map = {}
for attr in attrs:
    name, type_ = attr.split(':')
    attr_map[name] = type_
name = args.modname
all = args.all
ctrl = args.controller
service = args.service

create_mod_dir(name)
create_mod_file(name)
create_providers_dir(name)
create_interfaces_dir(name)
create_entities_dir(name)
create_ires_file(name, attr_map)
create_repo_file(name)
create_irepo_file(name)
create_entity_file(name, attr_map)

if ctrl or all:
    create_controller_file(name)
    create_responses_dir(name)
    create_response_file(name, attr_map)
    create_paginated_response_file(name)

if service or ctrl or all:
    create_dtos_dir(name)
    create_create_dto_file(name)
    create_update_dto_file(name)
    create_iservice_file(name)
    create_service_file(name)