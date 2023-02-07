from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
import pandas as pd
from iou import compute_iou
from point import Point
from shape import BoundingBox

from string_utils import change_string_to_dict

ANNOTATOR_DATA_CSV_PATH = "annotator_data.csv"
GROUND_TRUTH_CSV_PATH = "ground_truth.csv"

COORDINATE_COLUMN = "coordinates"
LABEL_CLASS_COLUMN = "label_class"
CW_EMAIL_COLUMN = "cw"
IOU_COLUMN = "iou"

LOWER_X_COORDINATE = "x_1"
LOWER_Y_COORDINATE = "y_1"
UPPER_X_COORDINATE = "x_2"
UPPER_Y_COORDINATE = "y_2"

# THE TEMPLATE DESIGN PATTERN
class Flow(ABC):
  @abstractmethod
  def load_csv(self) -> None:
    pass
  def pre_compute(self) -> None:
    pass
  def compute(self) -> None:
    pass
  def post_compute(self) -> None:
    pass
  def display_results(self) -> None:
    pass
  def run_flow(self):
    self.load_csv()
    self.pre_compute()
    self.compute()
    self.post_compute()
    self.display_results()

@dataclass
class IOUFlow(Flow):

  _ground_truth_df: pd.DataFrame = pd.DataFrame()
  _annotated_df: pd.DataFrame = pd.DataFrame()
  _iou_scores: List[float] = field(default_factory=list)

  def load_csv(self) -> None:
    self._ground_truth_df = pd.read_csv(GROUND_TRUTH_CSV_PATH)
    self._annotated_df = pd.read_csv(ANNOTATOR_DATA_CSV_PATH)
  
  def pre_compute(self) -> None:
    # convert coordinates column from str to dict
    self._annotated_df[COORDINATE_COLUMN] = self._annotated_df[COORDINATE_COLUMN].apply(change_string_to_dict)
    self._ground_truth_df[COORDINATE_COLUMN] = self._ground_truth_df[COORDINATE_COLUMN].apply(change_string_to_dict)

  def compute(self) -> None:

    for _, row in self._annotated_df.iterrows():

      label_class = row[LABEL_CLASS_COLUMN]

      ground_truth_filtered_by_label_class_df = self._filter_df_by_column_value(self._ground_truth_df, LABEL_CLASS_COLUMN, label_class)
      ground_truth_filtered_by_label_class_coordinates_df = self._get_df_column(ground_truth_filtered_by_label_class_df, COORDINATE_COLUMN)
      ground_truth_coordinate_value = self._get_first_row(ground_truth_filtered_by_label_class_coordinates_df)
      ground_truth_bbox = self._coordinates_to_bounding_box(ground_truth_coordinate_value)

      annotated_bbox = self._coordinates_to_bounding_box(row[COORDINATE_COLUMN])

      iou_score = compute_iou(ground_truth_bbox, annotated_bbox)
      self._iou_scores.append(iou_score)

  
  def post_compute(self) -> None:
    self._annotated_df[IOU_COLUMN] = self._iou_scores
  
  def display_results(self) -> None:
      print(self._annotated_df)

  @staticmethod
  def _filter_df_by_column_value(df: pd.DataFrame, column_name: str, column_value: str) -> pd.DataFrame:
    return df[df[column_name] == column_value]
  
  @staticmethod
  def _get_df_column(df: pd.DataFrame, column_name:str) -> pd.Series:
    return df[column_name]
  
  @staticmethod
  def _get_first_row(df: pd.Series):
    return df.iloc[0]
  
  @staticmethod
  def _coordinates_to_bounding_box(coordinates:dict) -> BoundingBox:
    lower_point = Point(coordinates[LOWER_X_COORDINATE], coordinates[LOWER_Y_COORDINATE])
    upper_point = Point(coordinates[UPPER_X_COORDINATE], coordinates[UPPER_Y_COORDINATE])
    return BoundingBox(lower_point, upper_point)
