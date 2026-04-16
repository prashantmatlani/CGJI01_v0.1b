
from core.domain_triggers import DEPTH_TRIGGERS
from core.detection_engine import significance

#def philosophical_depth_required(text):
#    return significance(text, DEPTH_TRIGGERS) > 0.55

def philosophical_depth_required(text):
    score = significance(text, DEPTH_TRIGGERS)
    return score > 0.55 and len(text.split()) > 3
