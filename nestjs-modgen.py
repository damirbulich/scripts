#!/opt/homebrew/bin/python3
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
    os.mkdir(os.path.join(base_path, '{name}'.format(name=name)))

def create_providers_dir(name):
    os.mkdir(os.path.join(base_path, '{name}/providers'.format(name=name)))

def create_interfaces_dir(name):
    os.mkdir(os.path.join(base_path, '{name}/interfaces'.format(name=name)))

def create_entities_dir(name):
    os.mkdir(os.path.join(base_path, '{name}/entities'.format(name=name)))

def create_dtos_dir(name):
    os.mkdir(os.path.join(base_path, '{name}/dtos'.format(name=name)))
    
def create_responses_dir(name):
    os.mkdir(os.path.join(base_path, '{name}/responses'.format(name=name)))

def create_mod_file(name):
    filename = os.path.join(base_path, '{name}/{name}.module.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ Module }} from '@nestjs/common';
import {{ TypeOrmModule }} from '@nestjs/typeorm';

import {{ {pascal} }} from './entities/{kebab}.entity';
import {{ {pascal}RepositoryToken }} from './interfaces/{kebab}.repository.interface';
import {{ {pascal}ServiceToken }} from './interfaces/{kebab}.service.interface';
import {{ {pascal}Repository }} from './providers/{kebab}.repository';
import {{ {pascal}Service }} from './providers/{kebab}.service';
import {{ {pascal}Controller }} from './{kebab}.controller';

@Module({{
  imports: [TypeOrmModule.forFeature([{pascal}])],
  controllers: [{pascal}Controller],
  providers: [
    {{
      provide: {pascal}RepositoryToken,
      useClass: {pascal}Repository,
    }},
    {{
      provide: {pascal}ServiceToken,
      useClass: {pascal}Service,
    }},
  ],
  exports: [{pascal}RepositoryToken],
}})
export class {pascal}Module {{}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))

def create_controller_file(name):
    filename = os.path.join(base_path, '{name}/{name}.controller.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  HttpStatus,
  Inject,
  Param,
  Patch,
  Post,
  Query,
}} from '@nestjs/common';
import {{
  ApiCreatedResponse,
  ApiNoContentResponse,
  ApiOkResponse,
  ApiOperation,
  ApiResponse,
  ApiTags,
}} from '@nestjs/swagger';

import {{ NumberIdParam }} from 'src/common/dto/number-id.param';
import {{ NDOExceptionResponse }} from 'src/common/exceptions/custom-exception.response';
import {{ PaginationParams }} from 'src/common/pagination/pagination.params';

import {{ Create{pascal}Dto }} from './dtos/create-{kebab}.dto';
import {{ Update{pascal}Dto }} from './dtos/update-{kebab}.dto';
import {{
  I{pascal}Service,
  {pascal}ServiceToken,
}} from './interfaces/{kebab}.service.interface';
import {{ Paginated{pascal}Response }} from './responses/{kebab}.paginated.response';
import {{ {pascal}Response }} from './responses/{kebab}.response';

@ApiTags('{plural_capitalized}')
@ApiResponse({{
  description: 'Non 2xx response',
  type: NDOExceptionResponse,
}})
@Controller('{plural_kebab}')
export class {pascal}Controller {{
  constructor(
    @Inject({pascal}ServiceToken) private readonly {camel}Service: I{pascal}Service,
  ) {{}}

  @ApiOperation({{ summary: 'Create a new {normal}' }})
  @ApiCreatedResponse({{
    status: HttpStatus.CREATED,
    description: '{normal_capital} resource',
    type: {pascal}Response,
  }})
  @HttpCode(HttpStatus.CREATED)
  @Post()
  create(@Body() data: Create{pascal}Dto) {{
    return this.{camel}Service.create(data);
  }}

  @ApiOperation({{ summary: 'List all {plural_normal}' }})
  @ApiOkResponse({{
    status: HttpStatus.OK,
    description: 'Paginated list of {plural_normal}',
    type: Paginated{pascal}Response,
  }})
  @HttpCode(HttpStatus.OK)
  @Get()
  list(@Query() params: PaginationParams) {{
    return this.{camel}Service.listAll(params);
  }}

  @ApiOperation({{ summary: 'Find a {normal} by ID' }})
  @ApiOkResponse({{
    status: HttpStatus.OK,
    description: '{normal_capital} resource',
    type: {pascal}Response,
  }})
  @HttpCode(HttpStatus.OK)
  @Get(':id')
  find(@Param() {{ id }}: NumberIdParam) {{
    return this.{camel}Service.findOne(id);
  }}

