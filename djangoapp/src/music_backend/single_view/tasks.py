from celery import shared_task

from music_backend.single_view.services import SingleViewService


@shared_task
def import_csv_file(single_view_data: list) -> None:
    SingleViewService.import_work_single_view(single_view_data)
