# Testing functions for autocorrelation and helper functions

### Area used for testing: ###
# NW: LatLng(41.9245, -87.83981)
# SE: LatLng(41.82225, -87.51297)
import batch.ops.autocorr as A

def go():
    print(A.get_squares(1000, 41.9245, -87.83981, 41.82225, -87.51297))
