import os
import cv2
import time
import argparse

from detector import DetectorTF2
from settings import OBJECT_DETECTION_MODEL

# def DetectFromVideo(detector, Video_path, save_output=False, output_dir='output/'):

# 	cap = cv2.VideoCapture(Video_path)
# 	if save_output:
# 		output_path = os.path.join(output_dir, 'detection_'+ Video_path.split("/")[-1])
# 		frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# 		frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 		out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), 30, (frame_width, frame_height))

# 	while (cap.isOpened()):
# 		ret, img = cap.read()
# 		if not ret: break

# 		timestamp1 = time.time()
# 		det_boxes = detector.DetectFromImage(img)
# 		elapsed_time = round((time.time() - timestamp1) * 1000) #ms
# 		img = detector.DisplayDetections(img, det_boxes, det_time=elapsed_time)

# 		cv2.imshow('TF2 Detection', img)
# 		if cv2.waitKey(1) == 27: break

# 		if save_output:
# 			out.write(img)

# 	cap.release()
# 	if save_output:
# 		out.release()



def DetectImagesFromFolder(detector, images_dir, save_output=False, output_dir='output/'):

	for file in os.scandir(images_dir):
		if file.is_file() and file.name.endswith(('.jpg', '.jpeg', '.png')) :
			image_path = os.path.join(images_dir, file.name)
			print(image_path)
			img = cv2.imread(image_path)
			det_boxes = detector.DetectFromImage(img)
			img = detector.DisplayDetections(img, det_boxes)
			extract_bbox(detector,image_path)
			# cv2.imshow('TF2 Detection', img)
			# cv2.waitKey(0)
			save_output=True
			if save_output:
				img_out = os.path.join(output_dir, file.name)
				cv2.imwrite(img_out, img)

def extract_bbox(detect_model,image_path,class_name="leaf"):
	img = cv2.imread(image_path)
	print("----Detecting leaf------")
	det_boxes = detect_model.DetectFromImage(img)
	if len(det_boxes)> 0:
		max_index= 0
		max_confidence = 0
		is_found = False
		for ix,bbox in enumerate(det_boxes):
			if bbox[4] == class_name:
				is_found= True
				if bbox[5] > max_confidence:
					max_confidence = bbox[5]
					max_index = ix
		if is_found:

			x_min, y_min, x_max, y_max = det_boxes[max_index][0],det_boxes[max_index][1],det_boxes[max_index][2],det_boxes[max_index][3]
			# print(img)
			print(x_min,y_min,x_max,y_max)
			img_out = img[y_min:y_max,x_min:x_max]
			print(img_out)
			cv2.imwrite(image_path,img_out)
			return True
		else:
			return False
	else:
		return False



# if __name__ == "__main__":

# 	parser = argparse.ArgumentParser(description='Object Detection from Images or Video')
# 	parser.add_argument('--model_path', help='Path to frozen detection model',
# 						default='models/ssd_mobilenet_v2_leaf_2/exported_model/saved_model')
# 	parser.add_argument('--path_to_labelmap', help='Path to labelmap (.pbtxt) file',
# 	                    default='label_map.pbtxt')
# 	parser.add_argument('--class_ids', help='id of classes to detect, expects string with ids delimited by ","',
# 	                    type=str, default=None) # example input "1,3" to detect person and car
# 	parser.add_argument('--threshold', help='Detection Threshold', type=float, default=0.6)
# 	parser.add_argument('--images_dir', help='Directory to input images)', default='eval_images/sample')
# 	parser.add_argument('--video_path', help='Path to input video)', default='data/samples/pedestrian_test.mp4')
# 	parser.add_argument('--output_directory', help='Path to output images and video', default='eval_images/annonated_images')
# 	parser.add_argument('--video_input', help='Flag for video input, default: False', action='store_true')  # default is false
# 	parser.add_argument('--save_output', help='Flag for save images and video with detections visualized, default: False',
# 	                    action='store_true')  # default is false
# 	args = parser.parse_args()

# 	id_list = None
# 	if args.class_ids is not None:
# 		id_list = [int(item) for item in args.class_ids.split(',')]

# 	if args.save_output:
# 		if not os.path.exists(args.output_directory):
# 			os.makedirs(args.output_directory)

# 	# instance of the class DetectorTF2
# 	detector = DetectorTF2(OBJECT_DETECTION_MODEL, "label_map.pbtxt", class_id=None, threshold=0.6)

# 	if args.video_input:
# 		# DetectFromVideo(detector, args.video_path, save_output=args.save_output, output_dir=args.output_directory)
# 		pass
# 	else:
# 		DetectImagesFromFolder(detector, args.images_dir, save_output=args.save_output, output_dir=args.output_directory)

# 	print("Done ...")
# 	# cv2.destroyAllWindows()
