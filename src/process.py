import base64
import cv2


#######
class ProcessBase():

    def __init__(self, ext):
        self.ext = ext

    def _ndarray_to_base64(self, ext, img_ndarray):
        res, data = cv2.imencode(ext, img_ndarray)
        data_base64 = base64.b64encode(data).decode('utf-8')
        return data_base64

#######
class GrayScale(ProcessBase):

    def __init__(self, ext, detail_process, detail_parameters): # 入り口を統一するため
        super(GrayScale, self).__init__(ext)

    def do(self, img_ndarray):
        gray = cv2.cvtColor(img_ndarray, cv2.COLOR_RGB2GRAY)
        gray_base64 = super()._ndarray_to_base64(self.ext, gray)
        return gray, gray_base64

#######
class Binarization(ProcessBase):

    cv2_processes = {
        'Binary': cv2.THRESH_BINARY,
        'ToZero': cv2.THRESH_TOZERO,
        'Otsu': cv2.THRESH_OTSU
    }

    def __init__(self, ext, detail_process, detail_parameters):
        super(Binarization, self).__init__(ext)
        self.cv2_process = self.cv2_processes[detail_process]
        self._parse_detail_parameters(detail_process, detail_parameters)

    def do(self, img_ndarray):
        ret, binary = cv2.threshold(img_ndarray, self.threshold, self.max, self.cv2_process)
        base64 = super()._ndarray_to_base64(self.ext, binary)
        return binary, base64

    def _parse_detail_parameters(self, detail_process, detail_parameters):
        self.max = detail_parameters['max']
        if detail_process == 'Otsu':
            self.threshold = 0
        else:
            self.threshold = detail_parameters['threshold']

#######
class Filter(ProcessBase):

    def __init__(self, ext, detail_process, detail_parameters):
        super(Filter, self).__init__(ext)
        self.detail_process    = detail_process
        self.detail_parameters = detail_parameters

    def do(self, img_ndarray):
        blur = None
        if self.detail_process == 'Average':
            blur = self._average_filter(img_ndarray)
        if self.detail_process == 'Median':
            blur = self._median_filter(img_ndarray)
        if self.detail_process == 'Gaussian':
            blur = self._gaussian_filter(img_ndarray)

        base64 = super()._ndarray_to_base64(self.ext, blur)
        return blur, base64

    def _average_filter(self, img_ndarray):
        kernel_x = self.detail_parameters['kernelX']
        kernel_y = self.detail_parameters['kernelY']
        return cv2.Blur(img_ndarray, (kernel_x, kernel_y))

    def _median_filter(self, img_ndarray):
        kernel = self.detail_parameters['kernel']
        return cv2.medianBlur(img_ndarray, kernel)

    def _gaussian_filter(self, img_ndrray):
        kernel_x = self.detail_parameters['kernelX']
        kernel_y = self.detail_parameters['kernelY']
        sigma    = self.detail_parameters['sigma']
        return cv2.GaussianBlur(img_ndrray, (kernel_x, kernel_y), sigma)

#######
class Gradient(ProcessBase):

    def __init__(self, ext, detail_process, detail_parameters):
        super(Gradient, self).__init__(ext)
        self.detail_process    = detail_process
        self.detail_parameters = detail_parameters

    def do(self, img_ndarray):
        grad = None
        if self.detail_process == 'Sobel':
            grad = self._sobel(img_ndarray)
        if self.detail_process == 'Laplacian':
            grad = self._laplacian(img_ndarray)
        if self.detail_process == 'Canny':
            grad = self._canny(img_ndarray)

        base64 = super()._ndarray_to_base64(self.ext, grad)
        return grad, base64

    def _sobel(self, img_ndarray):
        dx = self.detail_parameters['dx']
        dy = self.detail_parameters['dy']
        kernel = self.detail_parameters['kernel']
        return cv2.Sobel(img_ndarray, cv2.CV_64F, dx, dy, ksize=kernel)

    def _laplacian(self, img_ndarray):
        return cv2.Laplacian(img_ndarray, cv2.CV_64F)

    def _canny(self, img_ndarray):
        threshold1 = self.detail_parameters['threshold1']
        threshold2 = self.detail_parameters['threshold2']
        return cv2.Canny(img_ndarray, threshold1, threshold2)
