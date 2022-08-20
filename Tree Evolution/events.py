subscribers = dict()


def subscribe(event, func):
    # subscribe func to event name
    if event not in subscribers.keys():
        subscribers[event] = []

    subscribers[event].append(func)


def post_event(event, data):
    if event in subscribers.keys():
        # print(event+" Event")
        # Notify all subscribers of 'event', pass data.
        for f in subscribers[event]:
            try:
                f(data)
            except TypeError:
                f()

