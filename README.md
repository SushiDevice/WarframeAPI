# WarframeAPI

 ¡A small 4fun project that instanties a discord bot for asking
 questions related to the state of Warframe!

 Options are limited because some warframe APIs documentation
 are still in development.

 Currently using:

 - Warframe Community market API: https://warframe.market/api_docs
 - Warframe Status API: https://docs.warframestat.us/

## Current functionalities

For now, this bot allows 5 commands:

- `!price "Some item"` e.g. `!price gauss_prime_set` Please note that the items must be tradeable for the bot to show a list of prices.
- `!baro` This will display information about the state of the void trader, if is not in the solar system, the bot will tell you.
- `!warframe "Some_warframe` e.g. `!warframe volt prime` This will show you some basic information about the warframe that you gave as input.
- `!weapon "Some_weapon"` e.g. `!weapon tonkor` This will show you statistics related to the weapons, like critical chance. 
- `!drops "Some item"` e.g. `!drops gauss prime blueprint` This command will show you the relics that drop this item, but due to API limitations it will not make distinction from those that are currently in vault.
