# Office Hours

This page contains a list of topics where we would appreciate outside help and guidance.

## Incentivizing accurate identification of ConductorTopologyNodes

Fleshing out mechanisms for incentivizing the accurate identification of not just TerminalAssets but ConductorTopologyNodes.

## Adding occasional renewal to maintaining active TaDeed

Adding structure so that validation must be occasionally renewed to maintain an active TaDeed. Most generators need to get their metering re-tested once a year. This would be cost-prohibitive for most household load. One idea we like is creating a Poisson process that generates a small random probability of having the validator come and re-test for the TaDeed to stay active. What would it look like to design this into a PyTeal contract?

## Implementing better mechanics for exchanging an old TaDeed for a new one

Work through the timing of exchanging an old TaDeed for a new one that does not disrupt the operational flow of the GridWorks system founded on top of these TaDeeds. I have introduced an extra “graveyard” contract belonging to the admin to help with that (with the idea that assigning the manager to “graveyard” would indicate a liminal state).

## Building User Interfaces

Although we do not intend to build polished UIs in the short run, by next year we will require at least a user interface for installers. In addition, we want a sense for the scope of development work necessary for building reasonably nice user interface that can track the ownership history of TaDeeds and TaTradingRights.

## Better mechanism for branding GNodeAlias into TaDeed

Our GNodeAlias often run longer than 32 characters, so we cannot keep using them as-is for the asset_name. We will need some other mechanism for associating the GNodeAlias immutably with the TaDeed.

## Pytest working in github actions

We'd like to have our tests be part of continuous integration. This will require a local algorand sandbox working (I assume from a docker instance) when the tests are running in github.
