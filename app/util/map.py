RECORD = 'record'
FIELD = 'field'




CONV_MAP = {
    'subject': RECORD,
    'status': FIELD,
    'state': RECORD,
    'type': RECORD,
    'threads': RECORD,
    'userUpdatedAt': RECORD,
    'assignee': RECORD,
    'createdAt': RECORD,
    'customFields': RECORD,
    'customerWaitingSince': RECORD,
    'number': RECORD,
    'mailboxId': RECORD,
    'closedBy': RECORD,
    'id': FIELD,
    'createdBy': RECORD,
    'closedAt': RECORD,
    'tags': FIELD,
    'bcc': RECORD,
    'preview': RECORD,
    'source': RECORD,
    'cc': RECORD,
    'folderId': RECORD,
    'primaryCustomer': RECORD
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
    'ticketCount': FIELD,

}