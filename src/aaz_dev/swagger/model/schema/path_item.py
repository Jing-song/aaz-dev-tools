from schematics.models import Model
from schematics.types import ModelType, ListType, DictType
from .operation import Operation
from .parameter import ParameterField, ParameterBase
from .reference import Linkable, Reference


class PathItem(Model, Linkable):
    """Describes the operations available on a single path. A Path Item may be empty, due to ACL constraints. The path itself is still exposed to the documentation viewer but they will not know which operations and parameters are available"""

    get = ModelType(Operation)  # A definition of a GET operation on this path.
    post = ModelType(Operation)  # A definition of a POST operation on this path.
    put = ModelType(Operation)  # A definition of a PUT operation on this path.
    patch = ModelType(Operation)  # A definition of a PATCH operation on this path.
    delete = ModelType(Operation)  # A definition of a DELETE operation on this path.
    head = ModelType(Operation)  # A definition of a HEAD operation on this path.

    parameters = ListType(ParameterField(support_reference=True))  # A list of parameters that are applicable for all the operations described under this path. These parameters can be overridden at the operation level, but cannot be removed there. The list MUST NOT include duplicated parameters. A unique parameter is defined by a combination of a name and location. The list can use the Reference Object to link to parameters that are defined at the Swagger Object's parameters. There can be one "body" parameter at most.

    # ignored because it is not used
    # options = ModelType(Operation)  # A definition of a OPTIONS operation on this path.
    # ref = ReferenceType()  # Allows for an external definition of this path item. The referenced structure MUST be in the format of a Path Item Object. If there are conflicts between the referenced definition and this Path Item's definition, the behavior is undefined.

    def link(self, swagger_loader, *traces, **kwargs):
        if self.is_linked():
            return
        super().link(swagger_loader, *traces)

        if self.parameters is not None:
            for idx, param in enumerate(self.parameters):
                if isinstance(param, Linkable):
                    param.link(swagger_loader, *self.traces, 'parameters', idx)

            # replace parameter reference by parameter instance
            for idx in range(len(self.parameters)):
                param = self.parameters[idx]
                while isinstance(param, Reference):
                    param = param.ref_instance
                assert isinstance(param, ParameterBase)
                self.parameters[idx] = param

        link_operation_ids = kwargs.get('link_operation_ids', None)
        if self.get is not None and (not link_operation_ids or self.get.operation_id in link_operation_ids):
            self.get.link(swagger_loader, *self.traces, 'get')
        if self.put is not None and (not link_operation_ids or self.put.operation_id in link_operation_ids):
            self.put.link(swagger_loader, *self.traces, 'put')
        if self.post is not None and (not link_operation_ids or self.post.operation_id in link_operation_ids):
            self.post.link(swagger_loader, *self.traces, 'post')
        if self.delete is not None and (not link_operation_ids or self.delete.operation_id in link_operation_ids):
            self.delete.link(swagger_loader, *self.traces, 'delete')
        if self.head is not None and (not link_operation_ids or self.head.operation_id in link_operation_ids):
            self.head.link(swagger_loader, *self.traces, 'head')
        if self.patch is not None and (not link_operation_ids or self.patch.operation_id in link_operation_ids):
            self.patch.link(swagger_loader, *self.traces, 'patch')

    def link_examples(self, swagger_loader, operation_ids, *traces):
        super().link(swagger_loader, *traces)

        if self.get is not None and self.get.operation_id in operation_ids:
            self.get.link_examples(swagger_loader, *self.traces, "get")
        if self.put is not None and self.put.operation_id in operation_ids:
            self.put.link_examples(swagger_loader, *self.traces, "put")
        if self.post is not None and self.post.operation_id in operation_ids:
            self.post.link_examples(swagger_loader, *self.traces, "post")
        if self.delete is not None and self.delete.operation_id in operation_ids:
            self.delete.link_examples(swagger_loader, *self.traces, "delete")
        if self.head is not None and self.head.operation_id in operation_ids:
            self.head.link_examples(swagger_loader, *self.traces, "head")
        if self.patch is not None and self.patch.operation_id in operation_ids:
            self.patch.link_examples(swagger_loader, *self.traces, "patch")

    def to_cmd(self, builder, **kwargs):
        op = getattr(self, builder.method, None)
        if op is None:
            return None
        assert isinstance(op, Operation)
        cmd_op = builder(op, parent_parameters=self.parameters)
        return cmd_op


class PathsField(DictType):

    def __init__(self, **kwargs):
        super(PathsField, self).__init__(
            ModelType(PathItem),
            **kwargs
        )


class XmsPathsField(DictType):

    """
    OpenAPI 2.0 has a built-in limitation on paths. Only one operation can be mapped to a path and http method. There are some APIs, however, where multiple distinct operations are mapped to the same path and same http method. For example GET /mypath/query-drive?op=file and GET /mypath/query-drive?op=folder may return two different model types (stream in the first example and JSON model representing Folder in the second). Since OpenAPI does not treat query parameters as part of the path the above 2 operations may not co-exist in the standard "paths" element.

    To overcome this limitation an "x-ms-paths" extension was introduced parallel to "paths". URLs under "x-ms-paths" are allowed to have query parameters for disambiguation, however they are not actually used.

    https://github.com/Azure/autorest/tree/main/docs/extensions#x-ms-paths
    """

    def __init__(self, **kwargs):
        super(XmsPathsField, self).__init__(
            ModelType(PathItem),
            serialized_name="x-ms-paths",
            deserialize_from="x-ms-paths",
            **kwargs
        )

