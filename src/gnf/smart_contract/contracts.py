from pyteal import *


def approval_program():
    # Set this consts
    # GNodeFactoryAdminAddress (use "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI")
    # TaValidatorAddress (use "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII")
    # TaOwnerAddress (use "GSXFQJJHSZROXTK262SBGWR6OAO7KC6QQRQWRHYAIHS3KQ4VEXZ5L3DPTY")

    # TODO Txn.sender() who it is in terms of the above

    gnode_factory_admin_address_key = Bytes("gnode_factory_admin_address")
    ta_validator_address_key = Bytes("ta_validator_address")
    ta_owner_address_key = Bytes("ta_owner_address")
    asset_creator_address_key = Bytes("asset_creator_address")
    asset_index_key = Bytes("asset_index")

    op_transfer_deed_back = Bytes("transfer_deed_back")
    op_initial_deed_opt_in = Bytes("initial_deed_opt_in")
    op_new_deed_opt_in = Bytes("new_deed_opt_in")

    on_create = Seq(
        App.globalPut(gnode_factory_admin_address_key, Txn.application_args[1]),
        App.globalPut(ta_validator_address_key, Txn.application_args[2]),
        App.globalPut(ta_owner_address_key, Txn.application_args[3]),
        Approve()
    )

    initial_deed_opt_in = Seq(
        Assert(
            And(
               App.globalGet(ta_validator_address_key) == Txn.application_args[1],
               App.globalGet(ta_owner_address_key) == Txn.application_args[2],
            )
        ),
        App.globalPut(asset_index_key, Txn.application_args[3]),
        Approve()
    )

    new_deed_opt_in = Seq(
        Assert(
            App.globalGet(gnode_factory_admin_address_key) == Txn.application_args[2],
        ),
        Approve()
    )

    on_opt_in = Cond(
        [Txn.application_args[0] == op_initial_deed_opt_in, initial_deed_opt_in],
        [Txn.application_args[0] == op_new_deed_opt_in, new_deed_opt_in],
    )

    transfer_deed_back = Seq(
        Approve()  # TODO Implement
    )

    no_op = Cond(
        [Txn.application_args[0] == op_transfer_deed_back, transfer_deed_back],
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.OptIn, on_opt_in],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.NoOp, no_op],
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
