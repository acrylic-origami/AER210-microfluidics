import cv2
import numpy as np
import sys

if __name__ == '__main__':
	with open(sys.argv[1], 'rb') as f:
		f.read(48)
		size = f.read(4)
		size = ord(size[3]) << 24 | ord(size[2]) << 16 | ord(size[1]) << 8 | ord(size[0]) # little endian
		f.read(4)
		for i in range(size+1):
			buff = f.read(8)
			while buff != '\x30\x30\x64\x62\x00\x00\x14\x00' and buff != '':
				buff = f.read(8)
				
			if buff == '':
				# EOF
				break
			
			A = np.fromstring(f.read(1310720), dtype=np.uint8)
			B = np.reshape(A, (1024, 1280))
			cv2.imwrite('%s.%d.png' % (sys.argv[2], i), np.transpose(np.array([B[1::2,::2], (B[::2,::2]+B[1::2,1::2])/2, B[::2,1::2]], dtype=np.uint8), (1, 2, 0)))
