import logging
import os

import django

import gnf.config as config
from gnf.enums import CoreGNodeRole
from gnf.enums import GNodeStatus
from gnf.utils import camel_to_snake


PendingStatus = GNodeStatus.Pending
OtherRole = CoreGNodeRole.Other

gnr_addr = config.SandboxDemo().gnr_addr

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_related.settings")
django.setup()
logging.basicConfig(level="DEBUG")

from gnf.django_related import BaseGNodeDb


def main():
    gn = {
        "GNodeId": "7b1df82e-10c5-49d9-8d02-1e837e31b87e",
        "Alias": "d1",
        "StatusValue": GNodeStatus.Pending.value,
        "RoleValue": OtherRole.value,
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    root = BaseGNodeDb.objects.create(**d)

    root.status_value = GNodeStatus.Active.value
    root.save()

    gn = {
        "GNodeId": "c0119953-a48f-495d-87cc-58fb92eb4cee",
        "Alias": "d1.isone",
        "StatusValue": GNodeStatus.Pending.value,
        "RoleValue": CoreGNodeRole.ConductorTopologyNode,
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    isone = BaseGNodeDb.objects.create(**d)
    isone.status_value = GNodeStatus.Active.value
    isone.save()

    gn = {
        "GNodeId": "b572d571-22cf-4157-8c0f-33e9724d684f",
        "Alias": "d1.isone.ver",
        "StatusValue": GNodeStatus.value,
        "RoleValue": CoreGNodeRole.ConductorTopologyNode.value,
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    versant = BaseGNodeDb.objects.create(**d)
    versant.status_value = GNodeStatus.Active.value
    versant.save()

    gn = {
        "GNodeId": "575f374f-8533-4733-baf7-91146c607445",
        "Alias": "d1.isone.ver.keene",
        "StatusValue": GNodeStatus.Pending.value,
        "RoleValue": CoreGNodeRole.ConductorTopologyNode.value,
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]

    keene_rd = BaseGNodeDb.objects.create(**d)
    keene_rd.status_value = GNodeStatus.Active.value
    keene_rd.save()

    gn = {
        "GNodeId": "7d982442-d0ca-48d2-9b51-21f87229b708",
        "Alias": "d1.isone.ver.keene.pwrs",
        "StatusValue": GNodeStatus.value,
        "RoleValue": CoreGNodeRole.ConductorTopologyNode.value,
        "GNodeRegistryAddr": gnr_addr,
        "TypeName": "g.node.gt.100",
    }
    d = {camel_to_snake(k): v for k, v in gn.items()}
    del d["type_name"]
