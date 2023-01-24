import cv2 
import torch 
import time 
import numpy as np 

Q = np.array(([1.0, 0.0, 0.0, -160.0],
              [0.0, 1.0, 0.0, -120.0],
              [0.0, 0.0, 0.0, 350.0],
              [0.0, 0.0, 1.0/90.0, 0.0]), dtype=np.float32)

# MiDas para depth estimation
#model_type = "DPT_Large"
#model_type = "MiDaS_small"
model_type = "DPT_Hybrid"
midas = torch.hub.load("intel-isl/MiDas", model_type)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
#device = torch.device("cpu")
midas.to(device)
midas.eval()

midas_transforms = torch.hub.load("intel-isl/MiDas", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    start = time.time()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    input_batch = transform(img).to(device)
    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()
        depth_map = prediction.cpu().numpy()
        depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        points_3D = cv2.reprojectImageTo3D(depth_map, Q, handleMissingValues=True)
        mask_map = depth_map > 0.4
        output_points = points_3D[mask_map]
        output_colors = img[mask_map]
        end = time.time()
        totalTime = end - start
        fps = 1 / totalTime
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        depth_map = (depth_map*255).astype(np.uint8)
        depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_MAGMA)
        cv2.imshow('Image', img)
        cv2.imshow('Depth map', depth_map)

        if cv2.waitKey(5) & 0xFF == 27:
            break

##### CREATE POINT CLOUDS ######
def create_output(vertices, colors, filename):
    colors = colors.reshape(-1, 3)
    vertices = np.hstack([vertices.reshape(-1, 3), colors])
    ply_header = '''
    ply
    format_ascii 1.0
    comment VCGLIB generated
    element vertex %(vert_num)d
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    property uchar alpha
    element face 0
    property list uchar int vertex_indices
    end_header
    '''
    with open(filename, 'w') as f:
        f.write(ply_header %dict(vert_num=len(vertices)))
        np.savetxt(f, vertices, '%f %f %f %d %d %d')

output_file = "pointCloudDeepLearning.ply"
create_output(output_points, output_colors, output_file)
cap.release()
cv2.destroyAllWindows()