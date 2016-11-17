from __future__ import print_function
import cv2
import sys
import os
import math
import numpy as np

if __name__ == '__main__':
	d = sys.argv[1]
	cols = []
	for f in os.listdir(d):
		with open(os.path.join(d, f), 'r') as fd:
			fd.readline()
			print('%s/frame.%s.png' % (sys.argv[2], f), file=sys.stderr)
			im = cv2.imread('%s/frame.%s.png' % (sys.argv[2], f))
			for i, l in enumerate(fd):
				x1, y1, x2, y2 = [int(float(v)) for v in l.strip().split('\t')]
				
				dark = np.zeros(im.shape)
				cv2.line(dark, (x1, y1), (x2, y2), (1, 1, 1), 2)
				
				radial = np.zeros(im.shape)
				cv2.line(radial, (x1, y1), (x2, y2), (1, 1, 1), 6)
				cv2.line(radial, (x1, y1), (x2, y2), (0, 0, 0), 2)
				
				vec = np.array((x1-x2, y1-y2))
				unit_vec = vec/np.linalg.norm(vec)
				axial = np.zeros(im.shape)
				cv2.line(axial, tuple((-4*unit_vec).astype(np.int16)), tuple((vec+4*unit_vec).astype(np.int16)), (1, 1, 1), 6)
				cv2.line(axial, (x1, y1), (x2, y2), (0, 0, 0), 2)
				# cv2.imshow('%s.%d' % (f, i), np.multiply(im, np.reshape((dark[:,:,0] == 1), im.shape[:-1] + (1,)))[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)])
				vs = cv2.cvtColor(np.array([im[np.reshape((dark[:,:,0] == 1), im.shape[:-1])]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0,:,2]
				radial_vs = cv2.cvtColor(np.array([im[np.reshape((radial[:,:,0] == 1), im.shape[:-1])]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0,:,2]
				axial_vs = cv2.cvtColor(np.array([im[np.reshape((axial[:,:,0] == 1), im.shape[:-1])]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0,:,2]
				
				cols.append('%.3f\t%.3f\t%.3f' % (math.sqrt((x2-x1)**2+(y2-y1)**2), np.mean(vs)/np.mean(radial_vs), np.mean(vs)/np.mean(axial_vs)))
				print(f, i, file=sys.stderr)
	print("\n".join(cols))