from time import sleep
import asyncio
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Group
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        print('websocket Connected...', event)
        print('channel layer...', self.channel_layer)
        print('channel name...', self.channel_name)
        print('groupname ...', self.groupname)
        async_to_sync(self.channel_layer.group_add)(
            self.groupname, #static group name
            self.channel_name
            )
        self.send({
            'type': 'websocket.accept',
        })

    def websocket_receive(self, event):
        print('Message Recieved...', event)
        print('message: ', event['text'])
       

        async_to_sync(self.channel_layer.group_send)(self.groupname, {
            'type': 'chat.message',  # event , now we have to write handler for this event
            'message': event['text'],
            'sender': self.channel_name,
        })

        # <!.. realtime data sending >
        # for i in range(50) :
        #     self.send({
        #         'type' : 'websocket.send',
        #         'text' : str(i)
        #     })
        #     sleep(1)


    # self defined handler for event(chat.message)
    def chat_message(self, event):
        print('Event...', event)
        if(event['sender'] != self.channel_name):
            self.send({
                'type': 'websocket.send',
                'text': event['message'],
            })


    def websocket_disconnect(self, event):
        print('websocket Disconnected...', event)
        async_to_sync(self.channel_layer.group_discard)(
            self.groupname,
            self.channel_name
        )             
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        print('websocket Connected...', event)
        print('channel layer...', self.channel_layer)
        print('channel name...', self.channel_name)
        print('groupname...', self.groupname)
        await self.channel_layer.group_add(
            self.groupname, #static group name
            self.channel_name
            )
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        print('Message Recieved...', event)
        print('message: ', event['text'])
        print()
        await self.channel_layer.group_send(self.groupname, {
            'type': 'chat.message',  # event , now we have to write handler for this event
            'message': event['text'],
            'sender': self.channel_name,
        })

    async def chat_message(self, event):
        print('Event...', event)
        if(event['sender'] != self.channel_name):
            await self.send({
                'type': 'websocket.send',
                'text': event['message'],
            })

    async def websocket_disconnect(self, event):
        print('websocket Disconnected...', event)
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )            
        raise StopConsumer()