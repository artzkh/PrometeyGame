import os
from unittest import IsolatedAsyncioTestCase
from vkbottle import API, PhotoMessageUploader, VKAPIError

import config


class TestData:
    peer_id = 318378590
    group_id = 205473455
    message = 'test'
    file_source = os.path.abspath(__file__) + r'\..\test_image.png'


class TestApi(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.api = API(token=config.BOT_TOKEN)

    async def test_get_users(self):
        try:
            await self.api.users.get(user_ids=['-1'])
            self.assert_(False, "VKAPIError(113) not called")
        except VKAPIError(113):
            pass

        result = (await self.api.users.get(user_ids=['lifestealer86']))[0]
        self.assertEqual(result.first_name, 'Михаил')
        self.assertEqual(result.last_name, 'Фунтиков')

        result = (await self.api.users.get(user_ids=[str(TestData.peer_id)]))[0]
        self.assertEqual(result.first_name, 'Артём')
        self.assertEqual(result.last_name,  'Захаров')

    async def test_upload_images(self):
        photo_message_uploader = PhotoMessageUploader(self.api, generate_attachment_strings=True)

        try:
            await photo_message_uploader.upload(file_source=TestData.file_source,
                                                peer_id=1)
            self.assert_(False, "VKAPIError(901) not called")
        except VKAPIError(901):
            pass

        with self.assertRaises(FileNotFoundError):
            await photo_message_uploader.upload(file_source='/not_exist',
                                                peer_id=TestData.peer_id)

        attachment = await photo_message_uploader.upload(file_source=TestData.file_source,
                                                         peer_id=TestData.peer_id)
        self.assertIsInstance(attachment, str)

    async def test_messages_send(self):

        try:
            await self.api.messages.send(peer_id=1,
                                         random_id=0,
                                         message=TestData.message)
            self.assert_(False, "VKAPIError(901) not called")
        except VKAPIError(901):
            pass

        message_id = await self.api.messages.send(peer_id=TestData.peer_id,
                                                  random_id=0,
                                                  message=TestData.message)
        self.assertIsInstance(message_id, int)

    async def test_messages_edit(self):
        photo_message_uploader = PhotoMessageUploader(self.api, generate_attachment_strings=True)

        message_id = await self.api.messages.send(peer_id=TestData.peer_id,
                                                  random_id=0,
                                                  message=TestData.message)

        attachment = await photo_message_uploader.upload(file_source=TestData.file_source,
                                                         peer_id=TestData.peer_id)

        edit_status = await self.api.messages.edit(peer_id=TestData.peer_id,
                                                   group_id=TestData.group_id,
                                                   message_id=message_id,
                                                   message=TestData.message,
                                                   attachment=attachment)
        self.assertTrue(edit_status)

    async def test_messages_delete(self):

        message_id = await self.api.messages.send(peer_id=TestData.peer_id,
                                                  random_id=0,
                                                  message='delete')

        delete_status = await self.api.messages.delete(peer_id=TestData.peer_id,
                                                       group_id=TestData.group_id,
                                                       message_ids=[message_id])
        self.assertTrue(delete_status)

    async def asyncTearDown(self):
        await self.api.http.session.close()
