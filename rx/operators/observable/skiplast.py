from rx.core import ObservableBase, AnonymousObservable


def skip_last(count: int, source: ObservableBase) -> ObservableBase:
    """Bypasses a specified number of elements at the end of an observable
    sequence.

    Description:
    This operator accumulates a queue with a length enough to store the
    first `count` elements. As more elements are received, elements are
    taken from the front of the queue and produced on the result sequence.
    This causes elements to be delayed.

    Keyword arguments
    count -- Number of elements to bypass at the end of the source sequence.

    Returns an observable {Observable} sequence containing the source
    sequence elements except for the bypassed ones at the end.
    """

    observable = source

    def subscribe(observer, scheduler=None):
        q = []

        def send(value):
            front = None
            with observable.lock:
                q.append(value)
                if len(q) > count:
                    front = q.pop(0)

            if front is not None:
                observer.send(front)

        return observable.subscribe_(send, observer.throw, observer.close, scheduler)
    return AnonymousObservable(subscribe)