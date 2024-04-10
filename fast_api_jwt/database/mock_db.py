from typing import Dict, Any


class MockDB:
    def __init__(self):
        self.account_data = {
            '2112': {
                'id': '2112',
                'username': 'stevenm',
                'email': 'stevenm@nowhere.com'
            },
            '2113': {
                'id': '2113',
                'username': 'foobar',
                'email': 'foobar@nowhere.com'
            }
        }
        self.storyspace_data = {}

    def get_account(self, id: str) -> Dict[str, Any]:
        return self.account_data[id]

    def get_account_by_username(self, username: str) -> Dict[str, Any]:
        matches = [v for v in self.account_data.values() if v["username"] == username]
        assert len(matches)
        return matches[0]

    def add_account(self, account: Dict[str, Any]) -> Dict[str, Any]:
        assert 'id' in account
        assert 'username' in account

        self.account_data[account['id']] = account
        return account
