"""A simple pubsub library.

The goal is to have a simple pubsub library in python.

  Typical usage example:

  # Create an instance of a service that inherits from PubSub
  email_service = EmailService()

  # Subscribe to the EmailSentEvent of the service
  email_service.subscribe(lambda x: print(x), EmailSentEvent)

  # When the service sends the email the lambda function is executed
  email_service.send('mmann2943@gmail.com', 'cmann2943@gmail.com', 'This is a 2nd test email message with a subscription')

  # The implementation of the EmailService is below
  class EmailService(PubSub):
    def __init__(self) -> None:
        self.events_supported = Union[EmailSentEvent, None]
        super().__init__()

    def send(self, to_email: str, from_email: str, email_body: str) -> None:
        print('sending email')
        self.publish(EmailSentEvent(to_email, from_email, email_body))
"""
import abc
from typing import Callable, List, Type, Union

class Event(abc.ABC):
    """Represents an event in a publish/subscribe context.

    Attributes:
        name: The name of the event derived from the class name
    """
    def __init__(self):
        self.name = type(self).__name__


class PubSub(abc.ABC):
    """Represents the pub/sub behavior

    Attributes:
        subscribers: The subscribers to an event where the name of the event is the key
    """
    def __init__(self):
        self.subscribers: dict[str] = {}

    def publish(self, event: Event):
        """Publishes the event to all subscribers.

        Args:
          event:
            The event to publish.
        """
        if event.name in self.subscribers:
            for fn in self.subscribers[event.name]:
                fn(event)
        else:
            print(f'sorry but no subscribers for {event.name}')

    def subscribe(self, fn: Callable, event: Event):
        """Subscribe to an event.

        Args:
          fn: A Callable to execute when the event is raised
          event: The event being subscribed to
        """
        event_name: str = event.__name__
        if event_name not in self.subscribers:
            print(f'event {event_name} does not exist so adding')
            functions_list: List[Callable] = []
            self.subscribers[event_name] = functions_list

        self.subscribers[event_name].append(fn)
