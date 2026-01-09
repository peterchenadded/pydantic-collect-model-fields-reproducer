from pydantic import BaseModel, create_model, ConfigDict
import logging
from typing import Literal

logger = logging.getLogger(__name__)

class Component(BaseModel):
    model_config = ConfigDict(defer_build=True)

    name: str = "Component"
    description: str = "A generic component"
    owner: str = "unknown"
    status: Literal["current", "target"] = "current"

    field_a: str = "value_a"
    field_b: int = 42

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
    assert isinstance(test_instance, AWSCloudContainer)
    assert test_instance.name == "aws_cloud_container"
    assert test_instance.owner == "aws_team"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
    generate_subclasses(10000)

