
import credis
#see https://github.com/yihuang/credis

from JumpScale import j
import JumpScale.baselib.redis

class Redis():

    def __init__(self, addr="127.0.0.1",port=7768):
        self.redis=credis.Connection(host=addr,port=port)
        self.redis.connect()    
        self.fallbackredis=j.clients.redis.getRedisClient(addr,port)
        #certain commands (which are not performance sensitive need normal pyredis)

    def llen(self,key):
        return self.redis.execute('LLEN',key)

    def rpush(self,key, item):
        return self.redis.execute('RPUSH',key,item)

    def blpop(self,key, timeout="60"):
        return self.redis.execute('BLPOP',key,0)

    def lpop(self,key):
        return self.redis.execute('LPOP',key)
        
    def get(self,key):
        return self.redis.execute('GET',key)

    def set(self,key,value):
        return self.redis.execute('SET',key,value)

    def incr(self,key):
        return self.redis.execute('INCR',key)

    def incrby(self,key,nr):
        return self.redis.execute('INCRBY',key,nr)

    def delete(self,key):
        return self.redis.execute('DEL',key)

    def scriptload(self,script):
        return self.fallbackredis.script_load(script)
        # return self.redis.execute('SCRIPTLOAD',script)

    def evalsha(self,sha,nrkeys,*args):
        return self.redis.execute('EVALSHA',sha,nrkeys,*args)

    def eval(self,script,nrkeys,*args):        
        return self.redis.execute('EVAL',script,nrkeys,*args)
        
        

