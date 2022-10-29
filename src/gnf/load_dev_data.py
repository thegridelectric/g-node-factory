import json
import logging
import os
import time

import config
import django
from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap
from enums.g_node_status_map import GNodeStatus
from enums.g_node_status_map import GNodeStatusMap
from utils import camel_to_snake


PendingStatus = GNodeStatus.PENDING
OtherRole = CoreGNodeRole.OTHER
GNodeStatusMap.local_to_type(PendingStatus)
gnr_addr = config.SandboxDemo().gnr_addr
from data_classes.base_g_node import BaseGNode


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_related.settings")
django.setup()
logging.basicConfig(level="DEBUG")

from django_related.models import BaseGNodeDb


def main():
    gn = {
        "GNodeId": "7b1df82e-10c5-49d9-8d02-1e837e31b87e",
        "Alias": "d1",
        "StatusValue": GNodeStatusMap.local_to_type(GNodeStatus.PENDING),
        "RoleValue": CoreGNodeRoleMap.local_to_type(OtherRole),
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    root = BaseGNodeDb.objects.create(**d)

    root.status_value = GNodeStatusMap.local_to_type(GNodeStatus.ACTIVE)
    root.save()

    gn = {
        "GNodeId": "c0119953-a48f-495d-87cc-58fb92eb4cee",
        "Alias": "d1.isone",
        "StatusValue": GNodeStatusMap.local_to_type(GNodeStatus.PENDING),
        "RoleValue": CoreGNodeRoleMap.local_to_type(
            CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE
        ),
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    isone = BaseGNodeDb.objects.create(**d)
    isone.status_value = GNodeStatusMap.local_to_type(GNodeStatus.ACTIVE)
    isone.save()

    gn = {
        "GNodeId": "b572d571-22cf-4157-8c0f-33e9724d684f",
        "Alias": "d1.isone.ver",
        "StatusValue": GNodeStatusMap.local_to_type(GNodeStatus.PENDING),
        "RoleValue": CoreGNodeRoleMap.local_to_type(
            CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE
        ),
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    versant = BaseGNodeDb.objects.create(**d)
    versant.status_value = GNodeStatusMap.local_to_type(GNodeStatus.ACTIVE)
    versant.save()

    gn = {
        "GNodeId": "575f374f-8533-4733-baf7-91146c607445",
        "Alias": "d1.isone.ver.keene",
        "StatusValue": GNodeStatusMap.local_to_type(GNodeStatus.PENDING),
        "RoleValue": CoreGNodeRoleMap.local_to_type(
            CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE
        ),
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    keene_rd = BaseGNodeDb.objects.create(**d)
    keene_rd.status_value = GNodeStatusMap.local_to_type(GNodeStatus.ACTIVE)
    keene_rd.save()

    gn = {
        "GNodeId": "7d982442-d0ca-48d2-9b51-21f87229b708",
        "Alias": "d1.isone.ver.keene.pwrs",
        "StatusValue": GNodeStatusMap.local_to_type(GNodeStatus.PENDING),
        "RoleValue": CoreGNodeRoleMap.local_to_type(
            CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE
        ),
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]
