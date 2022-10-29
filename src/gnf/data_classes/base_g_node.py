""" BaseGNode Base Class Definition """
import logging
from typing import Dict
from typing import List
from typing import Optional

import property_format
from data_classes.gps_point import GpsPoint
from data_classes.mixin import StreamlinedSerializerMixin
from enums.core_g_node_role_map import CoreGNodeRole
from enums.core_g_node_role_map import CoreGNodeRoleMap
from enums.g_node_status_map import GNodeStatus
from enums.g_node_status_map import GNodeStatusMap
from errors import DcError
from errors import SchemaError


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)


class BaseGNode(StreamlinedSerializerMixin):
    by_id: Dict[int, "BaseGNode"] = {}
    by_alias: Dict[str, "BaseGNode"] = {}

    def __new__(cls, g_node_id, *args, **kwargs):
        try:
            return cls.by_id[g_node_id]
        except KeyError:
            instance = super().__new__(cls)
            cls.by_id[g_node_id] = instance
            return instance

    def __init__(
        self,
        g_node_id: Optional[str] = None,
        alias: Optional[str] = None,
        prev_alias: Optional[str] = None,
        status_value: Optional[str] = None,
        role_value: Optional[str] = None,
        g_node_registry_addr: Optional[str] = None,
        ownership_deed_nft_id: Optional[int] = None,
        ownership_deed_validator_addr: Optional[str] = None,
        owner_addr: Optional[str] = None,
        daemon_addr: Optional[str] = None,
        trading_rights_nft_id: Optional[int] = None,
        gps_point_id: Optional[str] = None,
    ):
        self.g_node_id = g_node_id
        self.alias = alias
        self.prev_alias = prev_alias
        self.status = GNodeStatusMap.type_to_local(status_value)
        self.role = CoreGNodeRoleMap.type_to_local(role_value)
        self.g_node_registry_addr = g_node_registry_addr
        self.ownership_deed_nft_id = ownership_deed_nft_id
        self.ownership_deed_validator_addr = ownership_deed_validator_addr
        self.owner_addr = owner_addr
        self.daemon_addr = daemon_addr
        self.trading_rights_nft_id = trading_rights_nft_id
        self.gps_point_id = gps_point_id
        self.__class__.by_alias[self.alias] = self

    def __repr__(self):
        rs = f"GNode Alias: {self.alias}, Role: {self.role.value}, Status: {self.status.value}"
        if self.ownership_deed_nft_id and self.role == CoreGNodeRole.TERMINAL_ASSET:
            rs += f", TaDeedIdx: {self.ownership_deed_nft_id}"
        return rs

    def gps_point(self) -> Optional[GpsPoint]:
        if self.gps_point_id is None:
            return None
        return GpsPoint.by_id["gps_point_id"]

    def is_root(self) -> bool:
        alias_list = self.alias.split(".")
        alias_list.pop()
        if len(alias_list) == 0:
            return True
        return False

    def is_copper(self) -> bool:
        """Returns true if role is not other"""
        if self.role == CoreGNodeRole.OTHER:
            return False
        return True

    @classmethod
    def active_g_nodes(cls) -> List["BaseGNode"]:
        g_nodes = list(BaseGNode.by_alias.values())
        return list(filter(lambda x: x.status == GNodeStatus.ACTIVE, g_nodes))

    @classmethod
    def parent_from_alias(cls, alias: str) -> Optional["BaseGNode"]:
        """
        Returns:
            - BaseGNode. If the parent as suggested by the alias exists as an
            Active BaseGNode, returns that.
            - None. If alias is one word long (i.e. root of world)
        """
        alias_list = alias.split(".")
        alias_list.pop()
        parent_alias = ".".join(alias_list)
        if parent_alias in list(map(lambda x: x.alias, cls.active_g_nodes())):
            return BaseGNode.by_alias[parent_alias]
        return None

    def parent(self) -> Optional["BaseGNode"]:
        """
        Raises: DcError if "natural" parent (as suggested by alias) is not Active,
        and either
            - prev_alias is None, OR
            - the parent as suggested by prev_alias is not Active and/or
            does not exist.
        Returns:
            BaseGNode.   Parent BaseGNode
              - If the parent as suggested by the alias exists as an
            Active BaseGNode, returns that ("natural" parent)
              - Else, if the parent as suggested by the prev_alais exists
              as an active BaseGNode, returns that.
            None.
              - If alias is one word long (i.e. root of world)
        """
        if self.is_root():
            return None
        natural_parent = self.parent_from_alias(self.alias)
        if natural_parent is not None:
            return natural_parent

        # alias may point to incorrect parent if getting updated
        if self.prev_alias is None:
            raise DcError(f"error finding parent for {self.alias}!")

        parent_pending_alias_update = self.parent_from_alias(self.prev_alias)
        if parent_pending_alias_update is None:
            raise DcError(f"error finding parent for {self.alias}!")
        return parent_pending_alias_update

    def children(self) -> List["BaseGNode"]:
        """Returns the list of BaseGnodes identifying this node as parent"""
        return list(filter(lambda x: x.parent() == self, BaseGNode.by_alias.values()))

    ##########################
    # Object creation
    #########################

    @classmethod
    def check_creation_axioms(cls, attributes):
        cls._creation_axiom_1(attributes)
        cls._creation_axiom_2(attributes)
        cls._creation_axiom_3(attributes)
        cls._creation_axiom_4(attributes)
        cls._creation_axiom_5(attributes)
        cls._schema_axiom_1(attributes)
        cls._schema_axiom_2(attributes)
        cls._schema_axiom_3(attributes)
        cls._schema_axiom_4(attributes)
        cls._joint_axiom_1(attributes)
        cls._joint_axiom_2(attributes)

    @classmethod
    def _creation_axiom_1(cls, attributes):
        """Creation Axiom 1: alias cannot be used, now or previously, by this or
        other BaseGNodes"""
        # Done in models.py, as it requires access to BaseGNodeHistory

    @classmethod
    def _creation_axiom_2(cls, attributes):
        """Creation Axiom 2: g_node_id must be a unique string of UUID format"""
        g_node_id = attributes["g_node_id"]
        if g_node_id in cls.by_id.keys():
            raise DcError(f"g_node_id {attributes['g_node_id']} already in use")
        if not isinstance(g_node_id, str):
            raise DcError(f"g_node_id must be a string, got {type(g_node_id)}.")
        try:
            property_format.check_is_uuid_canonical_textual(g_node_id)
        except SchemaError:
            raise DcError(
                f"g_node_id must have format UuidCanonicalTextutal. Got {g_node_id}."
            )

    @classmethod
    def _creation_axiom_3(cls, attributes):
        """Creation Axiom 3: Initial Status must be Pending"""
        status = GNodeStatusMap.type_to_local(attributes["status_value"])
        if status != GNodeStatus.PENDING:
            raise DcError(
                f"Creation Axiom 3: Initial Status must be Pending. Got {status}"
            )

    @classmethod
    def _creation_axiom_4(cls, attributes):
        """Creation Axiom 4: On creation, PrevAlias is None"""
        prev_alias = attributes["prev_alias"]
        if prev_alias is not None:
            raise DcError(
                f"Creation Axiom 4: On creation, PrevAlias is None. Got {prev_alias}"
            )

    @classmethod
    def _creation_axiom_5(cls, attributes):
        """Creation Axiom 5: TOPOLOGY. Assume the Alias has at least two words.
        Then
          - EXISTENCE the parent GNode (from alias) must in the GNodeFactory, unless GNode is root.
          - STATUS
             - If status is NOT active, all children must be PermanentlyDeactivated.
          - ROLE
            - If role is Ctn or MarketMaker, the parent must be a root, or have either role Ctn or MarketMaker.
            - If the role is AtomicMeausurementNode or AtomicTNode, the parent must be either Ctn or MarketMaker.
            - If the role is TerminalAsset, the parent must be either AtomicMeasurementNode or AtomicTNode"""
        alias: str = attributes["alias"]
        if len(alias.split(".")) == 1:
            "remaining axioms all have to do with parent-child relationship"
            return

        role = CoreGNodeRoleMap.type_to_local(attributes["role_value"])
        status = GNodeStatusMap.type_to_local(attributes["status_value"])

        parent = cls.parent_from_alias(alias)
        if parent is None:
            raise DcError(f"Create Axiom 5: non-root {alias} must have Active parent!")
        if parent.status is GNodeStatus.PERMANENTLY_DEACTIVATED and not (
            status is GNodeStatus.PERMANENTLY_DEACTIVATED
        ):
            raise DcError(
                "Creation Axiom 5`: the parent of an PermanentlyDeactivated GNode must be PermanentlyDeactivated."
            )

        if (role is CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE) or (
            role is CoreGNodeRole.MARKET_MAKER
        ):
            if not (
                parent.is_root()
                or (parent.role is CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE)
                or (parent.role is CoreGNodeRole.MARKET_MAKER)
            ):
                raise DcError(
                    f"Creation Axiom 5`: the parent of a {role} must be ConductorTopologyNode"
                    f" or MarketMaker, not {parent.role}"
                )
        if (role is CoreGNodeRole.ATOMIC_METERING_NODE) or (
            role is CoreGNodeRole.ATOMIC_T_NODE
        ):
            if not (
                (parent.role is CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE)
                or (parent.role is CoreGNodeRole.MARKET_MAKER)
            ):
                raise DcError(
                    f"Creation Axiom 5 `: the parent of a {role} must be ConductorTopologyNode"
                    f" or MarketMaker, not {parent.role}"
                )
        if role is CoreGNodeRole.TERMINAL_ASSET:
            if not (
                (parent.role is CoreGNodeRole.ATOMIC_METERING_NODE)
                or (parent.role is CoreGNodeRole.ATOMIC_T_NODE)
            ):
                raise DcError(
                    f"Joint Axiom `: the parent of a {role} must be AtomicMete PringNode"
                    f" or AtomicTNode, not {parent.role}"
                )

    #########################################################
    # Schema axioms (shared with type)
    #########################################################

    @classmethod
    def _schema_axiom_1(cls, attributes: Dict):
        """Schema Axiom 1: The following attributes must exist: g_node_id,
        alias, status_value, role_value, g_node_registry_addr"""
        if "g_node_id" not in attributes.keys():
            raise DcError("g_node_id must exist")
        if "alias" not in attributes.keys():
            raise DcError("alias must exist")
        if "status_value" not in attributes.keys():
            raise DcError(f"status_value must exist for g node {attributes}")
        if "role_value" not in attributes.keys():
            raise DcError(f"role_value must exist for g node {attributes}")
        if "g_node_registry_addr" not in attributes.keys():
            raise DcError(f"g_node_registry_addr must exist for g node {attributes}")

    @classmethod
    def _schema_axiom_2(cls, attributes):
        """Schema Axiom 2: FORMATTING
        If they exist:
        - Alias must be a string of format LRD Alias
        - PrevAlias must be a string of format LRD Alias
        - GNodeId must be a string of format UuidCanoicalTextual
        - OwnershipDeedNftId must be an integer,
        - OwnershipDeedValidatorAddr must be a string of format AlgoAddressStringFormat
        - OwnerAddr must be a string of format AlgoAddressStringFormat
        - DaemonAddr must be a string of format AlgoAddressStringFormat
        - TradingRightsNftId must be an integer"""

        g_node_registry_addr = attributes["g_node_registry_addr"]
        ownership_deed_nft_id = attributes["ownership_deed_nft_id"]
        ownership_deed_validator_addr = attributes["ownership_deed_validator_addr"]
        owner_addr = attributes["owner_addr"]
        daemon_addr = attributes["daemon_addr"]
        trading_rights_nft_id = attributes["trading_rights_nft_id"]
        if ownership_deed_nft_id:
            if not isinstance(ownership_deed_nft_id, int):
                raise DcError("Schema Axiom 2: OwnershipDeedNftId must be an integer")
        if trading_rights_nft_id:
            if not isinstance(trading_rights_nft_id, int):
                raise DcError("Schema Axiom 2: TradingRightsNftId must be an integer ")
        for addr in [
            ownership_deed_validator_addr,
            owner_addr,
            daemon_addr,
            g_node_registry_addr,
        ]:
            if addr:
                if not isinstance(addr, str):
                    raise DcError(f"jSchema Axiom 2: {addr} must be a string")
                try:
                    property_format.check_is_algo_address_string_format(addr)
                except SchemaError as e:
                    raise DcError(
                        f"Schema Axiom 2: {addr} must have format AlgoAddressStringFormat"
                    )

    @classmethod
    def _schema_axiom_3(cls, attributes):
        """Schema Axiom 3: Assume OwnershipDeedNftId exists and role is TerminalAsset.
        The Nft must be for a Valid TaDeed created by the 2-sig [GnfAdmin, ownership_deed_validator_addr]
        multi whose asset_name is this GNodeAlias."""
        pass

    @classmethod
    def _schema_axiom_4(cls, attributes):
        """Schema Axiom 4: Assume role is TerminalAsset and status is Active. Then the OwnershipDeedNftId
        must exist, and must be owned by the 2-sig [GnfAdmin, smart_daemon_addr, owner_addr] multi"""
        pass

    #####################################
    # Joing axioms for creation or update
    #####################################

    @classmethod
    def _joint_axiom_1(cls, attributes):
        """Joint Axiom 1: There is at most one root GNode."""
        aliases = list(set(cls.by_alias.keys()).union({attributes["alias"]}))
        roots = list(filter(lambda x: len(x.split(".")) == 1, aliases))
        if len(roots) > 1:
            raise DcError(
                f"Joint Axiom 1: There is at most one root GNode. Already have {set(roots) -  {attributes['alias']} }"
            )

    @classmethod
    def _joint_axiom_2(cls, attributes):
        """Joint Axiom 2: If GpsPointId is not None, then  there is a GpsPoint in the
        GNodeFactory with that GpsPointId"""
        gps_point_id = attributes["gps_point_id"]
        pass
        if gps_point_id is not None:
            if gps_point_id not in GpsPoint.by_id.keys():
                raise DcError(
                    "Joint Axoim 2: If GpsPointId is not None, then it exists in the GpsPoints"
                    f"Got {gps_point_id} for {attributes['g_node_id']}"
                )

    ##########################
    # Object update
    ##########################

    def check_update_axioms(self, new_attributes):
        self._update_axiom_1(new_attributes)
        self._update_axiom_2(new_attributes)
        self._update_axiom_3(new_attributes)
        self._update_axiom_4(new_attributes)
        self._update_axiom_5(new_attributes)
        self._schema_axiom_1(new_attributes)
        self._schema_axiom_2(new_attributes)
        self._schema_axiom_3(new_attributes)
        self._schema_axiom_4(new_attributes)
        self._joint_axiom_1(new_attributes)
        self._joint_axiom_2(new_attributes)

    def _update_axiom_1(self, new_attributes):
        """Update Axiom 1: g_node_alias cannot be used, now or previously, by this or
        other BaseGNodes.
        """
        # Done in models.py, as it requires access to BaseGNodeHistory
        pass

    def _update_axiom_2(self, new_attributes):
        """Update Axiom 2: g_node_id is Immutable"""
        if self.g_node_id:
            if new_attributes["g_node_id"] != self.g_node_id:
                raise DcError(f"Update Axiom 1: g_node_id is Immutable.")

    def _update_axiom_3(self, new_attributes):
        """Update Axiom 3:  Status update rules:
        - Pending can only change to Active,
        - Active can only change to Suspended or PermanentlyDeactivated
        - Suspended can only change to Active or PermanentlyDeactivated
        - PermanentlyDeactivated cannot change."""
        new_status_value = new_attributes["status_value"]
        new_status = GNodeStatusMap.type_to_local(new_status_value)
        if self.status is GNodeStatus.PENDING:
            if not (
                (new_status is GNodeStatus.PENDING)
                or (new_status is GNodeStatus.ACTIVE)
            ):
                raise DcError(
                    f"Update Axiom 2: Pending can only change to Active, not {new_status}"
                )
        elif self.status is GNodeStatus.ACTIVE:
            if not (
                (new_status is GNodeStatus.ACTIVE)
                or (new_status is GNodeStatus.PERMANENTLY_DEACTIVATED)
                or (new_status is GNodeStatus.SUSPENDED)
            ):
                raise DcError(
                    f"Update Axiom 2: Active can only change to Suspended or PermanentlyDeactivated, not {new_status}"
                )
        elif self.status is GNodeStatus.SUSPENDED:
            if not (
                (new_status is GNodeStatus.ACTIVE)
                or (new_status is GNodeStatus.PERMANENTLY_DEACTIVATED)
                or (new_status is GNodeStatus.SUSPENDED)
            ):
                raise DcError(
                    f"Update Axiom 2: Suspended can only change to Active or PermanentlyDeactivated, not {new_status}"
                )
        elif self.status is GNodeStatus.PERMANENTLY_DEACTIVATED:
            if not (new_status is GNodeStatus.PERMANENTLY_DEACTIVATED):
                raise DcError(
                    f"Update Axiom 3: Permanently Deactivated status cannot change. Got {new_status}"
                )

    def _update_axiom_4(self, attributes):
        """Update Axiom 4: TOPOLOGY. Assume the Alias has at least two words.
        Then
          - EXISTENCE the parent GNode  must in the GNodeFactory, unless GNode is root.
          - STATUS
             - If status is NOT Active, all children must have status PermanentlyDeactivated
            - If role is Ctn or MarketMaker, the parent must be a root, or have either role Ctn or MarketMaker.
            - If the role is AtomicMeausurementNode or AtomicTNode, the parent must be either Ctn or MarketMaker.
            - If the role is TerminalAsset, the parent must be either AtomicMeasurementNode or AtomicTNode"""
        alias: str = attributes["alias"]
        role = CoreGNodeRoleMap.type_to_local(attributes["role_value"])
        status = GNodeStatusMap.type_to_local(attributes["status_value"])
        if len(alias.split(".")) == 1:
            is_root = True
        else:
            is_root = False

        # If status is NOT Active, all children must have status PermanentlyDeactivated
        # LOOKING UP AT PARENT
        if not is_root:
            parent = self.parent()
            if parent is None and self.status != GNodeStatus.PERMANENTLY_DEACTIVATED:
                raise DcError(
                    f"Update Axiom 4: non-root {alias} with status {self.status} must have Active parent!"
                )

        # LOOKING DOWN AT DESCENDANTS
        if status != GNodeStatus.ACTIVE:
            children_status_set = set(filter(lambda x: x.status, self.children()))
            if (
                children_status_set != {GNodeStatus.PERMANENTLY_DEACTIVATED}
                and children_status_set != set()
            ):
                raise DcError(
                    f"Cannot change role to {role} unless there are no children or "
                    f"children are all PermanentlyDeactivated. Children: {self.children()}"
                )

        if not is_root:
            if (role is CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE) or (
                role is CoreGNodeRole.MARKET_MAKER
            ):
                if not (
                    parent.is_root()
                    or (parent.role is CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE)
                    or (parent.role is CoreGNodeRole.MARKET_MAKER)
                ):
                    raise DcError(
                        f"Update Axiom 4`: the parent of a {role} must be ConductorTopologyNode"
                        f" or MarketMaker, not {parent.role}"
                    )
            if (role is CoreGNodeRole.ATOMIC_METERING_NODE) or (
                role is CoreGNodeRole.ATOMIC_T_NODE
            ):
                if not (
                    (parent.role is CoreGNodeRole.CONDUCTOR_TOPOLOGY_NODE)
                    or (parent.role is CoreGNodeRole.MARKET_MAKER)
                ):
                    raise DcError(
                        f"Update Axiom 4`: the parent of a {role} must be ConductorTopologyNode"
                        f" or MarketMaker, not {parent.role}"
                    )
            if role is CoreGNodeRole.TERMINAL_ASSET:
                if not (
                    (parent.role is CoreGNodeRole.ATOMIC_METERING_NODE)
                    or (parent.role is CoreGNodeRole.ATOMIC_T_NODE)
                ):
                    raise DcError(
                        f"Update Axiom 4`: the parent of a {role} must be AtomicMete PringNode"
                        f" or AtomicTNode, not {parent.role}"
                    )
        # LOOKING DOWN AT DESCENDANTS
        # Question: add the above again, or rely on role update axioms??
        # ... should probably add above again in case role update axioms change ...

    def _update_axiom_5(self, attributes):
        """Update Axiom 5: Role update rules.  TerminalAsset, InterconnectionComponent, and
        Other cannot change roles. ConductorTopologyNode can turn into MarketMaker and vice
        versa. AtomicMeteringNode can turn into AtomicTNode and vice versa"""
        pass

    def _update_axiom_6(self, attributes):
        """Update Axiom 6: If alias has changed, then new prev_alias must equal
        original alias prior to the change. If alias has NOT changed then new prev_alias
         must equal original prev_alias."""
        new_alias: str = attributes["alias"]
        prev_alias: str = attributes["prev_alias"]
        if new_alias != self.alias:
            if prev_alias != self.alias:
                raise DcError(
                    f"Update Axiom 6: If alias has changed, then new prev_alias "
                    "must equal original alias prior to the change."
                )
        else:
            if prev_alias != self.prev_alias:
                raise DcError(
                    f"Update Axiom 6: If alias has NOT changed then new "
                    "prev_alias must equal original prev_alias."
                )