"""
This module contains classes for dealing with state logic
- especially as it pertains to getting and looking up state indexes
"""
import sys
import re

from collections import OrderedDict

if sys.version_info[1] < 6:
    raise Warning("""
        The State and StateSpace classes rely on Python version
        3.6 or greater (preserving the OrderedDict of kwargs) -
        use at your own risk
    """)


# TODO: Add more functionality once we figure out continuous state spaces
class AttrStateSpace:
    """
    A factory to produce a State class that contains methods for
    state indexing and state index lookup for Attribute State Spaces

    An attribute state space (and associatively a state) contain operations
    that convert a set of attributes (or variables) into a single state vector
    representation, and back. Practically, this looks something like:

        AttrState(hand_value=15, dealer_card=6, can_split=True, ...)
        <->
        state_ndx = 10293

    This is extremely helpful in building and interpreting transition matrices,
    reward vectors, value vectors, etc.
    """
    def __init__(self, *attr_lists, **named_attr_lists):
        """
        :param attr_lists: A varargs set of lists of unnamed variables
                          to include in the state
        :param named_attr_lists: A named args set of lists to specify the name
                            of the variables
        """
        self.state_var_map = OrderedDict({
            f"_{unnamed_arg_ndx}": attr_lists[unnamed_arg_ndx]
            for unnamed_arg_ndx in range(len(attr_lists))
        })
        for named_arg, attr_list in named_attr_lists.items():

            # Regex search text: "_{integer}" for entire string
            if re.search(r'\A_\d+\Z', named_arg):
                raise ValueError(
                    f"Named attribute {named_arg} shadows "
                    "unnamed arg naming convention"
                )

            self.state_var_map[named_arg] = attr_list

        self.state_class = self._create_state_class()

    def _create_state_class(state_space):
        """
        Factory method to create and return a state class for this state space
        :return: State class
        """

        class AttrState:
            """
            This subclass represents a state corresponding to the state space of
            attributes given

            Can be inherited to implement methods like `get_transition_vector`,
            `get_reward`, `get_value`, etc.
            """
            def __init__(self, *args, _state_ndx=None, **kwargs):
                """
                :param args: Ordered list of attributes (named or unnamed)
                             for the state
                :param kwargs: Set of named attributes for the state
                """
                self.state_var_map = state_space.state_var_map
                attr_keys = self.state_var_map.keys()

                try:
                    for ndx, attr_key in enumerate(attr_keys):
                        if ndx < len(args):
                            val = args[ndx]
                        else:
                            val = kwargs[attr_key]

                        if val not in self.state_var_map[attr_key]:
                            raise ValueError(
                                f"'{attr_key}'={val} not in Attribute List "
                                "for State Space"
                            )

                        # Setting attribute so that we can access it without
                        # using stringed keys to dict
                        setattr(self, attr_key, val)

                except KeyError:
                    raise ValueError(
                        'Must specify all attributes when creating State'
                    )

                if _state_ndx is None:
                    _state_ndx = self.get_state_ndx()
                self.state_ndx = _state_ndx

            def get_state_ndx(self):
                """
                Returns the state ndx in the AttrStateSpace for this state

                Example calculation:

                Consider attributes a, b, c. With these conditions:
                    - a in [10, 20, 30]
                    - b in [0, 1]
                    - c in [1, 2, 3]

                Total states = len(a_list) * len(b_list) * len(c_list) =
                3 * 2 * 3 = 18

                State index for AttrState(a=20, b=1, c=1) =
                index(a) + (index(b) * len(a_list)) +
                    (index(c) * len(a_list) * len(b_list)) =
                1 + (1 * 3) + (0 * 3 * 2) = 4

                State index for AttrState(a=20, b=1, c=2) =
                1 + (1 * 3) + (1 * 3 * 2) = 10

                State index for AttrState(a=30, b=1, c=3) =
                2 + (1 * 3) + (2 * 3 * 2) = 17 (max index)

                State index for AttrState(a=10, b=0, c=1) =
                0 + (0 * 3) + (0 * 3 * 2) = 0 (min index)

                :return: AttrStateSpace index (int)
                """
                state_ndx = 0

                for ndx, (attr_name, attr_list) in enumerate(
                        self.state_var_map.items()
                ):
                    curr_ndx_val = attr_list.index(
                        getattr(self, attr_name)
                    )

                    for i in range(ndx):
                        curr_ndx_val *= len(
                            list(self.state_var_map.values())[i]
                        )

                    state_ndx += curr_ndx_val

                return state_ndx

            @classmethod
            def from_ndx(cls, state_ndx):
                """
                Creates and returns a state given the index
                :param state_ndx: index within the AttrStateSpace
                :return: AttrState
                """
                attr_ndxs = []
                curr_state_ndx = state_ndx

                for attr_list in state_space.state_var_map.values():
                    attr_ndx = curr_state_ndx % len(attr_list)
                    curr_state_ndx //= len(attr_list)

                    attr_ndxs.append(attr_ndx)

                if curr_state_ndx != 0:
                    raise ValueError("This function is wrong")

                return AttrState(
                    *[
                        list(state_space.state_var_map.values())[ndx][attr_ndx]
                        for ndx, attr_ndx in enumerate(attr_ndxs)
                    ],
                    _state_ndx=state_ndx  # Don't want to calculate again
                )

            def __repr__(self):
                """
                Default representation of the state (could prob be overridden)
                """
                return 'AttrState - {}\n{}'.format(
                    self.state_ndx,
                    '\n'.join([
                        f"  {attr_name}: {getattr(self, attr_name)}"
                        for attr_name in self.state_var_map
                    ])
                )

        return AttrState

    def state_from_attrs(self, *attr_args, **attr_kwargs):
        """
        Wrapper to return a state object from a set of attributes
        :return: an AttrState object
        """
        return self.state_class(*attr_args, **attr_kwargs)

    def state_from_ndx(self, state_ndx):
        """
        Wrapper to return a state object given a state index
        :return: An AttrState object
        """
        return self.state_class.from_ndx(state_ndx)
