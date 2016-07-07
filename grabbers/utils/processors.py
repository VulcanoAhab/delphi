from grabbers.utils.html import Pythoness

class ProcessSequence:
    '''
    '''
    _browser=None
    _job=None
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
        mapped_elements=ps.map_sequence_targets(mapper, cls._browser)
        mlen=len(mapped_elements)
        print('[+] Mapped [{}] elements'.format(mlen))
        if mlen < 1:
            print('[+] Mapping lower than 1 has no purpose')
            print(cls._browser.browser.page_source[:500])
            print('[+] Mapped [{}] elements'.format(mlen))
            return
        cls._sequence_maps={
            'size':mlen,
            'attrs':[m.attrib for m in mapped_elements]
                }

    @classmethod
    def fire_sequence(cls, index=-1):
        '''
        '''
        for n,grabber in enumerate(cls._sequence):
            print('[+] Grabber [{}] running.'.format(grabber))
            ps=Pythoness()
            ps.set_job(cls._job)
            ps.set_grabber(grabber)
            if n == 0:#only the first one after mapping
                ps.session(cls._browser, element_index=index)
            else:
                ps.session(cls._browser, element_index=-1)
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

