import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
import onnx_graphsurgeon as gs
from utils.enums import ONNX_DTYPES_TO_TF_DTYPES
from utils.common_functions import (
    get_constant_or_variable,
    print_node_info,
)


@print_node_info
def make_node(
    *,
    graph_node: gs.Node,
    tf_layers_dict: dict,
    **kwargs: dict,
):
    """RandomNormalLike

    Parameters
    ----------
    graph_node: gs.Node
        graph_surgeon Node

    tf_layers_dict: dict
        optype, shape, dtype, tensorflow graph
    """
    graph_node_input = get_constant_or_variable(graph_node.inputs[0])
    graph_node_output: gs.Variable = graph_node.outputs[0]

    shape = graph_node_output.shape
    dtype = graph_node_output.dtype

    rdtype = graph_node.attrs.get('dtype', 1)
    rmean = graph_node.attrs.get('mean', 0.0)
    rscale = graph_node.attrs.get('scale', 1.0)
    rseed = graph_node.attrs.get('seed', 0)
    rshape = graph_node_input.shape

    # Preserving Graph Structure (Dict)
    tf_layers_dict[graph_node_output.name] = {
        'optype': graph_node.op,
        'shape': shape,
        'dtype': dtype,
    }

    # Generation of TF OP
    tf_layers_dict[graph_node_output.name]['tf_node'] = \
        tf.random.normal(
            shape=rshape,
            mean=rmean,
            stddev=rscale,
            dtype=ONNX_DTYPES_TO_TF_DTYPES[rdtype],
            seed=rseed,
            name=graph_node.name,
        )
