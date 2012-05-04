from gevent import monkey;monkey.patch_all(dns=False, thread=False)
from gevent import Timeout
import urllib2

CONNECT_TIMEOUT,DATA_TIMEOUT = 10, 10

def curl(ip):
    url = 'http://' + ip
    request = urllib2.Request(url=url)
    reason, other = None, 0

    timeout = Timeout(CONNECT_TIMEOUT + DATA_TIMEOUT)
    timeout.start()
    try:
        rsp = urllib2.urlopen(request)
        print rsp.read()
        reason, other = rsp.getcode(), rsp.msg
    except Timeout, t:
        if t is timeout:
            reason, other = 'gevent timeout', 0
        else:
            reason, other= 'gevent timeout 2', 0
    except urllib2.HTTPError, ex:
        reason, other = ex.code, ex.msg 
    except urllib2.URLError, ex:
        reason = ex.reason
        if isinstance(reason, socket.timeout):
            reason = reason.message
        elif isinstance(reason, socket.error):
            reason = reason.strerror 
    finally:
        timeout.cancel()
        print reason, ip, other
        return reason, ip, other 

if __name__ == '__main__':
    print curl('0.dev.qqpark.com')
    print curl('qzoneapi.tencent.haalee.com')
