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
from services import return_users_to_add, url

# @pytest.mark.dependency(depends=["TestAddSingleUser::test_valid_data"])
def test_get_requests():
    entire_url = url + "/api/requests"
    all_requests = requests.get(url=entire_url)
    
    assert all_requests.status_code == 200 or \
        all_requests.status_code == 400 and all_requests.json() == ["No requests created!"]
        
