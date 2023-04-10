from utils.reference import AbstractBaseModel, AbstractCreateAtModel, fields


class Configure(AbstractBaseModel):
    name = fields.CharField(max_length=20, null=False, unique=True, description="配置名")
    value = fields.TextField()
    active = fields.BooleanField(default=True, description="启用?")


class Service(AbstractBaseModel):
    name = fields.CharField(max_length=20, unique=True, null=False, description="服务名")
    alias = fields.CharField(max_length=30, description="别名")
    description = fields.TextField(description="描述", null=True)
    repository = fields.CharField(max_length=255, null=False, description="代码仓库")
    container_name = fields.CharField(max_length=20, unique=True, null=False, description="容器名")
    container_id = fields.CharField(max_length=20, unique=True, null=True, description="运行中的容器ID")


class History(AbstractCreateAtModel):
    service = fields.ForeignKeyField("models.Service", description="关联服务")
    version = fields.CharField(max_length=20, description="版本号")
    published = fields.BooleanField(description="发布?", default=False)
