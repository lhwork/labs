# -*- coding: UTF-8 -*-

import stackless

class Event():
    def __init__(self, name, params):
        self.name = name
        self.params = params

class EventDispatcher():
    def __init__(self):
        self.listener = {}
        self.channel = stackless.channel()
        self.channel.preference = 1
        stackless.tasklet(self.listen)()

    def fireEvent(self, msg):
        if isinstance(msg, Event):
            try:
                self.channel.send(msg)
            except:
                stackless.tasklet(self.channel.send)(msg)
        else:
            raise 'event obj is required.'

    def listen(self):
        while True:
            msg = self.channel.receive()
            if isinstance(msg, Event):
                #print 'listen:', msg.name, msg.params
                for f,p in self.listener[msg.name]:
                    stackless.tasklet(f)(msg.params,p)
            else:
                break

    def addListener(self, eventType, func, *args):
        if self.listener.has_key(eventType):
            self.listener[eventType].append((func,args))
        else:
            self.listener[eventType]=[(func,args)]

class Dog(EventDispatcher):
    def __init__(self,name):
        EventDispatcher.__init__(self)
        self.name = name

    def eat(self, food='cake'):
        self.fireEvent(Event('eat', food))

    def beat(self, something='rabbit'):
        self.fireEvent(Event('beat', something))

    def run(self, direct='east'):
        self.fireEvent(Event('beat', direct))

class DogMaster():
    name = '小强'
    def __init__(self, dog):
        if isinstance(dog, Dog):
            self.dog = dog
            self.dog.addListener('eat',self.onEat)
            self.dog.addListener('beat',self.onBeat)

    def feedMyDog(self, food):
        self.dog.fireEvent(Event('eat',food))

    def trainMyDog(self, xxx):
        self.dog.fireEvent(Event('beat',xxx))

    def onEat(self, s,*args):
        print 'my dog is eating:', s
        stackless.schedule()
        print 'onEat.over'

    def onBeat(self, s,*args):
        print 'my dog is beating:', s
        stackless.schedule()
        print 'onBeat.over'

def task():
    a = DogMaster(Dog('大熊'))
    a.feedMyDog('狗粮')
    a.trainMyDog('兔子')

t = stackless.tasklet(task)()

print '_start_'
stackless.run()
print '_end_'
