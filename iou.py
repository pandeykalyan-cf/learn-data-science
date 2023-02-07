from shape import Shape

def compute_iou(ground_truth: Shape, annotated: Shape) -> float:

    ground_truth_area = ground_truth.area()
    annotated_area = annotated.area()

    intersection_area = ground_truth.intersect(annotated)

    iou = intersection_area/float(ground_truth_area + annotated_area - intersection_area)

    return iou


