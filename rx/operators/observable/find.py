from rx.core import ObservableBase, AnonymousObservable
from rx.core.typing import Predicate


def find_value(source, predicate, yield_index):
    def subscribe(observer, scheduler=None):
        i = [0]

        def send(x):
            should_run = False
            try:
                should_run = predicate(x, i, source)
            except Exception as ex:
                observer.throw(ex)
                return

            if should_run:
                observer.send(i[0] if yield_index else x)
                observer.close()
            else:
                i[0] += 1

        def close():
            observer.send(-1 if yield_index else None)
            observer.close()

        return source.subscribe_(send, observer.throw, close, scheduler)
    return AnonymousObservable(subscribe)

def find(source, predicate: Predicate) -> ObservableBase:
    """Searches for an element that matches the conditions defined by the
    specified predicate, and returns the first occurrence within the entire
    Observable sequence.

    Keyword arguments:
    predicate -- {Function} The predicate that defines the conditions of the
        element to search for.

    Returns an Observable {Observable} sequence with the first element that
    matches the conditions defined by the specified predicate, if found
    otherwise, None.
    """

    return find_value(source, predicate, False)