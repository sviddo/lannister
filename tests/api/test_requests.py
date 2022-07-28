import pytest
import requests
import datetime
# import os
# import sys
# path_windows = "\\".join(os.path.abspath(__file__).split("\\")[:-3])
# path_linux = "/".join(os.path.abspath(__file__).split("/")[:-3])
# sys.path.append(path_windows)
# sys.path.append(path_linux)
# from tests.services import return_users_to_add, return_workers
# from api.test_users import TestAddSingleUser
from services import (
    url, 
    return_users_to_add, 
    create_invalid_requests,
    return_workers,
    create_valid_requests,
)

# print(len(create_requests()))
# for elem in create_requests():
#     print(elem)
# print([elem for elem in create_requests()])

# @pytest.mark.dependency(depends=["TestAddSingleUser::test_valid_data"])
def test_get_requests():
    entire_url = url + "/api/requests"
    all_requests = requests.get(url=entire_url)
    
    assert all_requests.status_code == 200 or \
        all_requests.status_code == 400 and all_requests.json() == ["No requests created!"]
                
created_requests = []

class TestCreateRequests:
    # @pytest.mark.order(after="test_users.py::TestHandleReviewerRole::test_delete_valid_data")
    @pytest.mark.parametrize("test",
                             create_invalid_requests())   
    def test_invalid_data(self, test):
        invalid_request = requests.post(url + "/api/create_request", json=test)
        
        assert invalid_request.status_code == 400
        
    
    # @pytest.mark.order(after="test_users.py::TestHandleReviewerRole::test_delete_valid_data")
    @pytest.mark.dependency(name="TestCreateRequests::test_valid_data")
    @pytest.mark.parametrize("test",
                             create_valid_requests())
    def test_valid_data(self, test):
        valid_request = requests.post(url + "/api/create_request", json=test)

        assert valid_request.status_code == 201
        
        created_requests.append(valid_request.json())
        
        
class TestUpdateRequests:
    @pytest.mark.parametrize("test", ["a", "b", "c"])
    def test_invalid_data_ids(self, test):
        invalid_request = requests.patch(url + f"/api/request/{test}", json={"bonus_type": "jbcj"})

        assert invalid_request.status_code == 400
        
        
    @pytest.mark.dependency(depends=["TestCreateRequests::test_valid_data"])
    def test_invalid_data(self):
        created_requests_copy = created_requests.copy()
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[0]['id']}", json={"creation_time": "2022-07-28T07:03:22.941528Z"})
        assert invalid_request.status_code == 400
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"creator": "abc"})
        assert invalid_request.status_code == 400
        
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"paymant_day": tomorrow})
        assert invalid_request.status_code == 400
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"paymant_day": tomorrow, "status": "r"})
        assert invalid_request.status_code == 400
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"paymant_day": tomorrow, "status": "p"})
        assert invalid_request.status_code == 400
                
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}")
        assert invalid_request.status_code == 400
        
        
    @pytest.mark.dependency(depends=["TestCreateRequests::test_valid_data"])
    def test_valid_data(self):
        invalid_request = requests.patch(url + f"/api/request/{created_requests[0]['id']}", json={"status": "r"})
        assert invalid_request.status_code == 201
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests[1]['id']}", json={"status": "p"})
        assert invalid_request.status_code == 201
        
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests[2]['id']}", json={"paymant_day": tomorrow,
                                                                                                  "status": "a"})
        assert invalid_request.status_code == 201
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests[3]['id']}", json={"bonus_type": "random_data"})
        assert invalid_request.status_code == 201
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests[3]['id']}", json={"description": "random_data"})
        assert invalid_request.status_code == 201
        
        

class TestGetRequestsPerUser:
    @pytest.mark.dependency(depends=["TestCreateRequests::test_valid_data"])
    @pytest.mark.parametrize("test", return_users_to_add())
    def test_valid_data_user(self, test):
        # print(test)
        # assert url + f"/api/requests/{test['service_id']}" == "http"
        invalid_requests = requests.get(url + f"/api/requests/{test['service_id']}")
        assert invalid_requests.status_code == 200

        # assert invalid_requests.status_code == 200
        
        
    @pytest.mark.dependency(depends=["TestCreateRequests::test_valid_data"])
    @pytest.mark.parametrize("test", [user for user in return_users_to_add() if "r" in user["roles"]])
    def test_valid_data_reviewer(self, test):
        # print(test)
        # assert url + f"/api/requests/{test['service_id']}" == "http"
        invalid_requests = requests.get(url + f"/api/requests/{test['service_id']}")
        assert invalid_requests.status_code == 200
        
    
    @pytest.mark.parametrize("test", 
                             ["abc",
                              "def",
                              "jhcjhdh"])
    def test_invalid_data_ids(self, test):
        invalid_request = requests.get(url + f"/api/requests/{test}")

        assert invalid_request.status_code == 400
        
        

# class TestGetRequestsPerUser:
#     @pytest.mark.dependency(depends=["TestCreateRequests::test_valid_data"])
#     @pytest.mark.parametrize("test", return_users_to_add())
#     def test_valid_data(self, test):
#         # print(test)
#         # assert url + f"/api/requests/{test['service_id']}" == "http"
#         invalid_requests = requests.get(url + f"/api/requests/{test['service_id']}")
#         assert invalid_requests.status_code == 200

#         # assert invalid_requests.status_code == 200
        
    
#     @pytest.mark.parametrize("test", 
#                              ["abc",
#                               "def",
#                               "jhcjhdh"])
#     def test_invalid_data_ids(self, test):
#         invalid_request = requests.get(url + f"/api/requests/{test}")

#         assert invalid_request.status_code == 400
    
        
        

# a = TestGetRequestsPerUser() 
# for elem in return_users_to_add():
#     a.test_valid_data(elem)