InitialTadeedAlgoOptin
==========================
Python pydantic class corresponding to  json type ```initial.tadeed.algo.optin```.

.. autoclass:: gnf.types.InitialTadeedAlgoOptin
    :members:

**TerminalAssetAlias**:
    - Description: The GNodeAlias of the TerminalAsset
    - Format: LeftRightDot

**TaOwnerAddr**:
    - Description: The Algorand address of the owner for the TerminalAsset
    - Format: AlgoAddressStringFormat

**ValidatorAddr**:
    - Description: Address of the TaValidator. The Algorand address of the TaValidator who has validated the location, device type, and power metering of the TerminalAsset.
    - Format: AlgoAddressStringFormat

**SignedInitialDaemonFundingTxn**:
    - Description: . Funding transaction for the TaDaemon account, signed by the TaOwner.
    - Format: AlgoMsgPackEncoded

.. autoclass:: gnf.types.initial_tadeed_algo_optin.check_is_left_right_dot
    :members:


.. autoclass:: gnf.types.initial_tadeed_algo_optin.check_is_algo_address_string_format
    :members:


.. autoclass:: gnf.types.initial_tadeed_algo_optin.check_is_algo_msg_pack_encoded
    :members:


.. autoclass:: gnf.types.InitialTadeedAlgoOptin_Maker
    :members:
