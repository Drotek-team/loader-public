import numpy as np
from hypothesis import settings
from hypothesis import strategies as st

slow = settings(max_examples=10)
st_nb_x = st.integers(1, 3)
st_nb_y = st.integers(1, 3)
st_nb_drone_per_family = st.integers(1, 3)
st_step_takeoff = st.floats(1, 10)
st_angle_takeoff = st.floats(0, 2 * np.pi)
