from pydantic import BaseModel, create_model, ConfigDict, PrivateAttr
import logging
from typing import Literal, ClassVar

logger = logging.getLogger(__name__)

class AuthorMetadata:
    author: str = ""
    email: str = ""

class VersionMetadata(AuthorMetadata):
    version: str = ""
    tag: str = ""

class Component(BaseModel, VersionMetadata):
    model_config = ConfigDict(defer_build=True)

    name: str = "Component"
    description: str = "A generic component"
    owner: str = "unknown"
    status: Literal["current", "target"] = "current"

    field_a: str = "value_a"
    field_b: int = 42

    _private_a: int = PrivateAttr(1)
    _private_b: int = PrivateAttr(2)
    _private_c: int = PrivateAttr(3)
    _private_d: int = PrivateAttr(4)
    _private_e: int = PrivateAttr(5)

    class_var_a: ClassVar[str] = "a"
    class_var_b: ClassVar[str] = "b"
    class_var_c: ClassVar[str] = "c"
    class_var_d: ClassVar[str] = "d"
    class_var_e: ClassVar[str] = "d"

class Container(Component):
    name: str = "container"
    description: str = "A docker container"
    owner: str = "devops_team"

class CloudContainer(Container):
    name: str = "cloud_container"
    description: str = "A cloud docker container"
    owner: str = "cloud_team"

class AWSCloudContainer(CloudContainer):
    name: str = "aws_cloud_container"
    description: str = "An AWS cloud docker container"
    owner: str = "aws_team"

    status: Literal["current", "target"] = "target"

def generate_subclasses(n: int):
    subclasses = []
    logger.info(f'Starting generation of {n} subclasses')
    for i in range(n):
        class_name = f'DynamicModel{i}'
        subclasses.append(create_model(class_name, __base__=AWSCloudContainer))
    logger.info(f'Generated {n} subclasses')

    test_instance = subclasses[1]()
    logger.info("DynamicModel0.__mro__=%s", subclasses[0].__mro__)
    logger.info("DynamicModel0.__bases__=%s", subclasses[0].__bases__)

    # Test values are correct
    assert isinstance(test_instance, AWSCloudContainer)
    assert test_instance.name == "aws_cloud_container"
    assert test_instance.owner == "aws_team"
    assert test_instance.status == "target"
    assert test_instance.field_a == "value_a"
    assert test_instance.field_b == 42
    assert test_instance.author == ""
    assert test_instance.class_var_a == "a"
    assert test_instance._private_a == 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
    generate_subclasses(10000)

