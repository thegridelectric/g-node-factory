from pyteal import *


def approval_program():
    # Set this consts
    # GNodeFactoryAdminAddress (use "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI")
    # TaValidatorAddress (use "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII")
    # TaOwnerAddress (use "GSXFQJJHSZROXTK262SBGWR6OAO7KC6QQRQWRHYAIHS3KQ4VEXZ5L3DPTY")

    # seller == owner == TaOwner

    gnode_factory_admin_address_key = Bytes("gnode_factory_admin_address")  # target
    ta_validator_address_key = Bytes("ta_validator_address")  # funder
    ta_owner_address_key = Bytes("ta_owner_address")  # owner
    deed_id_key = Bytes("deed_id")

    op_setup = Bytes("setup")
    op_transfer_deed_back = Bytes("transfer")

    on_create = Seq(
        Assert(Txn.application_args.length() == Int(4)),

        App.globalPut(gnode_factory_admin_address_key, Txn.application_args[0]),
        App.globalPut(ta_validator_address_key, Txn.application_args[1]),
        App.globalPut(ta_owner_address_key, Txn.application_args[2]),
        App.globalPut(deed_id_key, Btoi(Txn.application_args[3])),
        Approve()
    )

    on_setup_opt_in_to_receive_deed = Seq(
        Assert(Txn.assets[0] == App.globalGet(deed_id_key)),

        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Txn.assets[0],
                TxnField.asset_receiver: Global.current_application_address(),
                TxnField.asset_amount: Int(0),
            }
        ),
        InnerTxnBuilder.Submit(),
        Approve(),
    )

    transfer_deed = Seq(
        # Assert(Txn.assets[0] == App.globalGet(deed_id_key)),
        # Assert(Txn.accounts[0] == App.globalGet(gnode_factory_admin_address_key)),

        # https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/#asset-transfer
        # Assert(
        #     App.globalGet(gnode_factory_admin_address_key) == Txn.application_args[1]
        # ),
        InnerTxnBuilder.Begin(),

        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.sender: Global.current_application_address(),
            TxnField.xfer_asset: Txn.assets[0],
            TxnField.asset_receiver: Txn.sender(),
            TxnField.asset_amount: Int(1),
        }),

        InnerTxnBuilder.Submit(),
        Approve()
    )

    on_call_method = Txn.application_args[0]
    no_op = Cond(
        [on_call_method == op_setup, on_setup_opt_in_to_receive_deed],
        [on_call_method == op_transfer_deed_back, transfer_deed],
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, no_op],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
    )

    return program


def clear_state_program():
    return Approve()


if __name__ == "__main__":
    with open("approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)
