# GNodeRoles

The GNodeFactory recognizes 7 `GNodeRoles`:

1. [AtomicMeteringNode](atomic-metering-node.md)
2. [AtomicTransactiveNode](atomic-transactive-node.md)
3. [ConductorTopologyNode](conductor-topology-node.md)
4. [InterconnectionComponent](interconnection-component.md)
5. [MarketMaker](market-maker.md)
6. [TerminalAsset](terminal-asset.md)
7. Other

The GNodeFactory is the authority on GNode creation and update, and the copper topology of the grid as specified by the the spanning tree articulated by the non-other GNodeRoles. A GNodeRegistry is expected to expand the `Other` category into additional roles, such as `AggregatedTransactiveNodes`.
