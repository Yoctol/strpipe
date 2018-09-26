import json
import os


def serializable(state):
    assert json.dumps(state)


def unchange_after_serialize(state):
    temp_file = 'test_state.json'
    with open(temp_file, 'w') as filep:
        json.dump(state, filep, ensure_ascii=False)
    del filep

    with open(temp_file, 'r') as filep:
        state_restored = json.load(filep)

    os.remove(temp_file)
    assert state == state_restored
