import enum

from utils.reference import AbstractBaseModel, AbstractCreateAtModel, fields


class Configure(AbstractBaseModel):
    name = fields.CharField(max_length=20, null=False, unique=True, description="配置名")

    class DataType(str, enum.Enum):
        STRING = "string"
        INT = "int"
        FLOAT = "float"
        BOOL = "bool"

    data_type = fields.CharEnumField(DataType, max_length=6, description="数据类型")
    value = fields.TextField()
    active = fields.BooleanField(default=True, description="启用?")

    @property
    def real_value(self):
        match self.data_type.value:
            case self.DataType.INT:
                return int(self.value)
            case self.DataType.FLOAT:
                return float(self.value)
            case self.DataType.BOOL:
                return self.value == "yes"
            case _:
                return self.value


class Service(AbstractBaseModel):
    name = fields.CharField(max_length=20, unique=True, null=False, description="服务名")
    alias = fields.CharField(max_length=30, description="别名")
    description = fields.TextField(description="描述", null=True)
    repository = fields.CharField(max_length=255, null=False, description="代码仓库")
    container_name = fields.CharField(max_length=20, unique=True, null=False, description="容器名")


class History(AbstractCreateAtModel):
    service = fields.ForeignKeyField("models.Service", description="关联服务")
    version = fields.CharField(max_length=20, description="版本号")
    published = fields.BooleanField(description="发布?", default=False)
