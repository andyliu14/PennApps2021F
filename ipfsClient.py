import ipfshttpclient


class IpfsClient:
    def __init__(self, connectAddr):
        self._client = ipfshttpclient.connect(connectAddr, session=True)

    def add_file(self, file):
        hash = self._client.add(file, recursive=True)['Hash']
        self._client.pin.ls(type='all')
        return hash
    def add_temp_file(self, file):
        hash = self._client.add(file, recursive=True)['Hash']
        self._client.pin.ls(type='all')
        return hash
    def retrieve_file(self, hash):
        return self._client.cat(hash)
    
    def close(self):
        self._client.close()
    