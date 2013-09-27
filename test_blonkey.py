from app import app
from flask import json
import re


class Tests:
    app.testing = True
    client = app.test_client(use_cookies=True)
    #Testing request to TAG not logged in, should return 401

    def test_tag_request(self, status_code=401):
        assert self.client.get('/tags').status_code == status_code

    def test_login_and_logout(self):
        #Log in
        assert self.login().status_code == 200
        #Cheching you have the log out button, which requires been logged in
        assert "Log Out" in self.get('/index').data
        #Log out
        assert self.logout().status_code == 200
        #Checking there is not log out button
        assert "Log Out" not in self.get('/index').data

    def test_add_and_delete_post(self):
        self.login()
        post_resp = self.add_post()
        assert post_resp.status_code == 302
        ##Getting ID from response
        match = re.search(r'/post/\d+', post_resp.data).group()
        post_id = int(match.split("/")[2])
        # Checking that the post exist
        assert self.get("/post/%d" % post_id).status_code == 200
        # Deleting Post and checking that the address try to redirect to /index
        self.del_post(post_id)
        assert self.get("/post/%d" % post_id).status_code == 302
        self.logout()

    def test_add_and_delete_tag(self):
        self.login()
        #Adding a new Tag ( by default is "Test")
        tag = json.loads(self.add_tag().data)
        assert 'name' in tag
        #I try to insert 2 times the same tag will return an error
        assert 'error' in json.loads(self.add_tag().data)
        #Deleting tag
        assert 'id' in json.loads(self.del_tag(tag['id']).data)

    ## Helper methods

    #By default the login is as admin

    def login(self, nickname="admin", password="FastMonkeys"):
        return self.client.post('/login',
                                data=dict(
                                    nickname=nickname,
                                    password=password),
                                follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def get(self, endpoint, follow_redirects=False):
        return self.client.get(endpoint, follow_redirects=follow_redirects)

    def add_post(self, title='Default test title',
                 text="Default text entry", tags="", follow_redirects=False):
        if tags == "":
            return self.client.post('/post/add',
                                    data=dict(
                                        title=title,
                                        text=text),
                                    follow_redirects=follow_redirects)
        else:
            return self.client.post('/post/add',
                                    data=dict(
                                        title=title,
                                        text=text,
                                        tags=tags),
                                    follow_redirects=follow_redirects)

    def del_post(self, id, follow_redirects=False):
        return self.client.get("/post/%d/delete" % id,
                               follow_redirects=follow_redirects)

    def add_tag(self, name='Test', follow_redirects=False):
        return self.client.post('/tags/add',
                                data=dict(
                                    name=name),
                                follow_redirects=follow_redirects)

    def del_tag(self, id, follow_redirects=False):
        return self.client.post('/tags/del',
                                data=dict(
                                    id=id),
                                follow_redirects=follow_redirects)
