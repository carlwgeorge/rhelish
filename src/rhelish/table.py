import asyncio
import re

from prettytable import PrettyTable

import rhelish.fedora
import rhelish.el



async def get_table(package):

    output = PrettyTable(['BRANCH', 'VERSION'])

    tasks = [
        asyncio.ensure_future(rhelish.fedora.get_evrs(package)),
        asyncio.ensure_future(rhelish.el.get_evrs(package)),
    ]
    await asyncio.wait(tasks)
    results = [task.result() for task in tasks]

    for result in results:
        for pair in result:
            output.add_row(pair)

    output.sortby = 'BRANCH'
    return output


