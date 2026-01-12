from pydantic import BaseModel, Field
from typing import List, Optional, Callable
from pydantic.fields import FieldInfo
import copy
import pytest


class A(BaseModel):
    field: List[int] = Field(default_factory=list, description="description", alias="field", max_length=2)

test_field = A.model_fields['field']
test_range = 60_000

def custom_copy_using_init_and_attrs(field: FieldInfo) -> FieldInfo:
    new_field = FieldInfo()
    for slot in FieldInfo.__slots__:
        setattr(new_field, slot, getattr(field, slot))
    return new_field

def custom_copy_using_new_and_attrs(field: FieldInfo) -> FieldInfo:
    new_field = FieldInfo.__new__(FieldInfo)
    for slot in FieldInfo.__slots__:
        setattr(new_field, slot, getattr(field, slot))
    return new_field

def custom_copy_using_new_and_specific(field: FieldInfo) -> FieldInfo:
    new_field = FieldInfo.__new__(FieldInfo)
    new_field.annotation = field.annotation
    new_field.default = field.default
    new_field.default_factory = field.default_factory
    new_field.alias = field.alias
    new_field.alias_priority = field.alias_priority
    new_field.validation_alias = field.validation_alias
    new_field.serialization_alias = field.serialization_alias
    new_field.title = field.title
    new_field.field_title_generator = field.field_title_generator
    new_field.description = field.description
    new_field.examples = field.examples
    new_field.exclude = field.exclude
    new_field.exclude_if = field.exclude_if
    new_field.discriminator = field.discriminator
    new_field.deprecated = field.deprecated
    new_field.json_schema_extra = field.json_schema_extra
    new_field.frozen = field.frozen
    new_field.validate_default = field.validate_default
    new_field.repr = field.repr
    new_field.init = field.init
    new_field.init_var = field.init_var
    new_field.kw_only = field.kw_only
    new_field.metadata = field.metadata
    new_field._attributes_set = field._attributes_set
    new_field._qualifiers = field._qualifiers
    new_field._complete = field._complete
    new_field._original_assignment = field._original_assignment
    new_field._original_annotation = field._original_annotation

    return new_field

def check_field(field: FieldInfo):
    for name in FieldInfo.__slots__:
        assert getattr(field, name) == getattr(test_field, name)

class Scenario(BaseModel):
    id: str
    func: Callable[[FieldInfo], FieldInfo]

scenarios = [
    Scenario(id="copy.copy", func=copy.copy),
    Scenario(id="custom_copy_using_init_and_attrs", func=custom_copy_using_init_and_attrs),
    Scenario(id="custom_copy_using_new_and_attrs", func=custom_copy_using_new_and_attrs),
    Scenario(id="custom_copy_using_new_and_specific", func=custom_copy_using_new_and_specific),
]

@pytest.mark.parametrize("scenario", scenarios, ids=map(lambda x: x.id, scenarios))
def test_copy(scenario: Scenario):
    result : Optional[FieldInfo] = None
    for i in range(test_range):
        result = scenario.func(test_field)
    
    assert result
    check_field(result)

