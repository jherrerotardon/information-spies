"""
|--------------------------------------------------------------------------
| Database Connections
|--------------------------------------------------------------------------
|
| Here you may configure the connection information for each server that
| is used by your application. A default configuration has been added
| for each back-end shipped with pika. You are free to add more.
|
"""
connections = {}

params = {
    'cliTimeout': 1800,  # Max time to execute event.
    'forceClean': 900,  # Seconds until clean process resources.
    'queues': {
        # |--------------------------------------------------------------------------
        # | Crawler Queue
        # |--------------------------------------------------------------------------
        # | Queue to managements crawler tasks.
        #
        'download_ready': {
            'eventsNames': [
                'download.place.action',
                'download.info.action',
                'download.place.task',
                'download.info.task',
            ],
        },
    }
}
