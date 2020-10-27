import pytest
import numpy as np

from kale.calibration.calibration_methods import TemperatureScaling
from kale.metrics import ECE
from kale.sampling.fake_clf import DirichletFC
from kale.transformations import ShiftingSimplexAutomorphism


@pytest.fixture(scope="module")
def metric():
    return ECE()


@pytest.fixture(scope="module")
def calibration_method():
    return TemperatureScaling()


@pytest.fixture(scope="module")
def samples():
    shifting_vector = np.array([0, 2])
    aut = ShiftingSimplexAutomorphism(shifting_vector)
    faker = DirichletFC(2, simplex_automorphism=None)
    return faker.get_sample_arrays(1000)


def test_methods_calibrationErrorLessAfterCalibration(metric, samples, calibration_method):
    ground_truth, confidences = samples
    error_pre_calibration = metric.compute(confidences, ground_truth)
    calibration_method.fit(confidences, ground_truth)
    calibrated_confidences = calibration_method.get_calibrated_confidences(confidences)
    error_post_calibration = metric.compute(calibrated_confidences, ground_truth)

    assert error_post_calibration <= error_pre_calibration
