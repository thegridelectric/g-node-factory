TavalidatorcertAlgoTransfer
==========================
Python pydantic class corresponding to  json type ```tavalidatorcert.algo.transfer```.

.. autoclass:: gnf.types.TavalidatorcertAlgoTransfer
    :members:

**ValidatorAddr**:
    - Description: The address of the pending TaValidator
    - Format: AlgoAddressStringFormat

**HalfSignedCertTransferMtx**:
    - Description: Algo multi-transaction for certificate transfer, with 1 of 2 signatures
    - Format: AlgoMsgPackEncoded

.. autoclass:: gnf.types.tavalidatorcert_algo_transfer.check_is_algo_address_string_format
    :members:


.. autoclass:: gnf.types.tavalidatorcert_algo_transfer.check_is_algo_msg_pack_encoded
    :members:


.. autoclass:: gnf.types.TavalidatorcertAlgoTransfer_Maker
    :members:
