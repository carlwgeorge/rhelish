import asyncio
import json
import os
import time

import aiofiles
import aiohttp

import rhelish


infra = 'https://infrastructure.fedoraproject.org/repo/json'


async def load_data(branch):
    try:
        max_cache_age = int(rhelish.config['el']['max_cache_age'])
    except KeyError:
        max_cache_age = 604800
    cache_file = '{}/pkg_{}.json'.format(rhelish.cache_dir, branch)
    try:
        # check age of cache
        tdiff = time.time() - os.path.getmtime(cache_file)
        if tdiff < max_cache_age:
            try:
                async with aiofiles.open(cache_file) as f:
                    data_str = await f.read()
                    return json.loads(data_str)
            except json.decoder.JSONDecodeError:
                return await refresh_data(branch)
        else:
            return await refresh_data(branch)
    except FileNotFoundError:
        return await refresh_data(branch)


async def refresh_data(branch):
    cache_file = '{}/pkg_{}.json'.format(rhelish.cache_dir, branch)
    url = '{}/pkg_{}.json'.format(infra, branch)
    #from termcolor import colored
    #print(colored(url, 'red'))
    response = await aiohttp.get(url)
    if response.status == 200:
        data = await response.json()
        async with aiofiles.open(cache_file, mode='w') as f:
            data_str = json.dumps(data)
            await f.write(data_str)
        return data
    else:
        response.close()
        return None


async def get_evr(package, branch):
    # load data
    data = await load_data(branch)
    # extract evr
    try:
        epoch = data['packages'][package]['epoch']
        version = data['packages'][package]['version']
        release = data['packages'][package]['release']
    except KeyError:
        return None
    else:
        return '{}:{}-{}'.format(epoch, version, release)


async def get_evrs(package):

    try:
        branches = rhelish.config['el']['branches']
    except KeyError:
        raise SystemExit('cannot parse \'branches\' from \'el\' section of config')

    tasks = [
        asyncio.ensure_future(get_evr(package, branch))
        for branch in branches
    ]
    await asyncio.wait(tasks)
    results = [task.result() for task in tasks]

    return zip(branches, results)
