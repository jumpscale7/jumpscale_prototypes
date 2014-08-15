from __future__ import absolute_import

from celery import Celery

redis = 'redis://localhost:6379/0'

celery = Celery('proj.celery',
                broker=redis,
                backend=redis,
                include=['proj.tasks'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    celery.start()