  @ApiOperation({{ summary: 'Update a {normal}' }})
  @ApiOkResponse({{
    status: HttpStatus.OK,
    description: '{normal_capital} resource',
    type: {pascal}Response,
  }})
  @HttpCode(HttpStatus.OK)
  @Patch(':id')
  update(@Param() {{ id }}: NumberIdParam, @Body() data: Update{pascal}Dto) {{
    return this.{camel}Service.update(id, data);
  }}

  @ApiOperation({{ summary: 'Delete a {normal}' }})
  @ApiNoContentResponse({{
    description: '{normal_capital} deleted',
  }})
  @HttpCode(HttpStatus.NO_CONTENT)
  @Delete(':id')
  remove(@Param() {{ id }}: NumberIdParam) {{
    return this.{camel}Service.remove(id);
  }}
}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))

def create_repo_file(name):
    filename = os.path.join(base_path, '{name}/providers/{name}.repository.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ Injectable }} from '@nestjs/common';
import {{ EntityManager, SelectQueryBuilder }} from 'typeorm';

import {{ PaginationParams }} from 'src/common/pagination/pagination.params';

import {{ {pascal} }} from '../entities/{kebab}.entity';
import {{ I{pascal} }} from '../interfaces/{kebab}.interface';
import {{ I{pascal}Repository }} from '../interfaces/{kebab}.repository.interface';

@Injectable()
export class {pascal}Repository implements I{pascal}Repository {{
  constructor(private readonly entity: EntityManager) {{}}

  list(params: PaginationParams): Promise<[I{pascal}[], number]> {{
    return this.getBaseQuery()
      .skip(params.skip)
      .take(params.limit)
      .orderBy('{camel}.createdAt', 'ASC')
      .comment('{pascal}Repository.list')
      .getManyAndCount();
  }}

  findById(id: number): Promise<I{pascal}> {{
    return this.getBaseQuery()
      .where('{camel}.id = :id', {{ id }})
      .comment('{pascal}Repository.findById')
      .getOne();
  }}

  async existById(id: number): Promise<boolean> {{
    return this.entity
      .createQueryBuilder()
      .from({pascal}, '{camel}')
      .where('{camel}.id = :id', {{ id }})
      .comment('{pascal}Repository.existById')
      .getExists();
  }}

  async create({camel}: I{pascal}): Promise<I{pascal}> {{
    const raw = await this.entity
      .createQueryBuilder()
      .insert()
      .into({pascal})
      .values({camel})
      .returning('*')
      .comment('{pascal}Repository.create')
      .execute();
    return raw.generatedMaps[0] as I{pascal};
  }}

  async update({camel}: Partial<I{pascal}>): Promise<I{pascal}> {{
    const raw = await this.entity
      .createQueryBuilder()
      .update({pascal})
      .set({camel})
      .where('id = :id', {{ id: {camel}.id }})
      .returning('*')
      .comment('{pascal}Repository.update')
      .execute();
    return raw.generatedMaps[0] as I{pascal};
  }}

  delete(id: number): Promise<void> {{
    return void this.entity
      .createQueryBuilder()
      .delete()
      .from({pascal})
      .where('id = :id', {{ id }})
      .comment('{pascal}Repository.delete')
      .execute();
  }}

  private getBaseQuery(): SelectQueryBuilder<{pascal}> {{
    return this.entity
      .createQueryBuilder()
      .from({pascal}, '{camel}')
      .select([
        '{camel}.id',
        '{camel}.createdAt',
      ]);
  }}
}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))


