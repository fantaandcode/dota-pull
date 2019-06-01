import json

output = ''

def register(p_url)
    # Dotabuff or OpenDota
    if ('dotabuff.com/players' in p_url or 'opendota.com/players' in p_url):
        p_id = p_url.split('/')[-1]
        print(p_id)

        # check if PID is an int
        try:
            p_id = int(p_id)
            await ctx.send(f'{p_id} is registered to {ctx.author}')
        except ValueError:
            await ctx.send('The URL might be incorrect, please use OpenDota or Dotabuff.')
    else:
        await ctx.send('The URL might be incorrect, please use OpenDota or Dotabuff.')

    # add later for registration
    # p_id for SteamID
    # ctx.author.id for Discord ID
