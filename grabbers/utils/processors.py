from grabbers.utils.crushers import Pythoness
from grabbers.utils.filters import Condis


class ProcessSequence:
    '''
    '''
    def __init__(self):
        self._browser=None
        self._job=None
        self._task=None
        self._sequence=None
        self._target_url=None
        self._sequence_maps={
            'size':1,
            'rects':[]
                }


    def set_job(self, job):
        '''
        '''
        self._job=job

    def set_task(self, task):
        '''
        '''
        self._task=task

    def set_target_url(self, url):
        '''
        '''
        self._target_url=url

    def set_browser(self, browser):
        '''
        '''
        self._browser=browser

    def set_sequence(self, sequence):
        '''
        '''
        self._sequence=sequence

    def mapping(self, mapper):
        '''
        '''
        if not mapper:return
        self._browser.page_source(job=self._job)
        ps=Pythoness()
        ps._job=self._job
        ps.map_targets(mapper, self._browser)


    def fire_sequence(self, index=-1):
        '''
        '''
        #always save page source before sequence
        self._browser.page_source(job=self._job, target_url=self._target_url)
        iseq=self._sequence.indexed_grabbers.all().order_by('sequence_index')
        #start grabbers sequence
        for indexed_grabber in iseq:
            print('[+] Grabber [{}] running.'.format(indexed_grabber))
            ps=Pythoness()
            ps.set_job(self._job)
            ps.set_task(self._task)
            ps.set_grabber(indexed_grabber.grabber)
            ps.session(self._browser, element_index=index)
            ps.save_data(self._browser, target_url=self._target_url)

    def run(self):
        '''
        '''
        if not self._sequence:
            print('[+] No sequence to work')
            return
        if self._sequence_maps['size']<=1:
            self.fire_sequence()
        else:
            run_cycle=range(self._sequence_maps['size'])
            for n in run_cycle:self.fire_sequence(index=n)
        print('[+] Sequence is done')



class ProcessCondition:
    '''
    '''
    def __init__(self, browser, condition):
        self._browser=browser
        self._sequence=condition.sequence
        self._condition=condition

    def fire_sequence(self, index=-1):
        '''
        '''
        iseq=self._sequence.indexed_grabbers.all().order_by('sequence_index')
        #start grabbers sequence
        for indexed_grabber in iseq:
            print('[+] Grabber [{}] running.'.format(indexed_grabber))
            ps=Pythoness()
            ps.set_grabber(indexed_grabber.grabber)
            ps.session(self._browser, element_index=index)
        #condition save only on by the last sequence element
        ps.save_condition(self._browser, self._condition)

    def run(self):
        '''
        '''
        if not self._condition:
            print('[-] No condition to work')
            return

        ####------  test condition ---------------
        ##########################################
        Condis.type=self._condition.type
        Condis.relation=self._condition.relation
        Condis.value=self._condition.value
        if not Condis.test(self._browser):return
        self.fire_sequence()
        print('[+] Condition::sequence is done')
