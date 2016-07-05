import hashlib

def build_control_key(url, job_id):
    '''
    '''
    mdis=hashlib.md5()
    mdis.update(url.encode())
    return '---'.join([mdis.hexdigest(), str(job_id)])

