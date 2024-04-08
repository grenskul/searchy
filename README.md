# searchy
A discord attachment searching bot

Expects an environment variable called "discord_token" containing a valid discord token .
Also expects a folder mapping to where you will have 3 json files attach_link.json, attach_link.jsonc, this is where it basically stores it's data for permanence (it's not very scalable since it's 3 json files but it's not important for my ends ). If no information is present it expects 3 empty json files with that name.
It has automatic deduplication of found results (at the link level).
This bot isn't really made expecting to be run in multiple servers either.
You can run this standalone without docker but expect to change the hardcoded paths and the files must be present
