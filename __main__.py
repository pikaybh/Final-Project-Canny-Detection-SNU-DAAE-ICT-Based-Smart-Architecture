# %%
from canny_edge_detection import CannyEdge

import os
from tqdm import tqdm


if __name__ == "__main__":
    input_dir = "<Change this>"
    output_dir = "output"
    if not os.path.isdir(output_dir): os.mkdir
    for file in tqdm(os.listdir(input_dir)):
        canny_obj = CannyEdge(input_dir, file, output_dir)
        canny_obj.contouring()
# %%
