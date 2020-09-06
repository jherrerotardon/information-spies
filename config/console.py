from pyframework.commands.listen import Listen

from src.commands.actions.download_entity import DownloadEntity as DownloadEntityAction
from src.commands.actions.download_place import DownloadPlace as DownloadPlaceAction
from src.commands.fire.fire_city_download import FireCityDownload
from src.commands.fire.fire_entity_download import FireEntityDownload
from src.commands.tasks.download_entity import DownloadEntity as DownloadEntityTask
from src.commands.tasks.download_place import DownloadPlace as DownloadPlaceTask

metadata = {
    "commands": {
        # Fire.
        'fire:cityDownload': FireCityDownload,
        'fire:entityDownload': FireEntityDownload,

        # Actions.
        'download:place:ready:action': DownloadPlaceAction,
        'download:entity:ready:action': DownloadEntityAction,

        # Tasks.
        'download:place:ready:task': DownloadPlaceTask,
        'download:entity:ready:task': DownloadEntityTask,

        # Py-framework commands.
        'Listen': Listen,
    },
    'cliTimeout': 60,
}
