"""Detección de landmarks con MediaPipe FaceLandmarker (478 puntos + pose de cabeza)."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import math
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "face_landmarker.task"


@dataclass
class FaceResult:
    image_bgr: np.ndarray
    pts: np.ndarray            # (478, 3) en píxeles: x, y, z (z escalado por ancho)
    yaw: float                 # grados; + = gira hacia su izquierda (mira a la derecha de la imagen)
    pitch: float               # grados; + = mira hacia arriba
    roll: float                # grados; + = inclina cabeza en sentido horario en la imagen
    blur: float                # varianza del laplaciano sobre la cara (más alto = más nítida)

    @property
    def size(self) -> tuple[int, int]:
        h, w = self.image_bgr.shape[:2]
        return w, h


_landmarker = None


def _get_landmarker():
    global _landmarker
    if _landmarker is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Falta el modelo: {MODEL_PATH}")
        opts = vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(MODEL_PATH)),
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=True,
            min_face_detection_confidence=0.5,
        )
        _landmarker = vision.FaceLandmarker.create_from_options(opts)
    return _landmarker


def _euler_from_matrix(m: np.ndarray) -> tuple[float, float, float]:
    """Yaw, pitch, roll en grados a partir de la matriz 4x4 de MediaPipe (cámara mira -Z)."""
    r = m[:3, :3]
    sy = math.sqrt(r[0, 0] ** 2 + r[1, 0] ** 2)
    if sy > 1e-6:
        pitch = math.degrees(math.atan2(r[2, 1], r[2, 2]))
        yaw = math.degrees(math.atan2(-r[2, 0], sy))
        roll = math.degrees(math.atan2(r[1, 0], r[0, 0]))
    else:
        pitch = math.degrees(math.atan2(-r[1, 2], r[1, 1]))
        yaw = math.degrees(math.atan2(-r[2, 0], sy))
        roll = 0.0
    return yaw, pitch, roll


def detect(image_path: str | Path) -> FaceResult:
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {image_path}")
    return detect_array(img)


def detect_array(img: np.ndarray) -> FaceResult:
    h, w = img.shape[:2]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    res = _get_landmarker().detect(mp_img)
    if not res.face_landmarks:
        raise ValueError("No se detectó ninguna cara")
    lm = res.face_landmarks[0]
    pts = np.array([[p.x * w, p.y * h, p.z * w] for p in lm], dtype=np.float64)
    yaw = pitch = roll = 0.0
    if res.facial_transformation_matrixes:
        m = np.array(res.facial_transformation_matrixes[0])
        yaw, pitch, roll = _euler_from_matrix(m)
    x0, y0 = pts[:, 0].min(), pts[:, 1].min()
    x1, y1 = pts[:, 0].max(), pts[:, 1].max()
    crop = img[max(0, int(y0)):int(y1), max(0, int(x0)):int(x1)]
    blur = float(cv2.Laplacian(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()) if crop.size else 0.0
    return FaceResult(image_bgr=img, pts=pts, yaw=yaw, pitch=pitch, roll=roll, blur=blur)
