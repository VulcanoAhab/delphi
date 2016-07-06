from grabbers.utils.html import Pythoness

class ProcessSequence:
    '''
    '''
    _browser=None
    _job_id=None
    _sequence=None
    _sequence_maps={
        'size':1,
        'rects':[]
            }

    @classmethod
    def set_job_id(cls, job_id):
        '''
        '''
        cls._job_id=job_id

    @classmethod
    def set_browser(cls, browser):
        '''
        '''
        cls._browser=browser

    @classmethod
    def set_sequence(cls, sequence):
        '''
        '''
        cls._sequence=sequence

    @classmethod
    def mapping(cls, mapper):
        '''
        '''
        if not mapper:return
        ps=Pythoness()
        mapped_elements=ps.map_sequence_targets(mapper)
        mlen=len(mapped_elements)
        if mlen < 1:
            print('[+] Mapping lower than 1 has no purpose')
            return
        cls._sequence_maps={
            'size':mlen,
            'rects':[m.rect for m in mapped_elements]
                }

    @classmethod
    def fire_sequence(cls, index=-1):
        '''
        '''
        for grabber in cls._sequence:
            print('[+] Grabber [{}] running.'.format(grabber))
            job=Job.objects.get(id=cls._job_id) #why | lets improve please
            ps=Pythoness()
            ps.set_job(job)
            ps.set_grabber(grabber)
            ps.session(cls._browser, element_index=index)
            ps.save_data()

    @classmethod
    def run(cls):
        '''
        '''
        if cls._sequence_maps['size']<=1:
            cls.fire_sequence()
        else:
            run_cycle=range(cls._sequence_maps['size'])
            for n in run_cycle:cls.fire_sequence(index=n)
        print('[+] Sequence is done')

