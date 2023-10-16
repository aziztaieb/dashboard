RECORD = 'record'
FIELD = 'field'




CONV_MAP = {
    'status': FIELD,
    'state': RECORD,
    'type': RECORD,
    'userUpdatedAt': RECORD,
    'assignee': RECORD,
    'createdAt': RECORD,
    'customerWaitingSince': RECORD,
    'mailboxId': RECORD,
    'closedBy': RECORD,
    'id': FIELD,
    'createdBy': RECORD,
    'closedAt': RECORD,
    'tags': FIELD,
    'folderId': RECORD,
    'primaryCustomer': RECORD,
    'closedByUser': RECORD
}


MAILBOXES_MAP = {
    'id': FIELD,
    'name': FIELD,
    'slug': FIELD,
    'email': FIELD,
    'createdAt': FIELD,
    'updatedAt': FIELD
}

USERS_MAP = {
    'photoUrl': FIELD,
    'id': FIELD,
    'firstName': FIELD,
    'updatedAt': FIELD,
    'lastName': FIELD,
    'email': FIELD,
    'role': FIELD,
    'timezone': FIELD,
    'type': FIELD,
    'createdAt': FIELD
}

TAGS_MAP= {
    
    'name': FIELD,
    'ticketCount': FIELD

}

USERS_MAP = {
    
    'firstName': FIELD,
    'role': FIELD,
    
}
