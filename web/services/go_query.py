import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import GoInfo, GoInteraction

class InvalidGOIDException(Exception):
    # raised when the GO ID format is invalid.
    pass

class GOIDNotFoundException(Exception):
    # raised when the GO term is not found in the database.
    pass

def normalize_go(go_id):
    """
    Normalize user input GO term to the format 'GO:XXXXXXX'.
    """
    go_id = go_id.strip().upper().replace("GO:", "").replace("GO", "")
    if not go_id.isdigit():
        raise InvalidGOIDException("Invalid GO term format")
    return f"GO:{go_id.zfill(7)}"

def go_term_details(go_id):
    # normalize GO term
    go_id = normalize_go(go_id)

    # query GO term information
    go_info = GoInfo.query.filter_by(id=go_id).first()
    if not go_info:
        raise GOIDNotFoundException(f"GO term not found: {go_id}")

    # query outgoing and incoming interactions
    outgoing_interactions = GoInteraction.query.filter_by(go_id=go_id).all()
    incoming_interactions = GoInteraction.query.filter_by(target_go_id=go_id).all()

    # prepare interaction data
    outgoing_data = [
        {'go_term': interaction.go_id, 'to_go_term': interaction.target_go_id, 'interaction_type': interaction.relationship}
        for interaction in outgoing_interactions
    ]
    incoming_data = [
        {'go_term': interaction.target_go_id, 'from_go_term': interaction.go_id, 'interaction_type': interaction.relationship}
        for interaction in incoming_interactions
    ]

    # return in json format
    return {
        'basic_info': {
            'id': go_info.id,
            'name': go_info.name,
            'category': go_info.category,
            'description': go_info.description,
        },
        'outgoing_interactions': outgoing_data,
        'incoming_interactions': incoming_data
    }
