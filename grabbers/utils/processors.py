from grabbers.utils.html import Pythoness

class ProcessSequence:
    '''
    '''
    _browser=None
    _job=None
    _task=None
    _sequence=None
    _sequence_maps={
        'size':1,
        'rects':[]
            }

    @classmethod
    def set_job(cls, job):
        '''
        '''
        cls._job=job

    @classmethod
    def set_task(cls, task):
        '''
        '''
        cls._task=task


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
        ps._job=cls._job
        ps.map_targets(mapper, cls._browser)


    @classmethod
    def fire_sequence(cls, index=-1):
        '''
        '''
        for indexed_grabber in cls._sequence:
            print('[+] Grabber [{}] running.'.format(indexed_grabber))
            ps=Pythoness()
            ps.set_job(cls._job)
            ps.set_task(cls._task)
            ps.set_grabber(indexed_grabber.grabber)
            ps.session(cls._browser, element_index=index)
            ps.save_data(cls._browser)

    @classmethod
    def run(cls):
        '''
        '''
        if not cls._sequence:
            print('[+] No sequence to work')
            return
        if cls._sequence_maps['size']<=1:
            cls.fire_sequence()
        else:
            run_cycle=range(cls._sequence_maps['size'])
            for n in run_cycle:cls.fire_sequence(index=n)
        print('[+] Sequence is done')

