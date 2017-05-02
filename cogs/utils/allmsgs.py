import json
import mimetypes
from random import randint

quick = [('shrug', '¯\_(ツ)_/¯'), ('flip', '(╯°□°）╯︵ ┻━┻'), ('unflip', '┬─┬﻿ ノ( ゜-゜ノ)'), ('lenny', '( ͡° ͜ʖ ͡°)'), ('comeatmebro', '(ง’̀-‘́)ง')]


# Quick cmds for da memes
def quickcmds(message):
    for i in quick:
        if message == i[0]:
            return i[1]
    return None


# Searches commands.json for the inputted command. If exists, return the response associated with the command.
def custom(message):
    success = False

    with open('settings/config.json') as f:
        config = json.load(f)
    if message.startswith(config['customcmd_prefix'][0]):
        with open('settings/commands.json', 'r') as f:
            commands = json.load(f)
        found_cmds = {}
        for i in commands:
            if message[1:].lower().startswith(i.lower()):
                found_cmds[i] = len(i)

        if found_cmds != {}:
            match = max(found_cmds, key=found_cmds.get)

            # If the commands resulting reply is a list instead of a str
            if type(commands[match]) is list:
                try:
                    # If index from list is specified, get that result.
                    if message[len(match) + 1:].isdigit():
                        index = int(message.content[len(match) + 1:].strip())
                    else:
                        title = message[len(match) + 1:]
                        for b, j in enumerate(commands[match]):
                            if j[0].lower() == title.lower().strip():
                                index = int(b)
                                break
                    mimetype, encoding = mimetypes.guess_type(commands[match][index][1])

                    # If value is an image, send as embed
                    if mimetype and mimetype.startswith('image'):
                        return 'embed', commands[match][index][1]
                    else:
                        return 'message', commands[match][index][1]
                except:

                    # If the index is not specified, get a random index from list
                    index = randint(0, len(commands[match]) - 1)
                    mimetype, encoding = mimetypes.guess_type(commands[match][index][1])

                    # If value is an image, send as embed
                    if mimetype and mimetype.startswith('image'):
                        return 'embed', commands[match][index][1]
                    else:
                        return 'message', commands[match][index][1]
            else:
                mimetype, encoding = mimetypes.guess_type(commands[match])

                # If value is an image, send as embed
                if mimetype and mimetype.startswith('image'):
                    return 'embed', commands[match]
                else:
                    return 'message', commands[match]
    if success is True:
        return None