def create_service_file(name):
    filename = os.path.join(base_path, '{name}/providers/{name}.service.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ Inject }} from '@nestjs/common';

import {{ NDONotFoundException }} from 'src/common/exceptions/custom.exception';
import {{ PaginationParams }} from 'src/common/pagination/pagination.params';
import {{ PaginationModel }} from 'src/common/pagination/paginaton.model';

import {{ Create{pascal}Dto }} from '../dtos/create-{kebab}.dto';
import {{ Update{pascal}Dto }} from '../dtos/update-{kebab}.dto';
import {{ I{pascal} }} from '../interfaces/{kebab}.interface';
import {{
  I{pascal}Repository,
  {pascal}RepositoryToken,
}} from '../interfaces/{kebab}.repository.interface';
import {{ I{pascal}Service }} from '../interfaces/{kebab}.service.interface';

export class {pascal}Service implements I{pascal}Service {{
  constructor(
    @Inject({pascal}RepositoryToken)
    private readonly {camel}Repository: I{pascal}Repository,
  ) {{}}

  async create(data: Create{pascal}Dto): Promise<I{pascal}> {{
    const {camel} = await this.{camel}Repository.create(data);
    return {camel};
  }}

  async listAll(params: PaginationParams): Promise<PaginationModel<I{pascal}>> {{
    const [{camel_plural}, total] = await this.{camel}Repository.list(params);
    return new PaginationModel<I{pascal}>({camel_plural}, params, total);
  }}

  async findOne(id: number): Promise<I{pascal}> {{
    const {camel} = await this.{camel}Repository.findById(id);
    if (!{camel}) {{
      throw new NDONotFoundException('{normal_capital} not found');
    }}
    return {camel};
  }}

  async checkExistanceOrFail(id: number): Promise<void> {{
    const exist = await this.{camel}Repository.existById(id);
    if (!exist) {{
      throw new NDONotFoundException('{normal_capital} not found');
    }}
  }}

  async update(id: number, data: Update{pascal}Dto): Promise<I{pascal}> {{
    const {camel} = await this.{camel}Repository.findById(id);
    if (!{camel}) {{
      throw new NDONotFoundException('{normal_capital} not found');
    }}
    Object.assign({camel}, data);
    return this.{camel}Repository.update({camel});
  }}

  async remove(id: number): Promise<void> {{
    await this.checkExistanceOrFail(id);
    await this.{camel}Repository.delete(id);
  }}
}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))


def create_irepo_file(name):
    filename = os.path.join(base_path, '{name}/interfaces/{name}.repository.interface.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ PaginationParams }} from 'src/common/pagination/pagination.params';

import {{ I{pascal}, ICreate{pascal} }} from './{kebab}.interface';

export const {pascal}RepositoryToken = Symbol('{pascal}RepositoryToken');

export interface I{pascal}Repository {{

  /**
   * List all {plural_normal}.
   * @param params - pagination parameters: skip, limit
   * @returns List of {normal} entities
   */
  list(params: PaginationParams): Promise<[I{pascal}[], number]>;

  /**
   * Find a {normal} by ID.
   * @param id - ID of the {normal}
   * @returns {pascal} entity
   */
  findById(id: number): Promise<I{pascal} | null>;

  /**
   * Check if a {normal} exists by ID.
   * @param id - ID of the {normal}
   * @returns Boolean
   */
  existById(id: number): Promise<boolean>;

  /**
   * Create a new {normal}.
   * @param {camel} - {pascal} entity
   * @returns {pascal} entity
   */
  create({camel}: ICreate{pascal}): Promise<I{pascal}>;

  /**
   * Update a {normal}.
   * @param {camel} - {pascal} entity
   * @returns {pascal} entity
   */
  update({camel}: Partial<I{pascal}>): Promise<I{pascal}>;

  /**
   * Delete a {normal} by ID.
   * @param id - ID of the {normal}
   */
  delete(id: number): Promise<void>;
}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))


def create_iservice_file(name):
    filename = os.path.join(base_path, '{name}/interfaces/{name}.service.interface.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ PaginationParams }} from 'src/common/pagination/pagination.params';
import {{ PaginationModel }} from 'src/common/pagination/paginaton.model';

import {{ Create{pascal}Dto }} from '../dtos/create-{kebab}.dto';
import {{ Update{pascal}Dto }} from '../dtos/update-{kebab}.dto';
import {{ I{pascal} }} from './{kebab}.interface';

export const {pascal}ServiceToken = Symbol('{pascal}ServiceToken');

export interface I{pascal}Service {{
  /**
   * Create a new {normal}.
   * @param data - {normal} data
   * @returns {pascal} resource
   */
  create(data: Create{pascal}Dto): Promise<I{pascal}>;

  /**
   * List all {plural_normal}.
   * @param params - pagination parameters: skip, limit
   * @returns Paginated list of {normal} entities
   */
  listAll(params: PaginationParams): Promise<PaginationModel<I{pascal}>>;

  /**
   * Find a {normal} by ID.
   * @param id - ID of the {normal}
   * @returns {pascal} resource
   */
  findOne(id: number): Promise<I{pascal}>;

  /**
   * Check if a {normal} exists by ID.
   * @param id - ID of the {normal}
   * @throws Exception if the {normal} does not exist
   */
  checkExistanceOrFail(id: number): Promise<void>;

  /**
   * Update a {normal}.
   * @param id - ID of the {normal}
   * @param data - {normal} data
   * @returns {pascal} resource
   */
  update(id: number, data: Update{pascal}Dto): Promise<I{pascal}>;

  /**
   * Delete a {normal} by ID.
   * @param id - ID of the {normal}
   */
  remove(id: number): Promise<void>;
}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))


