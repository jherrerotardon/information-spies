from src.commands.fire.fire_city_download import FireCityDownload
from src.commands.tasks.download_place import DownloadPlace as DownloadPlaceTask
from src.commands.actions.download_place import DownloadPlace as DownloadPlaceAction

from pyframework.commands.listen import Listen

metadata = {
    "commands": {
        # Fire.
        'fire:cityDownload': FireCityDownload,

        # Actions.
        '': DownloadPlaceAction,
        # Tasks.
        '': DownloadPlaceTask,

        # Py-framework commands.
        'Listen': Listen,
    },
    'cliTimeout': 60,
}
