from edinsights.core.decorators import event_handler, query

@event_handler()
def sample_event_handler(mongodb, events):
    """An empty event handler"""
    pass

@query()
def sample_query(mongodb, parameter):
    """An empty query handler"""
    pass
