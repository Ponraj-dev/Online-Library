from celery import Celery,Task # type: ignore
from .task import send_monthly_report,send_daily_mail,export_csv_report
from website import create_app
import flask_excel  as excel
import os
from celery import Celery,shared_task # type: ignore
import flask_excel as excel # type: ignore
from celery.schedules import crontab # type: ignore

def create_celery_app(app):
    celery = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        timezone = 'Asia/Kolkata'
    )
    celery.conf.update(app.config)

    class ContextTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app =  create_app()
excel.init_excel(app)
celery =  create_celery_app(app)
celery.set_default()




@celery.on_after_configure.connect
def setup_periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(
        crontab(minute=1, hour=16 ),
        send_daily_mail.s(),
    )
    sender.add_periodic_task(
        crontab(minute=0, hour=1, day_of_month=1),
        send_monthly_report.s(),
    )
    sender.add_periodic_task(
        crontab(minute=0, hour=1, day_of_month=1),
        export_csv_report.s(),
    )