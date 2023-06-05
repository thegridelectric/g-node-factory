BasegnodeScadaCreate
==========================
Python pydantic class corresponding to  json type ```basegnode.scada.create```.

.. autoclass:: gnf.types.BasegnodeScadaCreate
    :members:

**TaAlias**:
    - Description: TerminalAsset Alias. GNodeAlias of the TerminalAsset that will be controlled by the new SCADA GNode. The SCADA GNodeAlias will have '.scada' appended to this.
    - Format: LeftRightDot

**ScadaAddr**:
    - Description: Algorand address for the SCADA. The TaOwner makes the corresponding private key, puts it on the SCADA device, and then sends this address to the GNodeFactory.
    - Format: AlgoAddressStringFormat

**TaDaemonAddr**:
    - Description: Algorand address of the associated TaDaemon. The TaDaemonAddr will have the TaDeed, and can be used to verify the public address of the TaOwner
    - Format: AlgoAddressStringFormat

**GNodeRegistryAddr**:
    - Description: GNodeRegistry Algorand address. The GNodeRegistry that contains Make/Model information about the SCADA and TerminalAsset
    - Format: AlgoAddressStringFormat

**SignedProof**:
    - Description: Recent transaction signed by the TaOwner. These will be replaced by composite transactions in next gen code.
    - Format: AlgoMsgPackEncoded

.. autoclass:: gnf.types.basegnode_scada_create.check_is_left_right_dot
    :members:


.. autoclass:: gnf.types.basegnode_scada_create.check_is_algo_address_string_format
    :members:


.. autoclass:: gnf.types.basegnode_scada_create.check_is_algo_msg_pack_encoded
    :members:


.. autoclass:: gnf.types.BasegnodeScadaCreate_Maker
    :members:
