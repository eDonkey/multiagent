from app.worker import celery_app


@celery_app.task
def send_followup_message(lead_id: int):
    print(f'Sending follow-up for lead {lead_id}')
