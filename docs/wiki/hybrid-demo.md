# Hybrid Transactive Asset Demonstration

GridWorks is working with [Ridgeline Energy](https://ridgelineanalytics.com/) on a pilot demonstration project run by Efficiency Maine to install 5 space heating systems that use heat pumps coupled with thermal storage in Maine. If this first demonstration succeeds, the goal is to expand to hundreds of homes installed in an area of Maine where transmission constraints and wind projects are driving wholesale electricity prices negative in about 30% of hours during the winter months, and to demonstrate how transactive heat can reduce heating costs while simultaneously improving the economics of the constrained wind projects.

GridWorks and Ridgeline are building Demonstration SCADA Devices (DSDs) that will do the monitoring and control of these systems. The DSD has two components - a high voltage box with the various relays required for dispatch, and a low-voltage box with the brains and most of the sensing. The low-voltage box includes a raspberry Pi 4 with open-source code developed by GridWorks. This is still a work in progress, although a first DSD has been installed and is currently monitoring the power use of a heat pump hot water heater in Freedom Maine. The code running on the Pi is availabe at [this repo](https://github.com/thegridelectric/gw-scada-spaceheat-python). Jessica has done most of that coding work to date, although Andrew Schweitzer will be taking on an increasing role in the continued development effort for the SCADA.

The plan is to set up key components of the Gridworks Platform - including in particular the GNodeRegistry and the GNodeFactory - on Amazon instances. Instead of running on a private algo sandbox instance, this demonstration GNodeFactory will create NFTs on TestNet.

The 5 heating systems will be the `real` partipants in this demonstration. A pair of NFTs on testnet will be created for each of the 5 homeowners - the `Terminal Asset Deed`

![alt_text](img/terminal-asset-deed-icon.png)

which is the token attesting to the fact that the homeowner owns a specific type of heating system with specific metering capabilities at their specific address, and the `Terminal Asset Trading rights` NFT

![alt_text](img/terminal-asset-trading-rights-icon.png)

which the homeowner will provide to the GridWorks bidding agent (aka `AtomicTNode`) in order to allow the agent to participate in the GridWorks market structures.

In addition to these 5 real homes, we will create 500 simulated homes which also join the `GNodeRegistry` and are assigned their pair of NFTs.
