from typing import List
import json

from strpipe.ops import op_factory as default_op_factory


_EMPTY_STATE_FILLER = '_EMPTY_STATE_FILLER'


class _Step:

    def __init__(self, op, state=None):
        self.op = op
        self.state = state

    def fit(self, data):
        if self.state is not None:  # avoid re-fit if state is exist
            # TODO: add a force-update condition
            return
        self.state = self.op.fit(data) or _EMPTY_STATE_FILLER
        # NOTE: if the op is stateless, the op.fit will return None

    def transform(self, data):
        state = None if self.state == _EMPTY_STATE_FILLER else self.state
        return self.op.transform(state, data)

    def inverse_transform(self, data, tx_info):
        state = None if self.state == _EMPTY_STATE_FILLER else self.state
        return self.op.inverse_transform(state, data, tx_info)

    @property
    def output_type(self):
        return self.op.output_type

    @property
    def input_type(self):
        return self.op.input_type

    @property
    def can_transform(self):
        return self.state is not None


class Pipe:

    def __init__(self, op_factory=None):
        self._steps = []
        self._step_info = []
        self.op_factory = default_op_factory if op_factory is None else op_factory
        self.reset_checkpoints()

    def add_step_by_op_name(
            self,
            op_name,
            op_kwargs=None,
            state=None,
        ):
        """Add steps based on the operation name.

        This method create a steps, which has a op. The op
        is created

        Args:
            op_name:
            op_kwargs,
            state,

        Raises:
            TypeError:

        """
        if op_kwargs is None:
            op_kwargs = {}
        op = self.op_factory[op_name](**op_kwargs)
        step = _Step(op, state)
        if len(self._steps) > 0:
            target_type = self._steps[-1].output_type
            in_type = step.input_type
            if in_type != target_type:
                raise TypeError("InputType of the step op is not valid."
                                f"Got {in_type}, but requires {target_type}")
        self._steps.append(step)
        self._step_info.append({  # for pipe serialization
            'op_name': op_name,
            'op_kwargs': op_kwargs,
        })

    def add_checkpoint(self):
        """Record current index of steps"""
        self._checkpoints.add(len(self._steps) - 1)

    def set_checkpoints(self, step_indices: List[int]):
        """Record all indices of steps"""
        self._checkpoints = set(step_indices)

    def reset_checkpoints(self):
        """Clear recorded indices of steps"""
        self._checkpoints = set()

    def fit(self, data):
        input_data = data
        for step in self._steps:
            step.fit(input_data)
            input_data, _ = step.transform(input_data)

    def transform(self, data):
        """Process data based on Steps(Ops).

        This method process input data according to the given
        steps.

        Args:
            data:

        Returns:
            data: transfromed data
            tx_info: list of information for inverse transformation.
            intermediate: list of intermediate data processed during
                          transfromation

        """

        self._check_all_steps_can_transform()
        tx_info = []
        intermediate = []
        for i, step in enumerate(self._steps):
            data, meta = step.transform(data)
            tx_info.append(meta)
            if i in self._checkpoints:
                intermediate.append(data)
        return data, tx_info, intermediate

    def inverse_transform(self, data, tx_info):
        self._check_all_steps_can_transform()
        n_steps = len(self._steps)
        for idx in reversed(range(n_steps)):
            meta = tx_info[idx]
            step = self._steps[idx]
            data = step.inverse_transform(data, meta)
        return data

    def get_state(self, index: int):
        state = self._steps[index].state
        return state

    def save_json(self, path):
        serializable = {}
        step_recoverables = []
        # save step info and state
        for step, info in zip(self._steps, self._step_info):
            step_recoverables.append({
                **info,
                'state': step.state,
            })
        serializable['steps'] = step_recoverables
        # save checkpoints
        serializable['checkpoints'] = list(self._checkpoints)
        with open(path, 'w') as fw:
            json.dump(serializable, fw, ensure_ascii=False)

    @classmethod
    def restore_from_json(cls, path: str, op_factory=None):
        p = cls(op_factory=op_factory)
        with open(path, 'r') as f:
            _data = json.load(f)
            step_recoverables = _data['steps']
        # restore steps
        for step_info in step_recoverables:
            p.add_step_by_op_name(
                op_name=step_info['op_name'],
                op_kwargs=step_info['op_kwargs'],
                state=step_info['state'],
            )
        # restore checkpoints
        p.set_checkpoints(_data.get('checkpoints', []))
        return p

    def _check_all_steps_can_transform(self):
        steps_can_transform_status = [s.can_transform for s in self._steps]
        return all(steps_can_transform_status)
