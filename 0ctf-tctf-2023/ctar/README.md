### ctar

Some kind of file upload/download and packaging service

### Solution

Make the server throw exception in `f.extractall` after `self.data` status changed, and then you can download flag directly.
