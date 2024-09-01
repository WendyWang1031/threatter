
RELATION_STATUS_NONE = "None"
RELATION_STATUS_PENDING = "Pending"
RELATION_STATUS_FOLLOWING = "Following"

VISIBILITY_PUBLIC = "Public"
VISIBILITY_PRIVATE = "Private"

def get_relation_status(relation_data):

    if relation_data is None or 'relation_state' not in relation_data:
        return RELATION_STATUS_NONE
    
    relation_state = relation_data['relation_state']

    if relation_state is None or relation_state == 'None':
        return RELATION_STATUS_NONE
    elif relation_state == 'Pending':
        return RELATION_STATUS_PENDING
    elif relation_state == 'Following':
        return RELATION_STATUS_FOLLOWING
    
    return RELATION_STATUS_NONE

def get_visibility(visibility, relation_state):
    
    if visibility == VISIBILITY_PUBLIC:
        return True

    if relation_state == RELATION_STATUS_FOLLOWING:
        return True
    
    return False
