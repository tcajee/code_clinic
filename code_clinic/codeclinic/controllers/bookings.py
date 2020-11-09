from time import strftime
from cement import Controller, ex

class Bookings(Controller):
    class Meta:
        label = 'Bookings'

    @ex(help='List bookings')
    def list_bookings(self):
        data = {}
        data['bookings'] = self.app.db.all()
        self.app.render(data, 'bookings/list.jinja2')

    @ex(
            help='Create new booking',
            arguments=[
                (
                    ['booking_text'],
                    {
                        'help': 'booking text',
                        'action': 'store'
                    }
                )
            ]
        )
    def create_booking(self):
        text = self.app.pargs.booking_text
        now = strftime("%Y-%m-%d %H%M%S")
        self.app.log.info(f"Creating booking {text}")

        booking = {
            'timestamp': now,
            'state': 'pending',
            'text': text
        }

        self.app.db.insert(booking)

    @ex(
            help='Update a booking',
            arguments=[
                (
                    ['booking_id'],
                    {
                        'help': 'booking database ID',
                        'action': 'store'
                    }
                ),
                (
                    ['--text'],
                    {
                       'help': 'booking text',
                        'action': 'store',
                        'dest': 'booking_text'
                    }
                ),
                ]
            )
    def update_booking(self):
        id = int(self.app.pargs.booking_id)
        text = self.app.pargs.booking_text
        now = strftime("%Y-%m-%d %H%M%S")
        self.app.log.info(f"Updating booking {id} - {text}")

        booking = {
            'timestamp': now,
            'text': text,
        }

        self.app.db.update(booking, doc_ids=[id])

    @ex(
            help='Delete a booking',
            arguments=[
                (
                    ['booking_id'],
                    {
                        'help': 'booking database ID',
                        'action': 'store'
                    }
                )
            ]
        )
    def delete_booking(self):
        id = int(self.app.pargs.booking_id)
        self.app.log.info(f"Deleting booking {id}")
        self.app.db.remove(doc_ids=[id])

    @ex(
            help='Complete a booking',
            arguments=[
                (
                    ['booking_id'],
                    {
                        'help': 'booking database ID',
                        'action': 'store'
                    }
                )
            ]
        )
    def complete_booking(self):
        id = int(self.app.pargs.booking_id)
        now = strftime("%Y-%m-%d %H%M%S")
        booking = self.app.db.get(doc_id=id)

        booking['timestamp'] = now
        booking['state'] = 'complete'

        self.app.log.info(f"Completing booking {id}")
        self.app.db.update(booking, doc_ids=[id])

        ### Send an email message

        msg = """
        MESSAGE BODY
        """

        self.app.mail.send(msg,
                subject='codeclinic test',
                to=[self.app.config.get('codeclinic', 'email')],
                from_addr='noreply@localhost',
                )

