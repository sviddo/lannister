import pytest
import requests
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
                
        
class TestCreateRequests:
    # @pytest.mark.order(after="test_users.py::TestHandleReviewerRole::test_delete_valid_data")
    @pytest.mark.parametrize("test",
                             create_invalid_requests())   
    def test_invalid_data(self, test):
        invalid_request = requests.post(url + "/api/create_request", json=test)
        
        assert invalid_request.status_code == 400
        
    
    # @pytest.mark.order(after="test_users.py::TestHandleReviewerRole::test_delete_valid_data")
    @pytest.mark.parametrize("test",
                             create_valid_requests())
    def test_valid_data(self, test):
        valid_request = requests.post(url + "/api/create_request", json=test)
        # print(valid_request.json())
        # print(valid_request.status_code)
        assert valid_request.status_code == 201
        

# a = TestCreateRequests() 
# for elem in create_valid_requests():
#     a.test_valid_data(elem)