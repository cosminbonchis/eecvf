import os

# noinspection PyPackageRequirements
import cv2
import numpy as np
import json

import config_main
from Utils.log_handler import log_setup_info_to_console, log_error_to_console, log_benchmark_info_to_console
from Benchmarking.Util.image_parsing import find_img_extension


def sb_iou(box1, box2) -> float:
    x1, y1, x2, y2 = box1[0][0], box1[0][1], box1[1][0], box1[1][1]
    x3, y3, x4, y4 = box2[0][0], box2[0][1], box2[1][0], box2[1][1]
    x_inter1 = max(x1, x3)
    y_inter1 = max(y1, y3)
    x_inter2 = min(x2, x4)
    y_inter2 = min(y2, y4)
    width_inter = abs(x_inter2 - x_inter1)
    height_inter = abs(y_inter2 - y_inter1)
    area_inter = width_inter * height_inter
    width_box1 = abs(x2 - x1)
    height_box1 = abs(y2- y1)
    width_box2 = abs(x4 - x3)
    height_box2 = abs(y4 - y3)
    area_box1 = width_box1 * height_box1
    area_box2 = width_box2 * height_box2
    area_union = area_box1 + area_box2 - area_inter
    iou = area_inter / area_union
    return iou


# noinspection PyPep8Naming
def run_SB_benchmark_IoU() -> None:
    """
    Calculate the IoU for a set of images.
    :param class_list_name: list of names corresponding the classes
    :param unknown_class: the class value for unknown classification of pixels.
    :param is_rgb_gt: if ground truth images are in RGB format
    :param class_list_rgb_value: list of greyscale values of RGB colors used.
    :param show_only_set_mean_value: show on console only the mean IoU for each set
    :return: None
    """
    log_setup_info_to_console("BENCHMARKING SB IoU")

    for set_image in config_main.BENCHMARK_SETS:
        log_benchmark_info_to_console('Current set: {}'.format(set_image))

        try:
            # Write results to disk
            results_path = os.path.join(os.getcwd(), config_main.BENCHMARK_RESULTS, 'SB_IoU')

            if not os.path.exists(results_path):
                os.makedirs(results_path)

            ground_truth = dict()
            json_files = [f for f in os.listdir(config_main.BENCHMARK_GT_LOCATION) if os.path.isfile(os.path.join(config_main.BENCHMARK_GT_LOCATION, f))]

            for json_file in json_files:
                f = open(os.path.join(config_main.BENCHMARK_GT_LOCATION, json_file))
                data = json.load(f)
                f.close()

                try:
                    ground_truth[data["asset"]["name"]] = data["regions"]["points"]
                except KeyError as e:
                    log_error_to_console('BENCHMARK SB IoU NOK: Key Not Found', e.__str__())

            # Here read json from algorithm
            for file in config_main.BENCHMARK_SAMPLE_NAMES:
                pass

        except Exception as ex:
            log_error_to_console('BENCHMARK SB IoU NOK', ex.__str__())


if __name__ == "__main__":
    pass