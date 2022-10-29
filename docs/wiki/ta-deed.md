TerminalAssetDeed (`taDeed` )

---

This is an NFT establishing ownership rights of a [TerminalAsset](terminal-asset.md).

![alt_text](img/terminal-asset-deed-icon.png)

Placement of this deed in the 2-sig, 3-owner multi account [GnfAdmin, TaOwnerSmartDaemon, TaOwner] (call this `taMulti`) is a prerequiste for the GNodeFactory to change the TerminalAsset GNodeStatus from Pending to Active.

Funding that `taMulti` account with 100 Algos is a prerequisite for receiving the `taDeed`. The intention is for this to be the beginning of financial assurance once an agent is actively transacting in electricity markets on behalf of the `TerminalAsset`. The final size of that financial assurance will be determined by
the counterparties of the market transactions. It will scale with the typical monthly energy transaction size
of the asset.

A prerequisite for creation of the `taDeed` is that a third party Validator attests to the accuracy of the following information:
_ Physical location of the TerminalAsset device and meter as provided by the taOwner (lat/lon)
_ The TerminalAsset electricity meter is accurate ()
_ The meter is measuring the TerminalAsset and nothing else
_ The `parent` GNode - as determined by the GNodeAlias - exists in the `GNodeFactory` \* There are no known GNodes that exist on the copper GNode spanning tree _between_ the parent
and the TerminalAsset (Be more explicit)

The chosen validator must have a ValidatorAddress, and the joint account [GnfAdmin, Validator] (`multiValidator`) must
have a `ValidatorCerticate` NFT. Anyone may become a Validator through the ValidatorCertification process. The `ValidatorCertifcate` provides public accountability of the Validator and includes a web page. This
way, potential counterparties for energy transactions with the `TerminalAsset` can evaluate how confident
they are of the location and metering of the `TerminalAsset` by examining what entity validated their
`taDeed`.

The `taDeed` is _created_ by the `multiValidator` account.
