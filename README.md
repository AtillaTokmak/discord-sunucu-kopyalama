# Discord Server Cloner

Exports Discord guilds to JSON config files, which can then be parsed into a separate guild.

## Discord already provides templates, whats the point?

 - While Discord's templates are more suitable for most scenarios, in
   the event that a guild gets terminated, the template also gets
   deleted.
 - This tool can also be extended, for example resending old messages.

## Commands

|Command|Description|
|--|--|
|$saveconfig name|Exports guild JSON to server_configs directory|
|$loadconfig name|Loads JSON, and recreates the guild|





