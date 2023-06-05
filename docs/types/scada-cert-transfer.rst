ScadaCertTransfer
==========================
Python pydantic class corresponding to  json type ```scada.cert.transfer```.

.. autoclass:: gnf.types.ScadaCertTransfer
    :members:

**TaAlias**:
    - Description: TerminalAsset Alias. GNodeAlias of the TerminalAsset for which the SCADA certificate is issued. The ScadaCert can be found from this.
    - Format: LeftRightDot

**SignedProof**:
    - Description: Signed Proof from the SCADA Actor. The Scada GNode has a ScadaAlgoAddr in the GNodeFactory database, and the identity of the SCADA actor can be verified by this.
    - Format: AlgoMsgPackEncoded

.. autoclass:: gnf.types.scada_cert_transfer.check_is_left_right_dot
    :members:


.. autoclass:: gnf.types.scada_cert_transfer.check_is_algo_msg_pack_encoded
    :members:


.. autoclass:: gnf.types.ScadaCertTransfer_Maker
    :members:
