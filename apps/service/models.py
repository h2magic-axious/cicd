import enum

from utils.reference import AbstractBaseModel, AbstractCreateAtModel, fields


class Service(AbstractBaseModel):
    name = fields.CharField(max_length=20, unique=True, null=False, description="服务名")
    alias = fields.CharField(max_length=30, description="别名")
    description = fields.TextField(description="描述", null=True)
    repository = fields.CharField(max_length=255, null=False, description="代码仓库")
    container_id = fields.CharField(max_length=64, unique=True, null=True, description="运行中的容器ID")

    def __str__(self):
        return f"{self.name}"


class History(AbstractCreateAtModel):
    service = fields.ForeignKeyField("models.Service", description="关联服务")
    version = fields.CharField(max_length=20, description="版本号")
    image_id = fields.CharField(max_length=64, description="", null=True)
    running = fields.BooleanField(description="运行?", default=False)
    description = fields.TextField(description="版本描述", null=True)


class ContainerConfigure(AbstractBaseModel):
    service = fields.ForeignKeyField("models.Service", description="关联服务")

    class CType(enum.IntEnum):
        PORT = 1
        ENVIRONMENT = 2
        VOLUMNE = 3
    
    configure_type = fields.IntEnumField(CType)
    value = fields.CharField(max_length=255, null=False)
