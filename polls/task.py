from time import sleep
from mysite import celery_app

@celery_app.task()
def my_task():
    i = 0
    while i<10:
        print("Hola desde mi tarea en segundo plano!")
        sleep(1)
        i+=1
    return 1