def create_ires_file(name, attr_map):
    text = 'export interface ICreate{capital} {{\n'.format(capital=to_pascal_case(name))
    for attr_name in attr_map:
        text += '{key}:{value};\n'.format(key=to_camel_case(attr_name), value=attr_map[attr_name])
    text += '''}}

export interface I{pascal} extends ICreate{pascal} {{
  id: number;
  createdAt: Date;
  updatedAt: Date;
}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        )
    filename = os.path.join(base_path, '{name}/interfaces/{name}.interface.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write(text)


def create_entity_file(name, attr_map):
    text = '''import {{
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
}} from 'typeorm';

import {{ I{pascal} }} from '../interfaces/{kebab}.interface';

@Entity({{ name: '{snake_plural}' }})
export class {pascal} implements I{pascal} {{
  @PrimaryGeneratedColumn()
  id: number;
'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            snake_plural=to_snake_case(pluralize(name)),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        )

    for attr_name in attr_map:
        additional = ''
        if attr_name.endswith('?'):
            additional += ', nullable: true'
        text += '''
  @Column({{ name: '{snake}'{additional} }})
  {name}: {value}
'''.format(name=to_camel_case(attr_name), snake=to_snake_case(attr_name.replace('?','')), additional=additional, value=attr_map[attr_name])

    text += '''  
  @CreateDateColumn({ name: 'created_at', type: 'timestamptz' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at', type: 'timestamptz' })
  updatedAt: Date;
}'''
    filename = os.path.join(base_path, '{name}/entities/{name}.entity.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write(text)


def create_create_dto_file(name):
    filename = os.path.join(base_path, '{name}/dtos/create-{name}.dto.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ ICreate{pascal} }} from '../interfaces/{kebab}.interface';

export class Create{pascal}Dto implements ICreate{pascal} {{
}}'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            snake_plural=to_snake_case(pluralize(name)),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))


def create_update_dto_file(name):
    filename = os.path.join(base_path, '{name}/dtos/update-{name}.dto.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ PartialType }} from '@nestjs/swagger';

import {{ Create{pascal}Dto }} from './create-{kebab}.dto';

export class Update{pascal}Dto extends PartialType(Create{pascal}Dto) {{}}
'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            snake_plural=to_snake_case(pluralize(name)),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))


def create_response_file(name, attr_map):
    text = '''import {{ I{pascal} }} from '../interfaces/{kebab}.interface';

export class {pascal}Response implements I{pascal} {{
  id: number;
'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            snake_plural=to_snake_case(pluralize(name)),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        )

    for attr_name in attr_map:
        text += '''
  {name}: {value};
'''.format(name=to_camel_case(attr_name), value=attr_map[attr_name])

    text += '''  
  createdAt: Date;

  updatedAt: Date;
}'''
    filename = os.path.join(base_path, '{name}/responses/{name}.response.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write(text)


def create_paginated_response_file(name):
    filename = os.path.join(base_path, '{name}/responses/{name}.paginated.response.ts'.format(name=name))
    with open(filename, 'w') as file:
        file.write('''import {{ ApiProperty }} from '@nestjs/swagger';

import {{ PaginationModel }} from 'src/common/pagination/paginaton.model';

import {{ {pascal}Response }} from './{kebab}.response';

export class Paginated{pascal}Response extends PaginationModel<{pascal}Response> {{
  @ApiProperty({{ type: [{pascal}Response] }})
  items: {pascal}Response[];
}}
'''.format(
            normal=to_normal_case(name), 
            normal_capital=to_normal_case(name.capitalize()), 
            camel=to_camel_case(name), 
            camel_plural=to_camel_case(pluralize(name)),
            pascal=to_pascal_case(name),
            plural_kebab=pluralize(name),
            snake=to_snake_case(name),
            snake_plural=to_snake_case(pluralize(name)),
            plural_normal=to_normal_case(pluralize(name)),
            plural_capitalized=to_normal_case(pluralize(name.capitalize())),
            kebab=name
        ))


parser = argparse.ArgumentParser(prog='ResGen',description='gens res',)

parser.add_argument('modname')
parser.add_argument('attributes')
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('-c', '--controller', action='store_true')
parser.add_argument('-s', '--service', action='store_true')

args = parser.parse_args()
curr_dir = os.getcwd()
base_path = os.path.join(curr_dir, 'src/modules')
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

