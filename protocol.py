'''
Created on 21 Nov 2018

@author: devwarrior
'''

class Protocol(object):
    '''
    Defines requests and responses between app-client and app-server
    '''
    known_cmds = [ 'ping' ]
    
    @classmethod
    def make_ping_request(cls):
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(cmd='ping'),
        )

    #. . .
    
    @classmethod
    def get_response_content(cls, request):
        content = {'error': None}
        cmd = request['cmd']
        if not cmd in cls.known_cmds:
            content['error'] = 'unknown command: {}'.format(cmd)
            return content
        
        if cmd == 'ping':
            content['result'] = 'pong'
        #
            
        return content   
            